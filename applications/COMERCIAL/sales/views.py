from datetime import date, timedelta
import json
import re
import unicodedata
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.shortcuts import render, get_object_or_404, redirect

from django.shortcuts import render

from django.db.models import Count, Sum, Q, Prefetch

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
  ItemTracking,
  IntQuotes,
  WorkOrder
)

from applications.cuentas.models import (
  Tin,
)

from applications.COMERCIAL.stakeholders.models import client, supplier
from applications.PRODUCTION.models import Trafos
from applications.COMERCIAL.sales.models import Items,ItemTracking, ItemImage
from applications.LOGISTICA.transport.models import Container

from .forms import (
  IncomesForm,
  quotesForm,
  IntQuoteForm,
  ItemForm,
  ItemImageForm,
  MultipleItemImageForm,
  ItemTrackingForm,
  trafoForm,
  WorkOrderForm,
  IntQuoteEditForm,
  WorkOrderEditForm
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

class QuoteDetailView(ComercialFinanzasMixin, DetailView):
    model = quotes
    template_name = 'COMERCIAL/sales/quote-detalle.html'
    context_object_name = 'quote'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Items asociados a esta PO/QUO
        items = self.object.item_Quote.all().order_by("-created")
        context['trafos'] = items

        # Tracking de la cotización
        context['tracking'] = QuoteTracking.objects.filter(idquote=self.object)

        # IntQuotes: cotizaciones internas vinculadas a través de los items
        int_quote_ids = items.values_list(
            'idTrafoIntQuote', flat=True
        ).exclude(idTrafoIntQuote__isnull=True).distinct()
        context['int_quotes'] = IntQuotes.objects.filter(
            id__in=int_quote_ids
        ).select_related('idClient', 'idTinReceiving')

        # WorkOrders: órdenes de trabajo vinculadas a través de los items
        wo_ids = items.values_list(
            'idWorkOrder', flat=True
        ).exclude(idWorkOrder__isnull=True).distinct()
        context['work_orders'] = WorkOrder.objects.filter(
            id__in=wo_ids
        ).select_related('idSupplier', 'idTinReceiving')

        return context

class QuoteCreateView(ComercialFinanzasMixin, CreateView):
    model = quotes
    form_class = quotesForm
    template_name = 'COMERCIAL/sales/quote_create.html'
    success_url = reverse_lazy('ventas_app:cotizaciones-lista')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    @transaction.atomic
    def form_valid(self, form):
        try:
            self.object = form.save(commit=False)
            
            items_data = self.request.POST.get('items_data', '[]')
            files_metadata = self.request.POST.get('files_metadata', '{}')
            
            total_amount = 0
            
            import json
            items_list = json.loads(items_data)
            files_metadata_dict = json.loads(files_metadata)
            
            if not items_list:
                form.add_error(None, 'Debe agregar al menos un transformador')
                return self.form_invalid(form)
            
            file_mapping = {}
            for file_id, metadata in files_metadata_dict.items():
                file_mapping[metadata['item_index']] = {
                    'file_id': file_id,
                    'file_name': metadata['file_name']
                }
            
            for index, item_data in enumerate(items_list):
                quantity = int(item_data.get('quantity', 1))
                unit_cost = float(item_data.get('unit_cost', 0))
                total_amount += quantity * unit_cost
            
            self.object.amount = total_amount
            self.object.initialAmount = total_amount
            self.object.save()  # Aquí ya se guarda con idTinReceiving correcto
            
            # ... resto del código igual ...
            for index, item_data in enumerate(items_list):
                quantity = int(item_data.get('quantity', 1))
                unit_cost = float(item_data.get('unit_cost', 0))
                
                drawing_file = None
                if index in file_mapping:
                    file_id = file_mapping[index]['file_id']
                    drawing_file = self.request.FILES.get(file_id)
                
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
                
                base_seq = item_data.get('seq', f'TRAFO-{index+1:03d}')
                
                for i in range(quantity):
                    item_seq = f"{base_seq}-{i+1:03d}" if quantity > 1 else base_seq
                    item = Items.objects.create(
                        idTrafoQuote=self.object,
                        idTrafo=trafo,
                        seq=item_seq,
                        unitCost=unit_cost,
                    )
            
            QuoteTracking.objects.create(
                idquote=self.object,
                status=QuoteTracking.ESPERA,
                area=QuoteTracking.COMERCIAL
            )
            
            if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'redirect_url': str(self.success_url),
                    'message': f'Cotización creada con {len(items_list)} transformador(es)'
                })
            
            messages.success(self.request, f'Cotización creada exitosamente.')
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

class QuoteUpdateView(ComercialFinanzasMixin, UpdateView):
    model = quotes
    form_class = quotesForm
    template_name = 'COMERCIAL/sales/quote-editar.html'
    context_object_name = 'quote'
    success_url = reverse_lazy('ventas_app:cotizaciones-lista')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

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

class TrafoQuoteListView(ComercialFinanzasMixin, ListView):
    """
    Lista de Cotizaciones Master (quotes).
    - Holding: ve TODAS las quotes de todas las companias.
    - Subsidiaria: ve solo las quotes donde idTinReceiving = su compania.
    Incluye resumen de IntQuotes y WorkOrders por cada quote.
    """
    template_name = 'COMERCIAL/sales/lista-cotizaciones.html'
    context_object_name = 'quotes_data'

    def get_queryset(self):
        user = self.request.user
        company = getattr(user, 'empleado', None)
        company_tin = company.company if company else None

        interval_date = self.request.GET.get('dateKword', '')
        if not interval_date or interval_date == 'today':
            start = date.today() - timedelta(days=90)
            end = date.today()
            interval_date = f"{start} to {end}"
        else:
            parts = interval_date.split(' to ')
            if len(parts) == 2:
                start = parts[0].strip()
                end = parts[1].strip()
            else:
                start = date.today() - timedelta(days=90)
                end = date.today()

        q = self.request.GET.get('q', '').strip()

        # Base queryset
        qs = quotes.objects.select_related(
            'idClient', 'idTinReceiving'
        ).prefetch_related(
            Prefetch(
                'item_Quote',
                queryset=Items.objects.select_related(
                    'idTrafo', 'idTrafoIntQuote',
                    'idTrafoIntQuote__idTinReceiving',
                    'idWorkOrder', 'idWorkOrder__idSupplier'
                )
            ),
        ).filter(
            dateOrder__range=[start, end]
        ).order_by('-dateOrder', '-id')

        if q:
            qs = qs.filter(
                Q(idClient__tradeName__icontains=q) |
                Q(poNumber__icontains=q) |
                Q(id__icontains=q)
            )

        # Filtrar por tipo de compania
        if company_tin and company_tin.company_type == Tin.SUBSIDIARY:
            qs = qs.filter(idTinReceiving=company_tin)

        # Annotate counts
        qs = qs.annotate(
            total_items=Count('item_Quote', distinct=True),
            items_with_intquote=Count(
                'item_Quote',
                filter=Q(item_Quote__idTrafoIntQuote__isnull=False),
                distinct=True
            ),
            items_with_wo=Count(
                'item_Quote',
                filter=Q(item_Quote__idWorkOrder__isnull=False),
                distinct=True
            ),
            total_amount_sum=Sum('item_Quote__unitCost'),
        )

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        company = getattr(user, 'empleado', None)
        company_tin = company.company if company else None

        interval_date = self.request.GET.get('dateKword', '')
        if not interval_date or interval_date == 'today':
            start = date.today() - timedelta(days=90)
            end = date.today()
            interval_date = f"{start} to {end}"

        is_holding = (
            company_tin and company_tin.company_type == Tin.HOLDING
        ) if company_tin else False

        qs = context['quotes_data']

        context.update({
            'intervalDate': interval_date,
            'is_holding': is_holding,
            'company_tin': company_tin,
            'total_quotes': qs.count() if hasattr(qs, 'count') else len(qs),
            'q': self.request.GET.get('q', ''),
        })
        return context

class TrafoQuoteListView0(ComercialFinanzasMixin,ListView):
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

# ================= CRUD PLANTILLAS ========================
class TrafoTemplatesListView(ComercialMixin,ListView):
    template_name = "COMERCIAL/sales/plantilla-lista.html"
    context_object_name = 'trafos'

    def get_queryset(self,**kwargs):
        result = Trafo.objects.ListAllDocuments()
        return result

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

class UpdateTrafoItemView0(ComercialFinanzasMixin, UpdateView):
    template_name = "COMERCIAL/sales/crear-item.html"
    model = Items
    form_class = ItemForm

    def get_context_data(self,**kwargs):
        #pk = self.kwargs['pk']
        #print(self.object.idTrafoQuote.id)
        context = super().get_context_data(**kwargs)
        if self.object.idTrafoQuote:
            context['pk'] = self.object.idTrafoQuote.id
        return context
    
    def get_success_url(self, *args, **kwargs):
        pk = self.kwargs["pk"]
        item = Items.objects.get(id = pk)
        return reverse_lazy('ventas_app:cotizacion-detalle', kwargs={'pk':item.idTrafoQuote.id})

class UpdateTrafoItemView(ComercialFinanzasMixin, UpdateView):
    template_name = "COMERCIAL/sales/crear-item.html"
    model = Items
    form_class = ItemForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.idTrafoQuote:
            context['pk'] = self.object.idTrafoQuote.id
        
        # Añadir el form del transformador para edición
        if self.object.idTrafo:
            if self.request.POST:
                context['trafo_form'] = trafoForm(
                    self.request.POST, 
                    self.request.FILES,
                    instance=self.object.idTrafo,
                    prefix='trafo'
                )
            else:
                context['trafo_form'] = trafoForm(
                    instance=self.object.idTrafo,
                    prefix='trafo'
                )
        
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        trafo_form = context.get('trafo_form')
        
        # Validar y guardar el form del transformador si existe
        if trafo_form and trafo_form.is_valid():
            trafo_form.save()
        elif trafo_form:
            return self.form_invalid(form)
        
        return super().form_valid(form)
    
    def get_success_url(self, *args, **kwargs):
        pk = self.kwargs["pk"]
        item = Items.objects.get(id=pk)
        return reverse_lazy('ventas_app:cotizacion-detalle', kwargs={'pk': item.idTrafoQuote.id})

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

# ================= INT ASIGN QUOTES ITEMS ========================
class IntQuoteListView(ComercialFinanzasMixin, ListView):
    """
    Lista de Cotizaciones Internas (IntQuotes).
    - Holding: ve todas las IntQuotes.
    - Subsidiaria: ve solo IntQuotes donde idTinReceiving = su compania.
    """
    template_name = 'COMERCIAL/sales/purhaseOrder/intquote_list.html'
    context_object_name = 'intquotes_data'

    def get_queryset(self):
        user = self.request.user
        company = getattr(user, 'empleado', None)
        company_tin = company.company if company else None

        interval_date = self.request.GET.get('dateKword', '')
        if not interval_date or interval_date == 'today':
            start = date.today() - timedelta(days=90)
            end = date.today()
            interval_date = f"{start} to {end}"
        else:
            parts = interval_date.split(' to ')
            if len(parts) == 2:
                start = parts[0].strip()
                end = parts[1].strip()
            else:
                start = date.today() - timedelta(days=90)
                end = date.today()

        q = self.request.GET.get('q', '').strip()

        qs = IntQuotes.objects.select_related(
            'idClient', 'idTinReceiving'
        ).prefetch_related(
            Prefetch(
                'item_IntQuote',
                queryset=Items.objects.select_related(
                    'idTrafo', 'idWorkOrder', 'idWorkOrder__idSupplier'
                )
            ),
        ).filter(
            dateOrder__range=[start, end]
        ).order_by('-dateOrder', '-id')

        if q:
            qs = qs.filter(
                Q(idClient__tradeName__icontains=q) |
                Q(poNumber__icontains=q) |
                Q(id__icontains=q)
            )

        if company_tin and company_tin.company_type == Tin.SUBSIDIARY:
            qs = qs.filter(idTinReceiving=company_tin)

        qs = qs.annotate(
            total_items=Count('item_IntQuote', distinct=True),
            items_with_wo=Count(
                'item_IntQuote',
                filter=Q(item_IntQuote__idWorkOrder__isnull=False),
                distinct=True
            ),
        )

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        company = getattr(user, 'empleado', None)
        company_tin = company.company if company else None

        interval_date = self.request.GET.get('dateKword', '')
        if not interval_date or interval_date == 'today':
            start = date.today() - timedelta(days=90)
            end = date.today()
            interval_date = f"{start} to {end}"

        is_holding = (
            company_tin and company_tin.company_type == Tin.HOLDING
        ) if company_tin else False

        context.update({
            'intervalDate': interval_date,
            'is_holding': is_holding,
            'company_tin': company_tin,
            'q': self.request.GET.get('q', ''),
        })
        return context

class QuoteKanbanView(ComercialFinanzasMixin,DetailView):
    """
    Vista Kanban para gestionar la asignación de items a cotizaciones internas.
    
    - Lado izquierdo: items sin asignar (pertenecientes a la quote master).
    - Lado derecho: columnas de IntQuotes con sus items asignados.
    - Drag & drop para mover items entre columnas.
    """
    model = quotes
    template_name = 'COMERCIAL/sales/agisnar_po_intermedio.html'
    context_object_name = 'quote'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quote = self.object

        # Items sin asignar a ninguna IntQuote
        unassigned_items = Items.objects.filter(
            idTrafoQuote=quote,
            idTrafoIntQuote__isnull=True
        ).select_related('idTrafo')

        # Items ya asignados (agrupados por IntQuote)
        assigned_items = Items.objects.filter(
            idTrafoQuote=quote,
            idTrafoIntQuote__isnull=False
        ).select_related('idTrafo', 'idTrafoIntQuote', 'idTrafoIntQuote__idTinReceiving')

        # IntQuotes que tienen items de esta quote
        int_quote_ids = assigned_items.values_list(
            'idTrafoIntQuote_id', flat=True
        ).distinct()
        int_quotes = IntQuotes.objects.filter(
            id__in=int_quote_ids
        ).select_related('idTinReceiving', 'idClient')

        # Construir estructura de columnas para el kanban
        kanban_columns = []
        for iq in int_quotes:
            iq_items = assigned_items.filter(idTrafoIntQuote=iq)
            kanban_columns.append({
                'int_quote': iq,
                'items': iq_items,
                'total': sum(
                    item.unitCostInt or Decimal('0')
                    for item in iq_items
                ),
            })

        # Todos los items de la quote (para referencia)
        all_items = Items.objects.filter(
            idTrafoQuote=quote
        ).select_related('idTrafo')

        # Formulario para crear nueva IntQuote
        form = IntQuoteForm(quote=quote)

        # Compañías TIN disponibles
        tins = Tin.objects.all()

        context.update({
            'unassigned_items': unassigned_items,
            'kanban_columns': kanban_columns,
            'all_items': all_items,
            'int_quotes': int_quotes,
            'form': form,
            'tins': tins,
            'total_items': all_items.count(),
            'unassigned_count': unassigned_items.count(),
        })
        return context

class CreateIntQuoteAPI(ComercialFinanzasMixin,View):
    """
    API endpoint para crear una nueva IntQuote desde el Kanban.
    Retorna JSON con los datos de la IntQuote creada.
    """

    def post(self, request, quote_pk):
        quote = get_object_or_404(quotes, pk=quote_pk)

        form = IntQuoteForm(request.POST, quote=quote)
        if form.is_valid():
            int_quote = form.save()
            return JsonResponse({
                'success': True,
                'int_quote': {
                    'id': int_quote.id,
                    'tin_name': str(int_quote.idTinReceiving) if int_quote.idTinReceiving else '—',
                    'currency': int_quote.get_currency_display() if int_quote.currency else '—',
                    'po_number': int_quote.poNumber or '—',
                    'pay_method': int_quote.get_payMethod_display() if int_quote.payMethod else '—',
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors,
            }, status=400)

class AssignItemsAPI(ComercialFinanzasMixin,View):
    """
    API endpoint para asignar/mover items entre IntQuotes (drag & drop).
    
    Recibe JSON:
    {
        "assignments": [
            {
                "item_id": 123,
                "int_quote_id": 45 | null,  (null = desasignar / volver a sin asignar)
                "unit_cost_int": "150.00"
            },
            ...
        ]
    }
    """

    def post(self, request, quote_pk):
        quote = get_object_or_404(quotes, pk=quote_pk)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'JSON inválido'
            }, status=400)

        assignments = data.get('assignments', [])
        updated_items = []
        errors = []

        for assignment in assignments:
            item_id = assignment.get('item_id')
            int_quote_id = assignment.get('int_quote_id')  # None = desasignar
            unit_cost_int = assignment.get('unit_cost_int')

            try:
                item = Items.objects.get(id=item_id, idTrafoQuote=quote)
            except Items.DoesNotExist:
                errors.append(f'Item {item_id} no encontrado en esta cotización.')
                continue

            # Asignar o desasignar IntQuote
            if int_quote_id is not None:
                try:
                    int_quote = IntQuotes.objects.get(id=int_quote_id)
                    item.idTrafoIntQuote = int_quote
                except IntQuotes.DoesNotExist:
                    errors.append(f'IntQuote {int_quote_id} no encontrada.')
                    continue
            else:
                item.idTrafoIntQuote = None
                item.unitCostInt = None

            # Actualizar costo unitario interno
            if unit_cost_int is not None and int_quote_id is not None:
                try:
                    item.unitCostInt = Decimal(str(unit_cost_int))
                except (InvalidOperation, ValueError):
                    errors.append(f'Costo inválido para item {item_id}.')
                    continue

            item.save(update_fields=['idTrafoIntQuote', 'unitCostInt'])
            updated_items.append(item.id)

        # Recalcular montos de IntQuotes afectadas
        affected_iq_ids = set()
        for assignment in assignments:
            iq_id = assignment.get('int_quote_id')
            if iq_id:
                affected_iq_ids.add(iq_id)

        for iq_id in affected_iq_ids:
            self._recalculate_int_quote(iq_id)

        return JsonResponse({
            'success': True,
            'updated_items': updated_items,
            'errors': errors,
        })

    def _recalculate_int_quote(self, int_quote_id):
        """Recalcula el monto total de una IntQuote basándose en sus items"""
        try:
            int_quote = IntQuotes.objects.get(id=int_quote_id)
            items = Items.objects.filter(idTrafoIntQuote=int_quote)
            total = sum(
                item.unitCostInt or Decimal('0')
                for item in items
            )
            int_quote.amount = total
            int_quote.save(update_fields=['amount'])
        except IntQuotes.DoesNotExist:
            pass

class DeleteIntQuoteAPI(ComercialFinanzasMixin,View):
    """
    API endpoint para eliminar una IntQuote.
    Los items asignados vuelven a 'sin asignar'.
    """

    def post(self, request, int_quote_pk):
        int_quote = get_object_or_404(IntQuotes, pk=int_quote_pk)

        # Desasignar todos los items de esta IntQuote
        Items.objects.filter(
            idTrafoIntQuote=int_quote
        ).update(idTrafoIntQuote=None, unitCostInt=None)

        int_quote.delete()

        return JsonResponse({'success': True})

class UpdateItemCostAPI(ComercialFinanzasMixin,View):
    """
    API endpoint para actualizar el costo unitario interno de un item.
    """

    def post(self, request, item_pk):
        item = get_object_or_404(Items, pk=item_pk)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'JSON inválido'
            }, status=400)

        unit_cost_int = data.get('unit_cost_int')
        if unit_cost_int is not None:
            try:
                item.unitCostInt = Decimal(str(unit_cost_int))
                item.save(update_fields=['unitCostInt'])
            except (InvalidOperation, ValueError):
                return JsonResponse({
                    'success': False,
                    'error': 'Valor de costo inválido'
                }, status=400)

        # Recalcular IntQuote si existe
        if item.idTrafoIntQuote:
            iq = item.idTrafoIntQuote
            items = Items.objects.filter(idTrafoIntQuote=iq)
            iq.amount = sum(i.unitCostInt or Decimal('0') for i in items)
            iq.save(update_fields=['amount'])

        return JsonResponse({
            'success': True,
            'new_cost': str(item.unitCostInt),
        })

class IntQuoteDetailView(ComercialFinanzasMixin, DetailView):
    """Vista de detalle de Cotizacion Interna"""
    model = IntQuotes
    template_name = 'COMERCIAL/sales/purhaseOrder/intquote_detail.html'
    context_object_name = 'int_quote'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        iq = self.object

        all_items = Items.objects.filter(
            idTrafoIntQuote=iq
        ).select_related(
            'idTrafo', 'idTrafoQuote', 'idWorkOrder',
            'idWorkOrder__idSupplier'
        )

        unassigned_items = all_items.filter(idWorkOrder__isnull=True)
        assigned_items = all_items.filter(idWorkOrder__isnull=False)

        wo_ids = assigned_items.values_list(
            'idWorkOrder_id', flat=True
        ).distinct()
        work_orders = WorkOrder.objects.filter(
            id__in=wo_ids
        ).select_related('idSupplier', 'idTinReceiving')

        wo_groups = []
        for wo in work_orders:
            wo_items = assigned_items.filter(idWorkOrder=wo)
            wo_groups.append({
                'work_order': wo,
                'items': wo_items,
                'total': sum(
                    item.unitCostWO or Decimal('0')
                    for item in wo_items
                ),
                'count': wo_items.count(),
            })

        quote_master = None
        first_item = all_items.first()
        if first_item and first_item.idTrafoQuote:
            quote_master = first_item.idTrafoQuote

        total_cost_int = sum(
            item.unitCostInt or Decimal('0') for item in all_items
        )
        total_cost_wo = sum(
            item.unitCostWO or Decimal('0') for item in assigned_items
        )

        context.update({
            'all_items': all_items,
            'unassigned_items': unassigned_items,
            'assigned_items': assigned_items,
            'work_orders': work_orders,
            'wo_groups': wo_groups,
            'quote_master': quote_master,
            'total_items': all_items.count(),
            'unassigned_count': unassigned_items.count(),
            'assigned_count': assigned_items.count(),
            'total_cost_int': total_cost_int,
            'total_cost_wo': total_cost_wo,
            'wo_count': work_orders.count(),
        })
        return context

class IntQuoteEditView(ComercialFinanzasMixin, UpdateView):
    """Vista de edicion de Cotizacion Interna"""
    model = IntQuotes
    form_class = IntQuoteEditForm
    template_name = 'COMERCIAL/sales/purhaseOrder/intquote_edit.html'
    context_object_name = 'int_quote'

    def get_success_url(self):
        return reverse(
            'ventas_app:intquote-detail',
            kwargs={'pk': self.object.pk}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        first_item = Items.objects.filter(
            idTrafoIntQuote=self.object
        ).select_related('idTrafoQuote').first()
        if first_item and first_item.idTrafoQuote:
            context['quote_master'] = first_item.idTrafoQuote
        return context


# ================= INTQUOTES TO WO ITEMS ========================
class WorkOrderListView(ComercialFinanzasMixin, ListView):
    """
    Lista de Ordenes de Trabajo (WorkOrder).
    - Holding: ve todas las WO.
    - Subsidiaria: ve solo WO donde idTinReceiving = su compania.
    """
    template_name = 'COMERCIAL/sales/workOrder/workorder_list.html'
    context_object_name = 'workorders_data'

    def get_queryset(self):
        user = self.request.user
        company = getattr(user, 'empleado', None)
        company_tin = company.company if company else None

        interval_date = self.request.GET.get('dateKword', '')
        if not interval_date or interval_date == 'today':
            start = date.today() - timedelta(days=90)
            end = date.today()
            interval_date = f"{start} to {end}"
        else:
            parts = interval_date.split(' to ')
            if len(parts) == 2:
                start = parts[0].strip()
                end = parts[1].strip()
            else:
                start = date.today() - timedelta(days=90)
                end = date.today()

        q = self.request.GET.get('q', '').strip()

        qs = WorkOrder.objects.select_related(
            'idSupplier', 'idTinReceiving'
        ).prefetch_related(
            Prefetch(
                'item_WorkOrder',
                queryset=Items.objects.select_related(
                    'idTrafo', 'idTrafoIntQuote'
                )
            ),
        ).filter(
            dateOrder__range=[start, end]
        ).order_by('-dateOrder', '-id')

        if q:
            qs = qs.filter(
                Q(idSupplier__tradeName__icontains=q) |
                Q(woNumber__icontains=q) |
                Q(id__icontains=q)
            )

        if company_tin and company_tin.company_type == Tin.SUBSIDIARY:
            qs = qs.filter(idTinReceiving=company_tin)

        qs = qs.annotate(
            total_items=Count('item_WorkOrder', distinct=True),
        )

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        company = getattr(user, 'empleado', None)
        company_tin = company.company if company else None

        interval_date = self.request.GET.get('dateKword', '')
        if not interval_date or interval_date == 'today':
            start = date.today() - timedelta(days=90)
            end = date.today()
            interval_date = f"{start} to {end}"

        is_holding = (
            company_tin and company_tin.company_type == Tin.HOLDING
        ) if company_tin else False

        context.update({
            'intervalDate': interval_date,
            'is_holding': is_holding,
            'company_tin': company_tin,
            'q': self.request.GET.get('q', ''),
        })
        return context

class IntQuoteWOView(ComercialFinanzasMixin,DetailView):
    """
    Vista Kanban para gestionar la asignación de items de una IntQuote
    hacia WorkOrders (órdenes de trabajo a proveedores).
    
    - Lado izquierdo: items de la IntQuote sin WorkOrder asignada.
    - Lado derecho: columnas de WorkOrders con sus items asignados.
    - Drag & drop para mover items entre columnas.
    """
    model = IntQuotes
    template_name = 'COMERCIAL/sales/workOrder/asignar_wo_proveedor.html'
    context_object_name = 'int_quote'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        int_quote = self.object

        # Items de esta IntQuote sin WorkOrder asignada
        unassigned_items = Items.objects.filter(
            idTrafoIntQuote=int_quote,
            idWorkOrder__isnull=True
        ).select_related('idTrafo', 'idTrafoQuote')

        # Items de esta IntQuote ya asignados a alguna WorkOrder
        assigned_items = Items.objects.filter(
            idTrafoIntQuote=int_quote,
            idWorkOrder__isnull=False
        ).select_related('idTrafo', 'idTrafoQuote', 'idWorkOrder', 'idWorkOrder__idSupplier', 'idWorkOrder__idTinReceiving')

        # WorkOrders que tienen items de esta IntQuote
        wo_ids = assigned_items.values_list(
            'idWorkOrder_id', flat=True
        ).distinct()
        work_orders = WorkOrder.objects.filter(
            id__in=wo_ids
        ).select_related('idSupplier', 'idTinReceiving')

        # Construir estructura de columnas para el kanban
        kanban_columns = []
        for wo in work_orders:
            wo_items = assigned_items.filter(idWorkOrder=wo)
            kanban_columns.append({
                'work_order': wo,
                'items': wo_items,
                'total': sum(
                    item.unitCostWO or Decimal('0')
                    for item in wo_items
                ),
            })

        # Todos los items de la IntQuote
        all_items = Items.objects.filter(
            idTrafoIntQuote=int_quote
        ).select_related('idTrafo')

        # Proveedores y TINs disponibles
        suppliers = supplier.objects.all()
        tins = Tin.objects.all()

        # Quote master (para mostrar referencia)
        # Obtenemos la quote master desde cualquier item
        quote_master = None
        first_item = all_items.first()
        if first_item and first_item.idTrafoQuote:
            quote_master = first_item.idTrafoQuote

        context.update({
            'unassigned_items': unassigned_items,
            'kanban_columns': kanban_columns,
            'all_items': all_items,
            'work_orders': work_orders,
            'suppliers': suppliers,
            'tins': tins,
            'quote_master': quote_master,
            'total_items': all_items.count(),
            'unassigned_count': unassigned_items.count(),
        })
        return context

class CreateWorkOrderAPI(View):
    """
    API endpoint para crear una nueva WorkOrder desde el Kanban de IntQuote.
    Retorna JSON con los datos de la WorkOrder creada.
    """

    def post(self, request, int_quote_pk):
        int_quote = get_object_or_404(IntQuotes, pk=int_quote_pk)

        form = WorkOrderForm(request.POST, int_quote=int_quote)
        if form.is_valid():
            work_order = form.save()
            return JsonResponse({
                'success': True,
                'work_order': {
                    'id': work_order.id,
                    'supplier_name': str(work_order.idSupplier) if work_order.idSupplier else '—',
                    'tin_name': str(work_order.idTinReceiving) if work_order.idTinReceiving else '—',
                    'currency': work_order.get_currency_display() if work_order.currency else '—',
                    'wo_number': work_order.woNumber or '—',
                    'pay_method': work_order.get_payMethod_display() if work_order.payMethod else '—',
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors,
            }, status=400)

class AssignItemsToWOAPI(View):
    """
    API endpoint para asignar/mover items entre WorkOrders (drag & drop).
    
    Recibe JSON:
    {
        "assignments": [
            {
                "item_id": 123,
                "work_order_id": 45 | null,  (null = desasignar)
                "unit_cost_wo": "150.00"
            },
            ...
        ]
    }
    """

    def post(self, request, int_quote_pk):
        int_quote = get_object_or_404(IntQuotes, pk=int_quote_pk)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'JSON inválido'
            }, status=400)

        assignments = data.get('assignments', [])
        updated_items = []
        errors = []

        for assignment in assignments:
            item_id = assignment.get('item_id')
            work_order_id = assignment.get('work_order_id')
            unit_cost_wo = assignment.get('unit_cost_wo')

            try:
                item = Items.objects.get(id=item_id, idTrafoIntQuote=int_quote)
            except Items.DoesNotExist:
                errors.append(f'Item {item_id} no encontrado en esta cotización interna.')
                continue

            # Asignar o desasignar WorkOrder
            if work_order_id is not None:
                try:
                    work_order = WorkOrder.objects.get(id=work_order_id)
                    item.idWorkOrder = work_order
                except WorkOrder.DoesNotExist:
                    errors.append(f'WorkOrder {work_order_id} no encontrada.')
                    continue
            else:
                item.idWorkOrder = None
                item.unitCostWO = None

            # Actualizar costo unitario WO
            if unit_cost_wo is not None and work_order_id is not None:
                try:
                    item.unitCostWO = Decimal(str(unit_cost_wo))
                except (InvalidOperation, ValueError):
                    errors.append(f'Costo inválido para item {item_id}.')
                    continue

            item.save(update_fields=['idWorkOrder', 'unitCostWO'])
            updated_items.append(item.id)

        # Recalcular montos de WorkOrders afectadas
        affected_wo_ids = set()
        for assignment in assignments:
            wo_id = assignment.get('work_order_id')
            if wo_id:
                affected_wo_ids.add(wo_id)

        for wo_id in affected_wo_ids:
            self._recalculate_work_order(wo_id)

        return JsonResponse({
            'success': True,
            'updated_items': updated_items,
            'errors': errors,
        })

    def _recalculate_work_order(self, work_order_id):
        """Recalcula el monto total de una WorkOrder basándose en sus items"""
        try:
            wo = WorkOrder.objects.get(id=work_order_id)
            items = Items.objects.filter(idWorkOrder=wo)
            total = sum(
                item.unitCostWO or Decimal('0')
                for item in items
            )
            wo.amount = total
            wo.save(update_fields=['amount'])
        except WorkOrder.DoesNotExist:
            pass

class DeleteWorkOrderAPI(View):
    """
    API endpoint para eliminar una WorkOrder.
    Los items asignados vuelven a 'sin asignar WO'.
    """

    def post(self, request, wo_pk):
        work_order = get_object_or_404(WorkOrder, pk=wo_pk)

        # Desasignar todos los items de esta WorkOrder
        Items.objects.filter(
            idWorkOrder=work_order
        ).update(idWorkOrder=None, unitCostWO=None)

        work_order.delete()

        return JsonResponse({'success': True})

class UpdateItemCostWOAPI(View):
    """
    API endpoint para actualizar el costo unitario WO de un item.
    """

    def post(self, request, item_pk):
        item = get_object_or_404(Items, pk=item_pk)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'JSON inválido'
            }, status=400)

        unit_cost_wo = data.get('unit_cost_wo')
        if unit_cost_wo is not None:
            try:
                item.unitCostWO = Decimal(str(unit_cost_wo))
                item.save(update_fields=['unitCostWO'])
            except (InvalidOperation, ValueError):
                return JsonResponse({
                    'success': False,
                    'error': 'Valor de costo inválido'
                }, status=400)

        # Recalcular WorkOrder si existe
        if item.idWorkOrder:
            wo = item.idWorkOrder
            items = Items.objects.filter(idWorkOrder=wo)
            wo.amount = sum(i.unitCostWO or Decimal('0') for i in items)
            wo.save(update_fields=['amount'])

        return JsonResponse({
            'success': True,
            'new_cost': str(item.unitCostWO),
        })

# ================= WORKORDERS ========================
class WorkOrderDetailView(DetailView):
    """Vista de detalle de Orden de Trabajo"""
    model = WorkOrder
    template_name = 'COMERCIAL/sales/workOrder/workorder_detail.html'
    context_object_name = 'work_order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wo = self.object

        # Items asignados a esta WorkOrder
        all_items = Items.objects.filter(
            idWorkOrder=wo
        ).select_related(
            'idTrafo', 'idTrafoQuote', 'idTrafoIntQuote',
            'idTrafoIntQuote__idTinReceiving'
        )

        # Totales
        total_cost_wo = sum(
            item.unitCostWO or Decimal('0') for item in all_items
        )
        total_cost_int = sum(
            item.unitCostInt or Decimal('0') for item in all_items
        )
        total_cost_client = sum(
            item.unitCost or Decimal('0') for item in all_items
        )

        # IntQuotes asociadas (los items pueden venir de distintas IntQuotes)
        iq_ids = all_items.values_list(
            'idTrafoIntQuote_id', flat=True
        ).distinct()
        int_quotes = IntQuotes.objects.filter(
            id__in=iq_ids
        ).select_related('idTinReceiving', 'idClient')

        # Agrupado por IntQuote
        iq_groups = []
        for iq in int_quotes:
            iq_items = all_items.filter(idTrafoIntQuote=iq)
            iq_groups.append({
                'int_quote': iq,
                'items': iq_items,
                'total': sum(
                    item.unitCostWO or Decimal('0')
                    for item in iq_items
                ),
                'count': iq_items.count(),
            })

        # Quote master
        quote_master = None
        first_item = all_items.first()
        if first_item and first_item.idTrafoQuote:
            quote_master = first_item.idTrafoQuote

        # IntQuote principal (la primera)
        int_quote_ref = int_quotes.first() if int_quotes.exists() else None

        # Margen: diferencia entre costo interno y costo OT
        margin = total_cost_int - total_cost_wo

        context.update({
            'all_items': all_items,
            'total_items': all_items.count(),
            'total_cost_wo': total_cost_wo,
            'total_cost_int': total_cost_int,
            'total_cost_client': total_cost_client,
            'margin': margin,
            'int_quotes': int_quotes,
            'iq_groups': iq_groups,
            'quote_master': quote_master,
            'int_quote_ref': int_quote_ref,
        })
        return context

class WorkOrderEditView(UpdateView):
    """Vista de edicion de Orden de Trabajo"""
    model = WorkOrder
    form_class = WorkOrderEditForm
    template_name = 'COMERCIAL/sales/workOrder/workorder_edit.html'
    context_object_name = 'work_order'

    def get_success_url(self):
        return reverse(
            'ventas_app:workorder-detail',
            kwargs={'pk': self.object.pk}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Breadcrumb references
        first_item = Items.objects.filter(
            idWorkOrder=self.object
        ).select_related(
            'idTrafoQuote', 'idTrafoIntQuote'
        ).first()
        if first_item:
            if first_item.idTrafoQuote:
                context['quote_master'] = first_item.idTrafoQuote
            if first_item.idTrafoIntQuote:
                context['int_quote_ref'] = first_item.idTrafoIntQuote
        return context



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

class TransformerSearchView(View):
    template_name = "COMERCIAL/sales/transformer-search.html"

    def get(self, request):
        query = request.GET.get("order", "").strip()

        payload = {
            "query": query,
            "results": [],
            "not_found": False,
        }

        if not query:
            return render(request, self.template_name, {"payload": payload})

        normalized = normalize_serial(query)

        # 1. IDs de quotes que coinciden por poNumber
        matching_quote_ids = list(
            quotes.objects.filter(
                poNumber__icontains=query
            ).values_list('id', flat=True)
        )

        # 2. IDs de containers que coinciden por nombre
        matching_container_ids = list(
            Container.objects.filter(
                containerName__icontains=query
            ).values_list('id', flat=True)
        )

        # 3. Traer todos los items candidatos de BD
        qs = Items.objects.select_related(
            'idTrafoQuote', 'idTrafo', 'idContainer'
        ).filter(
            Q(idTrafoQuote__id__in=matching_quote_ids) |
            Q(idContainer__id__in=matching_container_ids) |
            Q(seq__isnull=False)
        ).distinct()

        # 4. Filtrar en Python (serial normalizado + los que ya coinciden por PO/container)
        results = []
        seen_ids = set()

        for item in qs:
            if item.id in seen_ids:
                continue
            match_serial = normalize_serial(item.seq) == normalized
            match_po = item.idTrafoQuote_id in matching_quote_ids
            match_container = item.idContainer_id in matching_container_ids

            if match_serial or match_po or match_container:
                results.append(item)
                seen_ids.add(item.id)

        # 5. Obtener último tracking por item
        trackings_map = {}
        if results:
            trackings_qs = ItemTracking.objects.filter(
                idItem__in=[i.id for i in results]
            ).order_by('idItem_id', '-created')

            for t in trackings_qs:
                if t.idItem_id not in trackings_map:
                    trackings_map[t.idItem_id] = t

        # 6. Combinar item + tracking en una sola lista
        payload["results"] = [
            {"item": item, "tracking": trackings_map.get(item.id)}
            for item in results
        ]
        payload["not_found"] = len(results) == 0

        return render(request, self.template_name, {"payload": payload})

class TransformerItemDetailView(DetailView):
    model = Items
    template_name = "COMERCIAL/sales/transformer-detail.html"
    context_object_name = 'item'
    pk_url_kwarg = 'pk'

    def get_queryset(self):
        return Items.objects.select_related(
            'idTrafoQuote', 'idTrafo', 'idContainer'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['itemTracking'] = ItemTracking.objects.filter(
            idItem=self.object.id
        ).last()
        context['back_query'] = self.request.GET.get('q', '')
        return context

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
