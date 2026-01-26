from datetime import date, timedelta
import json
import re

from django.contrib import messages
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.shortcuts import render, get_object_or_404, redirect

from django.shortcuts import render

from applications.users.mixins import (
  ComercialMixin,
  ComercialFinanzasMixin
)

from django.forms import inlineformset_factory
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
import xml.etree.ElementTree as ET

from django.views.generic import (
    DetailView,
    DeleteView,
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    View,
    FormView,
)

from .models import (
  Incomes,
  quotes,
  Trafo,
  QuoteTracking,
  Items,
  ItemTracking
)

from applications.cuentas.models import (
  Tin,
)

from applications.clientes.models import (
  Cliente,
)

from applications.COMERCIAL.stakeholders.models import client
from applications.PRODUCTION.models import Trafos
from applications.COMERCIAL.sales.models import Items,ItemTracking, ItemImage

from .forms import (
  IncomesForm,
  quotesForm,
  ItemForm,
  ItemImageForm,
  MultipleItemImageForm,
  ItemTrackingForm,
  trafoForm
  )

class QuotesListView(ComercialMixin,ListView):
  template_name = "COMERCIAL/sales/quote-lista.html"
  context_object_name = 'documentos'

  def get_queryset(self,**kwargs):
    compania_id = self.request.session.get('compania_id')
    selectedType = self.request.GET.get("DocKword", '')

    intervalDate = self.request.GET.get("dateKword", '')
    if intervalDate == "today" or intervalDate =="":
      intervalDate = str(date.today() - timedelta(days = 120)) + " to " + str(date.today())

    if selectedType == "Todo" or selectedType == None or selectedType =="" :
      selectedType = 5

    documentation = Incomes.objects.ListaDocumentosPorTipo(
      intervalo = intervalDate,
      tipo = int(selectedType),
      compania_id = compania_id
      )
  
    payload = {}
    payload["intervalDate"] = intervalDate
    payload["selected"] = selectedType
    payload["documentation"] = documentation
    
    return payload

class IncomesCreateView(ComercialMixin,CreateView):
  template_name = "COMERCIAL/sales/ventas-nuevo.html"
  model = Incomes
  form_class = IncomesForm
  success_url = reverse_lazy('ventas_app:ventas-lista')

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
                cliente = client.objects.filter(ruc=supplier_id).first()

                if cliente:
                    fields['idClient'] = cliente.id
                    fields['idInvoice'] = invoice_id
                    if Incomes.objects.filter(idInvoice=invoice_id, idClient__ruc=supplier_id).exists():
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
                    '01': Incomes.FACTURA,
                    '03': Incomes.BOLETA,
                    '07': Incomes.NOTACREDITO,
                    '08': Incomes.NOTACREDITO
                }
                fields['typeInvoice'] = doc_type_mapping.get(document_type, Incomes.OTROS)

            if currency:
                currency_mapping = {
                    'PEN': Incomes.SOLES,
                    'USD': Incomes.DOLARES,
                    'EUR': Incomes.EUROS
                }
                fields['typeCurrency'] = currency_mapping.get(currency, Incomes.SOLES)
            
            
            
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
  
class IncomesEditView(ComercialMixin,UpdateView):
  template_name = "COMERCIAL/sales/ventas-editar.html"
  model = Incomes
  form_class = IncomesForm
  success_url = reverse_lazy('ventas_app:ventas-lista')

class IncomesDetailView(ComercialMixin,ListView):
  
  template_name = "COMERCIAL/sales/ventas-detalle.html"
  context_object_name = 'doc'
  
  def get_queryset(self,**kwargs):
    pk = self.kwargs['pk']
    payload = {}
    document = Incomes.objects.DocumentosPorId(id = int(pk))
    payload["document"] = document
    return payload
  
class IncomesDeleteView(ComercialMixin,DeleteView):
  template_name = "COMERCIAL/sales/ventas-eliminar.html"
  model = Incomes
  success_url = reverse_lazy('ventas_app:ventas-lista')

# ================= COTIZACIONES ========================

class QuoteCreateViewV1(ComercialFinanzasMixin,CreateView):
    model = quotes
    form_class = quotesForm
    template_name = 'COMERCIAL/sales/quote-crear.html'
    success_url = reverse_lazy('ventas_app:cotizaciones-lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trafo_form'] = TrafoForm()
        return context
    
    @transaction.atomic
    def form_valid(self, form):
        # Guardar la cotización
        self.object = form.save()
        
        # Obtener transformadores del campo oculto
        trafos_json = self.request.POST.get('trafos_data', '[]')
        trafos_data = json.loads(trafos_json)
        
        # Crear los transformadores asociados
        for trafo_data in trafos_data:
            trafo = Trafos(
                idTrafoQuote=self.object,
                serialNumber=trafo_data.get('serialNumber'),
                quantity=trafo_data.get('quantity'),
                unitCost=trafo_data.get('unitCost'),
                KVA=trafo_data.get('KVA'),
                KTapHV=trafo_data.get('KTapHV'),
                HVTAP=trafo_data.get('HVTAP'),
                LV=trafo_data.get('LV'),
                FIXHV=trafo_data.get('FIXHV'),
                HZ=trafo_data.get('HZ'),
                TYPE=trafo_data.get('TYPE'),
                MOUNTING=trafo_data.get('MOUNTING'),
                COOLING=trafo_data.get('COOLING'),
                WINDING=trafo_data.get('WINDING'),
                INSULAT=trafo_data.get('INSULAT'),
                CONNECTION=trafo_data.get('CONNECTION'),
                STANDARD=trafo_data.get('STANDARD')
            )
            trafo.save()
        
        # Crear registro de tracking
        QuoteTracking.objects.create(
            idquote=self.object,
            status=QuoteTracking.CREADO,
            area=QuoteTracking.TECHNICIAN
        )
        
        messages.success(self.request, 'Cotización creada exitosamente.')
        return super().form_valid(form)

@method_decorator(csrf_exempt, name='dispatch')
class AddTrafoToQuoteView(ComercialFinanzasMixin,View):
    def post(self, request, *args, **kwargs):
        form = TrafoForm(request.POST)
        
        if form.is_valid():
            # Obtener datos limpios pero excluir idTrafoQuote si existe
            trafo_data = form.cleaned_data.copy()
            
            # Asegurarse de que no se guarde idTrafoQuote en la sesión
            trafo_data.pop('idTrafoQuote', None)
            
            # Inicializar la lista de transformadores en la sesión si no existe
            if 'current_quote_trafos' not in request.session:
                request.session['current_quote_trafos'] = []
            
            # Agregar el nuevo transformador (sin idTrafoQuote)
            request.session['current_quote_trafos'].append(trafo_data)
            request.session.modified = True
            
            return JsonResponse({
                'success': True,
                'message': 'Transformador agregado correctamente.'
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })

class QuoteDetailView(ComercialFinanzasMixin,DetailView):
    model = quotes
    template_name = 'COMERCIAL/sales/quote-detalle.html'
    context_object_name = 'quote'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trafos'] = self.object.item_Quote.all().order_by("-created")
        context['tracking'] = QuoteTracking.objects.filter(idquote=self.object)
        return context

class TrafoQuoteListView(ComercialFinanzasMixin,ListView):
    template_name = 'COMERCIAL/sales/lista-cotizaciones.html'
    context_object_name = 'quotes'
    
    def get_queryset(self,**kwargs):
        compania_id = self.request.user.company.id
        intervalDate = self.request.GET.get("dateKword", '')
        if intervalDate == "today" or intervalDate =="":
            intervalDate = str(date.today() - timedelta(days = 90)) + " to " + str(date.today())

        Quotes = quotes.objects.ListaCotizacionesPorRuc(intervalo = intervalDate, company = compania_id)
        
        payload = {}
        payload["intervalDate"] = intervalDate
        payload["listQuotes"] = Quotes
        return payload

class QuoteUpdateView(ComercialFinanzasMixin,UpdateView):
    model = quotes
    form_class = quotesForm
    template_name = 'COMERCIAL/sales/quote-editar.html'
    context_object_name = 'quote'
    success_url = reverse_lazy('ventas_app:cotizaciones-lista')
    
    #def get_success_url(self):
    #    return reverse_lazy('ventas_app:detalle-cotizacion', kwargs={'pk': self.object.id})
    
    def form_valid(self, form):
        messages.success(self.request, 'Cotización actualizada exitosamente.')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trafos'] = self.object.item_Quote.all()
        return context

class QuoteDeleteView(ComercialFinanzasMixin,DeleteView):
    model = quotes
    template_name = 'COMERCIAL/sales/quote-eliminar.html'
    success_url = reverse_lazy('ventas_app:cotizaciones-lista')

class TrafoPoListView(ComercialFinanzasMixin,ListView):
    template_name = 'COMERCIAL/sales/lista-po.html'
    context_object_name = 'quotes'
    
    def get_queryset(self,**kwargs):
        compania_id = self.request.user.company.id
        intervalDate = self.request.GET.get("dateKword", '')
        if intervalDate == "today" or intervalDate =="":
            intervalDate = str(date.today() - timedelta(days = 90)) + " to " + str(date.today())

        Quotes = quotes.objects.ListaPOPorRuc(intervalo = intervalDate, company = compania_id, isPO = True)
        
        payload = {}
        payload["intervalDate"] = intervalDate
        payload["listQuotes"] = Quotes
        return payload

# ======================================
class QuoteCreateView(ComercialFinanzasMixin, CreateView):
    model = quotes
    form_class = quotesForm
    template_name = 'COMERCIAL/sales/quote_create.html'
    success_url = reverse_lazy('ventas_app:cotizaciones-lista')
    
    @transaction.atomic
    def form_valid(self, form):
        try:
            # Guardar la cotización primero
            self.object = form.save(commit=False)
            
            # Procesar items desde el frontend
            items_data = self.request.POST.get('items_data', '[]')
            files_metadata = self.request.POST.get('files_metadata', '{}')
            
            total_amount = 0
            
            import json
            items_list = json.loads(items_data)
            files_metadata_dict = json.loads(files_metadata)
            
            if not items_list:
                form.add_error(None, 'Debe agregar al menos un transformador')
                return self.form_invalid(form)
            
            # Mapeo inverso para archivos
            file_mapping = {}
            for file_id, metadata in files_metadata_dict.items():
                file_mapping[metadata['item_index']] = {
                    'file_id': file_id,
                    'file_name': metadata['file_name']
                }
            
            # Calcular monto total y crear items
            for index, item_data in enumerate(items_list):
                quantity = int(item_data.get('quantity', 1))
                unit_cost = float(item_data.get('unit_cost', 0))
                total_amount += quantity * unit_cost
            
            # Guardar cotización
            self.object.amount = total_amount
            self.object.initialAmount = total_amount
            self.object.save()
            
            # Procesar cada transformador
            for index, item_data in enumerate(items_list):
                quantity = int(item_data.get('quantity', 1))
                unit_cost = float(item_data.get('unit_cost', 0))
                
                # Obtener archivo si existe
                drawing_file = None
                if index in file_mapping:
                    file_id = file_mapping[index]['file_id']
                    drawing_file = self.request.FILES.get(file_id)
                
                # Crear el Transformador (Trafo)
                trafo = Trafo.objects.create(
                    PHASE=item_data.get('phase'),
                    COOLING=item_data.get('cooling'),
                    MOUNTING=item_data.get('mounting'),
                    KVA=item_data.get('kva'),
                    HV=item_data.get('hv'),
                    LV=item_data.get('lv'),
                    HZ=item_data.get('hz'),
                    WINDING=item_data.get('winding'),
                    CONNECTION=item_data.get('connection'),
                    STANDARD=item_data.get('standard'),
                    drawing_file=drawing_file
                )
                
                # Crear Items (uno por cada unidad)
                base_seq = item_data.get('seq', f'TRAFO-{index+1:03d}')
                
                for i in range(quantity):
                    item_seq = f"{base_seq}-{i+1:03d}" if quantity > 1 else base_seq
                    
                    item = Items.objects.create(
                        idTrafoQuote=self.object,
                        idTrafo=trafo,  # Relación con el transformador
                        seq=item_seq,
                        unitCost=unit_cost,
                    )
                    
                    # Crear tracking para el item
                    #ItemTracking.objects.create(
                    #    idItem=item,
                    #    statusItem=ItemTracking.SOLICITADO,
                    #    statusPlate=ItemTracking.SOLICITADO
                    #)
            
            # Crear tracking de la cotización
            QuoteTracking.objects.create(
                idquote=self.object,
                status=QuoteTracking.ESPERA,
                area=QuoteTracking.COMERCIAL
            )
            
            # Si es AJAX request
            if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'redirect_url': str(self.success_url),
                    'message': f'Cotización creada con {len(items_list)} transformador(es) y {sum(int(i.get("quantity", 1)) for i in items_list)} item(s)'
                })
            
            messages.success(self.request, f'Cotización creada exitosamente con {len(items_list)} transformador(es).')
            return redirect(self.success_url)
            
        except Exception as e:
            print(f"ERROR: {str(e)}")
            form.add_error(None, f'Error al procesar la cotización: {str(e)}')
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'error': 'Por favor corrige los errores en el formulario.',
                'errors': form.errors.as_json()
            })
        
        print("Errores:", form.errors)
        messages.error(self.request, 'Por favor corrige los errores en el formulario.')
        return super().form_invalid(form)

# ================= ITEMS ========================
class CreateTrafoItemView1(ComercialFinanzasMixin, CreateView):
    template_name = "COMERCIAL/sales/crear-item.html"
    model = Items
    form_class = ItemForm

    def get_context_data(self,**kwargs):
        pk = self.kwargs['pk']
        context = super().get_context_data(**kwargs)
        context['pk'] = pk
        return context
    
    def get_success_url(self, *args, **kwargs):
        pk = self.kwargs["pk"]
        return reverse_lazy('ventas_app:cotizacion-detalle', kwargs={'pk':pk})

class CreateTrafoItemView(ComercialFinanzasMixin, CreateView):
    template_name = "COMERCIAL/sales/crear-item.html"
    model = Items
    form_class = ItemForm

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        context = super().get_context_data(**kwargs)
        context['pk'] = pk
        context['quote'] = quotes.objects.get(pk=pk)  # AÑADIR: pasar la cotización al template
        
        # AÑADIR: formulario de Trafo si no existe
        if 'trafo_form' not in context:
            context['trafo_form'] = trafoForm()  # Necesitas crear este form
        return context
    
    @transaction.atomic
    def form_valid(self, form):
        pk = self.kwargs['pk']
        quote = quotes.objects.get(pk=pk)
        
        # AÑADIR: Crear el Trafo primero
        trafo_form = trafoForm(self.request.POST, self.request.FILES)
        
        if not trafo_form.is_valid():
            return self.form_invalid(form)
        
        trafo = trafo_form.save()
        
        # AÑADIR: Obtener cantidad y crear items
        quantity = int(self.request.POST.get('quantity', 1))
        unit_cost = form.cleaned_data.get('unitCost', 0)
        base_seq = form.cleaned_data.get('seq', f'TRAFO-{trafo.id:03d}')
        
        # Crear un Item por cada unidad
        for i in range(quantity):
            item_seq = f"{base_seq}-{i+1:03d}" if quantity > 1 else base_seq
            
            Items.objects.create(
                idTrafoQuote=quote,
                idTrafo=trafo,
                seq=item_seq,
                unitCost=unit_cost,
            )
        
        # AÑADIR: Actualizar monto de la cotización
        quote.amount += quantity * unit_cost
        quote.save()
        
        messages.success(self.request, f'Se añadieron {quantity} item(s) a la cotización.')
        return redirect(self.get_success_url())
    
    def form_invalid(self, form):
        # AÑADIR: manejar errores del trafo_form
        trafo_form = trafoForm(self.request.POST, self.request.FILES)
        return self.render_to_response(
            self.get_context_data(form=form, trafo_form=trafo_form)
        )
    
    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse_lazy('ventas_app:cotizacion-detalle', kwargs={'pk': pk})

class UpdateTrafoItemView(ComercialFinanzasMixin, UpdateView):
    template_name = "COMERCIAL/sales/crear-item.html"
    model = Items
    form_class = ItemForm

    def get_context_data(self,**kwargs):
        pk = self.kwargs['pk']
        context = super().get_context_data(**kwargs)
        context['pk'] = pk
        return context
    
    def get_success_url(self, *args, **kwargs):
        pk = self.kwargs["pk"]
        item = Items.objects.get(id = pk)
        return reverse_lazy('ventas_app:cotizacion-detalle', kwargs={'pk':item.idTrafoQuote.id})

class DetailTrafoItemView(ComercialFinanzasMixin,DetailView):
    model = Items
    template_name = 'COMERCIAL/sales/detalle-item.html'
    #context_object_name = 'quote'
    
class DeleteTrafoItemView(ComercialFinanzasMixin, DeleteView):
    model = Items
    template_name = 'COMERCIAL/sales/eliminar-item.html'

    def delete(self, request, *args, **kwargs):
        item = self.get_object()
        quote = item.idTrafoQuote
        
        # AÑADIR: Restar del monto total
        quote.amount -= item.unitCost
        quote.save()
        
        return super().delete(request, *args, **kwargs)
    
    def get_success_url(self):
        pk = self.kwargs["pk"]
        item = Items.objects.get(id=pk)
        return reverse_lazy('ventas_app:cotizacion-detalle', kwargs={'pk': item.idTrafoQuote.id})

# ================= IMAGENES ITEMS ========================
class ItemDetailAllListView(ComercialFinanzasMixin, ListView):
    """Listado de imágenes de un item específico"""
    model = ItemImage
    template_name = 'COMERCIAL/sales/item-detail.html'
    context_object_name = 'images'
    
    def get_queryset(self):
        self.item = get_object_or_404(Items, pk=self.kwargs['item_pk'])
        return ItemImage.objects.filter(item=self.item).order_by('order', '-is_main')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item'] = self.item
        return context

class ItemImageCreateView(ComercialFinanzasMixin, CreateView):
    """Agregar una imagen individual"""
    model = ItemImage
    form_class = ItemImageForm
    template_name = 'sales/items/image_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.item = get_object_or_404(Items, pk=self.kwargs['item_pk'])
        # Verificar límite de imágenes
        if self.item.images.count() >= 5:
            messages.error(request, 'Este item ya tiene el máximo de 5 imágenes.')
            return redirect('sales:item_detail', pk=self.item.pk)
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.item = self.item
        messages.success(self.request, 'Imagen agregada exitosamente.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('sales:detail-item-all', kwargs={'pk': self.item.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item'] = self.item
        return context

class ItemImageUpdateView(ComercialFinanzasMixin, UpdateView):
    """Actualizar una imagen existente"""
    model = ItemImage
    form_class = ItemImageForm
    template_name = 'sales/items/image_form.html'
    
    def get_queryset(self):
        return ItemImage.objects.filter(item_id=self.kwargs['item_pk'])
    
    def form_valid(self, form):
        messages.success(self.request, 'Imagen actualizada exitosamente.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('sales:item_detail', kwargs={'pk': self.object.item.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item'] = self.object.item
        return context

class ItemImageDeleteView(ComercialFinanzasMixin, DeleteView):
    """Eliminar una imagen"""
    model = ItemImage
    template_name = 'sales/items/image_confirm_delete.html'
    
    def get_queryset(self):
        return ItemImage.objects.filter(item_id=self.kwargs['item_pk'])
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Imagen eliminada exitosamente.')
        return super().delete(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse('sales:item_detail', kwargs={'pk': self.kwargs['item_pk']})

class ItemMultipleImageUploadView(ComercialFinanzasMixin, FormView):
    """Subir múltiples imágenes a la vez"""
    form_class = MultipleItemImageForm
    template_name = 'COMERCIAL/sales/multiple_image_upload.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.item = get_object_or_404(Items, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['item'] = self.item
        return kwargs
    
    def form_valid(self, form):
        images = self.request.FILES.getlist('images')
        
        if not images:
            messages.warning(self.request, 'No se seleccionaron imágenes.')
            return redirect('sales:item_detail', pk=self.item.pk)
        
        # Verificar límite total
        current_count = self.item.images.count()
        remaining = 5 - current_count
        
        if len(images) > remaining:
            messages.error(
                self.request, 
                f'Solo puedes agregar {remaining} imagen(es) más. '
                f'Actualmente tienes {current_count} imágenes.'
            )
            return self.form_invalid(form)
        
        # Crear las imágenes
        created_count = 0
        for i, image in enumerate(images):
            ItemImage.objects.create(
                item=self.item,
                image=image,
                order=current_count + i
            )
            created_count += 1
        
        messages.success(
            self.request, 
            f'{created_count} imagen(es) agregada(s) exitosamente.'
        )
        return redirect('ventas_app:detalle-item', pk=self.item.pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item'] = self.item
        context['current_count'] = self.item.images.count()
        context['remaining'] = 5 - context['current_count']
        return context

# ================= ACTUALIZAR SEGUIMIENTO ITEMS ========================
class UpdateTrackingItemView(ComercialFinanzasMixin, CreateView):
    template_name = "COMERCIAL/sales/actualizar-estado-item.html"
    model = ItemTracking
    form_class = ItemTrackingForm

    def get_context_data(self,**kwargs):
        pk = self.kwargs['pk']
        context = super().get_context_data(**kwargs)
        context['pk'] = pk
        context['tracking'] = ItemTracking.objects.filter(idItem = pk)
        return context
    
    def get_success_url(self, *args, **kwargs):
        pk = self.kwargs["pk"]
        item = Items.objects.get(id = pk)
        return reverse_lazy('ventas_app:detail-item-all', kwargs={'item_pk':item.id})

# ================= DETAIL ITEMS FOR CLIENT ======================== 

def normalize_serial(serial):
    """
    Normaliza un número de serie para búsqueda:
    - Elimina espacios en blanco
    - Elimina caracteres especiales (/, -, etc.)
    - Convierte a mayúsculas para uniformidad
    """
    if not serial:
        return ''
    # Eliminar espacios
    serial = serial.strip()
    # Eliminar caracteres especiales comunes (/, -, _, etc.)
    serial = re.sub(r'[/\-_\s]+', '', serial)
    # Convertir a mayúsculas para uniformidad
    serial = serial.upper()
    return serial

class DetailSerialNumberView(ListView):
    template_name = "COMERCIAL/sales/detail-serial-number.html"
    context_object_name = 'Items'

    def get_queryset(self):
        order = self.request.GET.get("order", '')
        normalized_order = normalize_serial(order)
        
        payload = {}
        payload["order"] = order
        
        # Filtrar todos los items y normalizar en Python
        all_items = Items.objects.filter(seq__isnull=False)
        matching_items = [
            item for item in all_items 
            if normalize_serial(item.seq) == normalized_order
        ]
        
        payload["tracking"] = matching_items
        
        if matching_items:
            payload["itemTracking"] = ItemTracking.objects.filter(
                idItem__in=[item.id for item in matching_items]
            ).last()
        else:
            payload["itemTracking"] = None
        
        return payload
