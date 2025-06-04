from datetime import date, timedelta

from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Q
from datetime import datetime

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
                financial_doc = FinancialDocuments(
                    typeInvoice=FinancialDocuments.RHE,
                    idInvoice=doc_emitido,
                    idClient=cliente,
                    doc_status=doc_status_map.get(item['Estado Doc. Emitido'], FinancialDocuments.NOANULADO),
                    doc_emisor=FinancialDocuments.RUC,
                    typeCurrency=currency_map.get(item['Moneda de Operación'], FinancialDocuments.SOLES),
                    date=datetime.strptime(item['Fecha de Emisión'], '%d/%m/%Y').date(),
                    description=item['Descripción'],
                    amount=float(item['Renta Bruta']),
                    incomeTax=float(item['Impuesto a la Renta']),
                    netAmount=float(item['Renta Neta']),
                    pendingNetPayment=float(item['Monto Neto Pendiente de Pago']),
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
        return redirect('documentos_app:carga-doc-rhe')

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
              
              # Espacio de nombres (ajustar según tu XML)
              ns = {'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2',
                    'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2',
                    'ext': 'urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2',
                    'sac': 'urn:sunat:names:specification:ubl:peru:schema:xsd:SunatAggregateComponents-1'
                  }
              
              # Extraer datos del XML
              fields = {}
              invoice_id = root.find('.//cbc:ID', ns).text if root.find('.//cbc:ID', ns) is not None else None
              issue_date = root.find('.//cbc:IssueDate', ns).text if root.find('.//cbc:IssueDate', ns) is not None else None
              document_type = root.find('.//cbc:InvoiceTypeCode', ns).text if root.find('.//cbc:InvoiceTypeCode', ns) is not None else None
              currency = root.find('.//cbc:DocumentCurrencyCode', ns).text if root.find('.//cbc:DocumentCurrencyCode', ns) is not None else None
              total_amount = root.find('.//cbc:PayableAmount', ns).text if root.find('.//cbc:PayableAmount', ns) is not None else None
              supplier_id = root.find('.//cac:AccountingSupplierParty/cac:Party/cac:PartyIdentification/cbc:ID', ns).text if root.find('.//cac:AccountingSupplierParty/cac:Party/cac:PartyIdentification/cbc:ID', ns) is not None else None
              client_recept = root.find('.//cac:AccountingCustomerParty/cac:Party/cac:PartyIdentification/cbc:ID', ns).text if root.find('.//cac:AccountingCustomerParty/cac:Party/cac:PartyIdentification/cbc:ID', ns) is not None else None

              
              # Mapear campos
              if invoice_id:
                  fields['idInvoice'] = invoice_id
                  # Verificar si ya existe
                  if FinancialDocuments.objects.filter(idInvoice=invoice_id).exists():
                      response_data['alerts'].append(f'Ya existe un documento con el ID {invoice_id}')

              if client_recept:
                  # Verificar si existe ruc receptor para evitar facturas de otras empresas
                  idTin =  Tin.objects.filter(tin = client_recept).first()

                  if idTin:
                    fields['idTin'] = idTin.id
                  else:
                      response_data['alerts'].append(f'El RUC {client_recept} no pertenece al grupo empresarial ')

              if issue_date:
                  fields['date'] = issue_date
              
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
              
              if total_amount:
                  fields['amount'] = total_amount
              
              # Buscar cliente
              if supplier_id:
                  from applications.clientes.models import Cliente
                  cliente = Cliente.objects.filter(ruc=supplier_id).first()

                  if cliente:
                      print(supplier_id,cliente.id)
                      fields['idClient'] = cliente.id
                      if FinancialDocuments.objects.filter(idInvoice=invoice_id, idClient__ruc=supplier_id).exists():
                          response_data['alerts'].append(
                              f'¡Alerta! Ya existe un documento con ID {invoice_id} para el cliente {cliente.razon_social} (RUC: {supplier_id})'
                          )
              
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
