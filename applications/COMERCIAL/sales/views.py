from datetime import date, timedelta
import json

from django.contrib import messages
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

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
  Trafos,
  QuoteTracking
)

from applications.cuentas.models import (
  Tin,
)

from applications.clientes.models import (
  Cliente,
)

from .forms import (
  IncomesForm,
  quotesForm,
  TrafoForm,
  TrafoItemForm
  )

TrafosFormSet = inlineformset_factory(quotes, Trafos, form=TrafoForm, extra=1)

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
                cliente = Cliente.objects.filter(ruc=supplier_id).first()

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

class QuoteCreateView(ComercialFinanzasMixin,CreateView):
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
        context['trafos'] = self.object.trafo_Quote.all().order_by("-created")
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
        context['trafos'] = self.object.trafo_Quote.all()
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

# ================= ITEMS ========================
class CreateTrafoItemView(ComercialFinanzasMixin,CreateView):
    model = Trafos
    form_class = TrafoItemForm
    template_name = 'COMERCIAL/sales/crear-item.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs["pk"]
        return context

    def get_success_url(self, **kwargs):
        idOr = self.kwargs["pk"]
        #idTrafo = Trafos.objects.get(id = idOr)
        return reverse_lazy('ventas_app:cotizacion-detalle', kwargs={'pk':idOr})
    
class UpdateTrafoItemView(ComercialFinanzasMixin,UpdateView):
    model = Trafos
    form_class = TrafoForm
    template_name = 'COMERCIAL/sales/editar-item.html'

    def get_success_url(self, **kwargs):
        idOr = self.kwargs["pk"]
        idTrafo = Trafos.objects.get(id = idOr)
        return reverse_lazy('ventas_app:cotizacion-detalle', kwargs={'pk':idTrafo.idTrafoQuote.id})

class DeleteTrafoItemView(ComercialFinanzasMixin,DeleteView):
    model = Trafos
    template_name = 'COMERCIAL/sales/eliminar-item.html'
    #success_url = reverse_lazy('ventas_app:ventas-lista')

    def get_success_url(self, **kwargs):
        idOr = self.kwargs["pk"]
        idTrafo = Trafos.objects.get(id = idOr)
        return reverse_lazy('ventas_app:cotizacion-detalle', kwargs={'pk':idTrafo.idTrafoQuote.id})

class DetailTrafoItemView(ComercialFinanzasMixin,DetailView):
    model = Trafos
    template_name = 'COMERCIAL/sales/detalle-item.html'
    #context_object_name = 'quote'
