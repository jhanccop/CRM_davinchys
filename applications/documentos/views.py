from datetime import date, timedelta

from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Q
from datetime import datetime
import json

from django.http import JsonResponse
import xml.etree.ElementTree as ET

from applications.users.mixins import (
  AdminPermisoMixin,
  AdminClientsPermisoMixin, # Adquisiciones, Finanzas, Tesoreria, contabilidad y administrador
  ContabilidadPermisoMixin,
  ComprasContabilidadPermisoMixin
)


from django.urls import reverse_lazy, reverse

from django.views.generic import (
    DetailView,
    DeleteView,
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    TemplateView,
    FormView,
)

from .models import (
  FinancialDocuments,
  OthersDocuments,
  RawsFilesRHE,
)

from applications.clientes.models import Cliente
from applications.cuentas.models import Tin

from .forms import (
  FinancialDocumentsForm,
  OthersDocumentsForm,
  UploadRHETextFileForm,
)

# ================= CARGA MASIVA RHE ========================
class UploadRHEFileView(FormView):
    template_name = 'documentos/procesar_RHE.html'
    form_class = UploadRHETextFileForm
    success_url = reverse_lazy('documentos_app:procesamiento-doc-rhe')
    
    def form_valid(self, form):
        # Guardar el archivo primero
        rhe_file = form.save(commit=False)
        rhe_file.status = RawsFilesRHE.PROCESANDO
        rhe_file.save()
        
        # Almacenar el ID en la sesión para el siguiente paso
        self.request.session['rhe_file_id'] = rhe_file.id
        return super().form_valid(form)

class ProcessRHEFileView(TemplateView):
    template_name = 'documentos/resultsRHE.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rhe_file_id = self.request.session.get('rhe_file_id')
        
        if not rhe_file_id:
            return context
            
        rhe_file = RawsFilesRHE.objects.get(id=rhe_file_id)
        
        # Procesar el archivo de texto a JSON
        processed_data = self.process_text_file(rhe_file.archivo)
        context['processed_data'] = processed_data
        
        # Verificar duplicados
        duplicates = []
        errors = []
        
        for item in processed_data['data']:
            doc_emitido = item['Nro_Doc_Emitido']
            doc_emisor = item['Nro_Doc_Emisor']
            
            # Verificar si existe en FinancialDocuments
            existing = FinancialDocuments.objects.filter(
                Q(idInvoice=doc_emitido) & 
                Q(idClient__ruc=doc_emisor)
            ).first()
            
            if existing:
                duplicates.append({
                    'data': item,
                    'existing': existing
                })
        
        context['duplicates'] = duplicates
        context['errors'] = errors
        context['rhe_file_id'] = rhe_file_id
        
        return context
    
    def process_text_file(self, file):
        lines = file.read().decode('utf-8').splitlines()
        #headers = lines[0].split('|')
        headers = [h.replace(' ', '_').replace('.', '').replace(',', '') for h in lines[0].split('|')]
        data = []
        
        for line in lines[1:]:
            if not line.strip():
                continue
                
            values = line.split('|')
            item = dict(zip(headers, values))
            data.append(item)
        
        return {
            "metadata": {
                "total_registros": len(data),
                "campos": headers,
                "anotaciones": "No hay anotaciones"
            },
            "data": data
        }
    
    def post(self, request, *args, **kwargs):
        rhe_file_id = request.session.get('rhe_file_id')
        if not rhe_file_id:
            return redirect('documentos_app:carga-doc-rhe')
            
        rhe_file = RawsFilesRHE.objects.get(id=rhe_file_id)
        processed_data = self.process_text_file(rhe_file.archivo)
        
        # Guardar los datos en FinancialDocuments
        saved_count = 0
        duplicates_count = 0
        
        for item in processed_data['data']:
            doc_emitido = item['Nro_Doc_Emitido']
            doc_emisor = item['Nro_Doc_Emisor']
            
            # Verificar si ya existe
            existing = FinancialDocuments.objects.filter(
                Q(idInvoice=doc_emitido) & 
                Q(idClient__ruc=doc_emisor)
            ).first()
            
            if existing:
                duplicates_count += 1
                continue
                
            # Obtener cliente por RUC
            try:
                cliente = Cliente.objects.get(ruc=doc_emisor)
            except Cliente.DoesNotExist:
                cliente = None
                
            # Mapear datos al modelo
            doc_status_map = {
                'NO ANULADO': FinancialDocuments.NOANULADO,
                'ANULADO': FinancialDocuments.ANULADO,
                'REVERTIDO': FinancialDocuments.REVERTIDO
            }
            
            currency_map = {
                'SOLES': FinancialDocuments.SOLES,
                'DÓLARES DE NORTE AMÉRICA': FinancialDocuments.DOLARES,
                'Dï¿½LARES DE NORTE AMï¿½RICA': FinancialDocuments.DOLARES,
                'EUROS': FinancialDocuments.EUROS
            }
            
            try:
                compania_id = self.request.session.get('compania_id')
                tin = Tin.objects.get(id = compania_id)

                financial_doc = FinancialDocuments(
                    typeInvoice = FinancialDocuments.RHE,
                    idInvoice = doc_emitido,
                    idClient = cliente,
                    idTin = tin,
                    doc_status = doc_status_map.get(item['Estado_Doc_Emitido'], FinancialDocuments.NOANULADO),
                    doc_emisor = FinancialDocuments.RUC,
                    typeCurrency = currency_map.get(item['Moneda_de_Operación'], FinancialDocuments.SOLES),
                    date = datetime.strptime(item['Fecha_de_Emisión'], '%d/%m/%Y').date(),
                    description = item['Descripción'],
                    amount = float(item['Renta_Bruta']),
                    incomeTax = float(item['Impuesto_a_la_Renta']),
                    netAmount = float(item['Renta_Neta']),
                    pendingNetPayment = float(item['Monto_Neto_Pendiente_de_Pago']),
                    user=request.user
                )
                financial_doc.save()
                saved_count += 1
            except Exception as e:
                print(f"Error al guardar documento {doc_emitido}: {str(e)}")
        
        # Actualizar estado del archivo original
        rhe_file.status = RawsFilesRHE.COMPLETADO
        rhe_file.procesado = True
        rhe_file.save()
        
        messages.success(request, f"Se guardaron {saved_count} registros. {duplicates_count} duplicados omitidos.")
        return redirect('documentos_app:documento-financiero-lista')

# ================= DOCUMENTACION FINANCIEROS ========================
class FinancialDocumentsListView(AdminClientsPermisoMixin,ListView):
  template_name = "documentos/documento-financiero-lista.html"
  context_object_name = 'documentos'

  def get_queryset(self,**kwargs):
    compania_id = self.request.session.get('compania_id')
    selectedType = self.request.GET.get("DocKword", '')

    intervalDate = self.request.GET.get("dateKword", '')
    if intervalDate == "today" or intervalDate =="":
      intervalDate = str(date.today() - timedelta(days = 120)) + " to " + str(date.today())

    if selectedType == "Todo" or selectedType == None or selectedType =="" :
      selectedType = 5

    documentation = FinancialDocuments.objects.ListaDocumentosPorTipo(
      intervalo = intervalDate,
      tipo = int(selectedType),
      compania_id = compania_id
      )
  
    payload = {}
    payload["intervalDate"] = intervalDate
    payload["selected"] = selectedType
    payload["documentation"] = documentation
    
    return payload

class FinancialDocumentsCreateView(AdminClientsPermisoMixin,CreateView):
  template_name = "documentos/documento-financiero-nuevo.html"
  model = FinancialDocuments
  form_class = FinancialDocumentsForm
  success_url = reverse_lazy('documentos_app:documento-financiero-lista')

  def get_form_kwargs(self):
    kwargs = super().get_form_kwargs()
    kwargs['request'] = self.request
    return kwargs
  
  def post(self, request, *args, **kwargs):
      # Verificar si es una solicitud AJAX para solo procesar el XML
      if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and 'process_only' in request.POST:
          return self.process_xml_only(request)
      return super().post(request, *args, **kwargs)

  def process_xml_only(self, request):
    form = self.get_form()
    form.is_valid()  # Ejecuta la validación para procesar el XML
    
    response_data = {
        'success': False,
        'fields': {},
        'alerts': []
    }
      
    if 'xml_file' in request.FILES:
        try:
            xml_file = request.FILES['xml_file']
            tree = ET.parse(xml_file)
            root = tree.getroot()

            namespaces = {
                'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2',
                'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2',
                'ext': 'urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2',
                'sac': 'urn:sunat:names:specification:ubl:peru:schema:xsd:SunatAggregateComponents-1'
            }

            # Extraer información general
            general_info = {
                'numero': root.find('.//cbc:ID', namespaces).text,
                'fecha_emision': root.find('.//cbc:IssueDate', namespaces).text,
                'hora_emision': root.find('.//cbc:IssueTime', namespaces).text,
                'tipo_documento': {
                    'codigo': root.find('.//cbc:InvoiceTypeCode', namespaces).text,
                    'descripcion': 'Factura'
                },
                'moneda': root.find('.//cbc:DocumentCurrencyCode', namespaces).text,
                'total_pagar': float(root.find('.//cbc:PayableAmount', namespaces).text),
                'monto_letras': root.find('.//cbc:Note', namespaces).text.split('[')[-1].split(']')[0]
            }

            # Extraer información del emisor
            supplier = root.find('.//cac:AccountingSupplierParty/cac:Party', namespaces)
            emisor = {
                'ruc': supplier.find('.//cbc:ID', namespaces).text,
                'razon_social': supplier.find('.//cac:PartyLegalEntity/cbc:RegistrationName', namespaces).text.strip(),
                'direccion': {
                    'calle': supplier.find('.//cac:PartyLegalEntity/cac:RegistrationAddress/cac:AddressLine/cbc:Line', namespaces).text.strip(),
                    'distrito': supplier.find('.//cac:PartyLegalEntity/cac:RegistrationAddress/cbc:District', namespaces).text.strip(),
                    'provincia': supplier.find('.//cac:PartyLegalEntity/cac:RegistrationAddress/cbc:CountrySubentity', namespaces).text.strip(),
                    'departamento': supplier.find('.//cac:PartyLegalEntity/cac:RegistrationAddress/cbc:CountrySubentity', namespaces).text.strip(),
                    'codigo_ubigeo': supplier.find('.//cac:PartyLegalEntity/cac:RegistrationAddress/cbc:CountrySubentityCode', namespaces).text.strip()
                }
            }

            # Extraer información del cliente
            customer = root.find('.//cac:AccountingCustomerParty/cac:Party', namespaces)
            cliente = {
                'ruc': customer.find('.//cbc:ID', namespaces).text,
                'razon_social': customer.find('.//cac:PartyLegalEntity/cbc:RegistrationName', namespaces).text.strip(),
                'direccion': {
                    'calle': customer.find('.//cac:PartyLegalEntity/cac:RegistrationAddress/cac:AddressLine/cbc:Line', namespaces).text.strip(),
                    'distrito': customer.find('.//cac:PartyLegalEntity/cac:RegistrationAddress/cbc:District', namespaces).text.strip(),
                    'provincia': customer.find('.//cac:PartyLegalEntity/cac:RegistrationAddress/cbc:CountrySubentity', namespaces).text.strip(),
                    'departamento': customer.find('.//cac:PartyLegalEntity/cac:RegistrationAddress/cbc:CountrySubentity', namespaces).text.strip(),
                    'codigo_ubigeo': customer.find('.//cac:PartyLegalEntity/cac:RegistrationAddress/cbc:CountrySubentityCode', namespaces).text.strip()
                }
            }

            # Extraer totales
            tax_total = root.find('.//cac:TaxTotal', namespaces)
            monetary_total = root.find('.//cac:LegalMonetaryTotal', namespaces)
            totales = {
                'gravado': float(monetary_total.find('.//cbc:LineExtensionAmount', namespaces).text),
                'igv': float(tax_total.find('.//cbc:TaxAmount', namespaces).text),
                'total_venta': float(monetary_total.find('.//cbc:PayableAmount', namespaces).text)
            }

            # Extraer items
            items = []
            for item in root.findall('.//cac:InvoiceLine', namespaces):
                item_data = {
                    'id': int(item.find('.//cbc:ID', namespaces).text),
                    'descripcion': item.find('.//cbc:Description', namespaces).text.strip(),
                    'cantidad': float(item.find('.//cbc:InvoicedQuantity', namespaces).text),
                    'unidad_medida': item.find('.//cbc:InvoicedQuantity', namespaces).attrib.get('unitCode'),
                    'valor_unitario': float(item.find('.//cbc:PriceAmount', namespaces).text),
                    'precio_referencia': float(item.find('.//cac:AlternativeConditionPrice/cbc:PriceAmount', namespaces).text),
                    'igv': float(item.find('.//cac:TaxTotal/cbc:TaxAmount', namespaces).text),
                    'valor_venta': float(item.find('.//cbc:LineExtensionAmount', namespaces).text)
                }
                items.append(item_data)

            # Extraer información adicional
            info_adicional = {
                'forma_pago': root.find('.//cac:PaymentTerms/cbc:PaymentMeansID', namespaces).text,
                'firma_digital': {
                    'presente': True,
                    'emisor': 'SUNAT'
                },
                'version_ubl': root.find('.//cbc:UBLVersionID', namespaces).text,
                'customizacion': root.find('.//cbc:CustomizationID', namespaces).text
            }

            # Construir el JSON final
            factura_json = {
                'factura': {
                    'informacion_general': general_info,
                    'emisor': emisor,
                    'cliente': cliente,
                    'totales': totales,
                    'items': items,
                    'informacion_adicional': info_adicional
                }
            }


            # COMPLETAR DATOS
            fields = {}

            client_recept = factura_json["factura"]["cliente"]["ruc"]

            # Verificar si existe ruc receptor para evitar facturas de otras empresas
            if client_recept:
                idTin =  Tin.objects.filter(tin = client_recept).first()

                if idTin:
                    fields['idTin'] = idTin.id
                else:
                    response_data['alerts'].append(f'El RUC {client_recept} no pertenece al grupo empresarial ')
                    response_data['success'] = True
                    return JsonResponse(response_data)

            supplier_id = factura_json["factura"]["emisor"]["ruc"]
            invoice_id = factura_json["factura"]["informacion_general"]["numero"]

            #  filtro, por id y por ruc para detectar duplicados
            if supplier_id:
                cliente = Cliente.objects.filter(ruc=supplier_id).first()

                if cliente:
                    fields['idClient'] = cliente.id
                    fields['idInvoice'] = invoice_id
                    if FinancialDocuments.objects.filter(idInvoice=invoice_id, idClient__ruc=supplier_id).exists():
                        response_data['alerts'].append(
                        f'¡Alerta! Ya existe un documento con ID {invoice_id} para el cliente {cliente.tradeName} (RUC: {supplier_id})'
                        )
                        response_data['dup'] = True
                else:
                    response_data['alerts'].append(
                    f'¡No se encuentra al porveedor {cliente.tradeName} (RUC: {supplier_id})'
                    )

            issue_date = factura_json["factura"]["informacion_general"]["fecha_emision"]
            document_type = factura_json["factura"]["informacion_general"]["tipo_documento"]["codigo"]

            currency = factura_json["factura"]["informacion_general"]["moneda"]

            total_gravado = factura_json["factura"]["totales"]["gravado"]
            total_igv = factura_json["factura"]["totales"]["igv"]
            total_amount = factura_json["factura"]["totales"]["total_venta"]

            fields['date'] = issue_date
            fields['netAmount'] = total_gravado
            fields['incomeTax'] = total_igv
            fields['amount'] = total_amount

            output = ""

            for item in factura_json["factura"]["items"]:
                output += (
                    f"ID: {item['id']}\n"
                    f"  Descripción     : {item['descripcion']}\n"
                    f"  Cantidad        : {item['cantidad']} {item['unidad_medida']}\n"
                    f"  Valor unitario  : {item['valor_unitario']:.6f}\n"
                    f"  Precio ref.     : {item['precio_referencia']:.6f}\n"
                    f"  Valor venta     : {item['valor_venta']:.4f}\n"
                    f"  IGV             : {item['igv']:.6f}\n"
                    f"{'-' * 60}\n"
                )

            fields['description'] = output

            if document_type:
                doc_type_mapping = {
                    '01': FinancialDocuments.FACTURA,
                    '03': FinancialDocuments.BOLETA,
                    '07': FinancialDocuments.NOTACREDITO,
                    '08': FinancialDocuments.NOTACREDITO
                }
                fields['typeInvoice'] = doc_type_mapping.get(document_type, FinancialDocuments.OTROS)

            if currency:
                currency_mapping = {
                    'PEN': FinancialDocuments.SOLES,
                    'USD': FinancialDocuments.DOLARES,
                    'EUR': FinancialDocuments.EUROS
                }
                fields['typeCurrency'] = currency_mapping.get(currency, FinancialDocuments.SOLES)
            
            
            
            response_data['success'] = True
            response_data['fields'] = fields
            
        except ET.ParseError as e:
            response_data['error'] = 'El archivo XML no es válido'
        except Exception as e:
            response_data['error'] = f'Error al procesar el XML: {str(e)}'
    
    return JsonResponse(response_data)

  def form_valid(self, form):
      xml_file = self.request.FILES.get('xml_file')
      if xml_file:
          instance = form.save(commit=False)
          instance.xml_file = xml_file
          instance.save()
          messages.success(self.request, 'Archivo XML procesado correctamente')
          
          if form.errors:
              for field, errors in form.errors.items():
                  for error in errors:
                      messages.warning(self.request, error)
      else:
          instance = form.save()
          
      return super().form_valid(form)
  
class FinancialDocumentsEditView(AdminClientsPermisoMixin,UpdateView):
  template_name = "documentos/documento-financiero-editar.html"
  model = FinancialDocuments
  form_class = FinancialDocumentsForm
  success_url = reverse_lazy('documentos_app:documento-financiero-lista')

class DocumentacionDetailView(AdminClientsPermisoMixin,ListView):
  template_name = "documentos/documento-financiero-detalle.html"
  context_object_name = 'doc'
  
  def get_queryset(self,**kwargs):
    pk = self.kwargs['pk']
    payload = {}
    document = FinancialDocuments.objects.DocumentosPorId(id = int(pk))
    payload["document"] = document
    return payload
  
class FinancialDocumentsDeleteView(AdminClientsPermisoMixin,DeleteView):
  template_name = "documentos/documento-financiero-eliminar.html"
  model = FinancialDocuments
  success_url = reverse_lazy('documentos_app:documento-financiero-lista')

# ================= DOCUMENTACION GENERICOS ========================
class OthersDocumentsListView(AdminClientsPermisoMixin,ListView):
  template_name = "documentos/documento-generico-lista.html"
  context_object_name = 'documentos'

  def get_queryset(self,**kwargs):
    compania_id = self.request.session.get('compania_id')
    selectedType = self.request.GET.get("DocKword", '')

    intervalDate = self.request.GET.get("dateKword", '')
    if intervalDate == "today" or intervalDate =="":
      intervalDate = str(date.today() - timedelta(days = 120)) + " to " + str(date.today())

    if selectedType == "Todo" or selectedType == None or selectedType =="" :
      selectedType = 5

    documentation = OthersDocuments.objects.ListaDocumentosPorTipo(
      intervalo = intervalDate,
      tipo = int(selectedType),
      compania_id = compania_id
      )
  
    payload = {}
    payload["intervalDate"] = intervalDate
    payload["selected"] = selectedType
    payload["documentation"] = documentation
    
    return payload

class OthersDocumentsCreateView(AdminClientsPermisoMixin,CreateView):
  template_name = "documentos/documento-generico-nuevo.html"
  model = OthersDocuments
  form_class = OthersDocumentsForm
  success_url = reverse_lazy('documentos_app:documento-generico-lista')
  
class OthersDocumentsEditView(AdminClientsPermisoMixin,UpdateView):
  template_name = "documentos/documento-generico-editar.html"
  model = OthersDocuments
  form_class = OthersDocumentsForm
  success_url = reverse_lazy('documentos_app:documento-generico-lista')

class OthersDocumentsDetailView(AdminClientsPermisoMixin,ListView):
  template_name = "documentos/documento-generico-detalle.html"
  context_object_name = 'doc'
  
  def get_queryset(self,**kwargs):
    pk = self.kwargs['pk']
    payload = {}
    document = OthersDocumentsForm.objects.DocumentosPorId(id = int(pk))
    payload["document"] = document
    return payload
  
class OthersDocumentsDeleteView(AdminClientsPermisoMixin,DeleteView):
  template_name = "documentos/documento-generico-eliminar.html"
  model = OthersDocuments
  success_url = reverse_lazy('documentos_app:documento-generico-lista')
