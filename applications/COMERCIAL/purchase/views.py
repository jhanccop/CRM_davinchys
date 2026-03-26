from datetime import date, timedelta
from unittest import result

from django.contrib import messages

from applications.users.mixins import (
  AdminPermisoMixin,
  AdminClientsPermisoMixin,
  LoginRequiredMixin,
  ComercialMixin
)
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings as django_settings

from django.shortcuts import redirect
from django.forms import formset_factory, BaseFormSet
from django.db import transaction

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
    FormView,
    View
)

from .models import (
  requirements,
  requirementItems,
  RequestTracking,
  PettyCash,
  PettyCashItems,
  requirementsInvoice,
  requirementsQuotes,
  QuoteSuppliers,
)

from applications.COMERCIAL.sales.models import (
  quotes, IntQuotes,
)
from applications.COMERCIAL.stakeholders.models import supplier as Supplier

from applications.cuentas.models import (
  Tin,
)

from applications.clientes.models import (
  Cliente,
)

from applications.COMERCIAL.stakeholders.models import client

from applications.users.models import User

from applications.FINANCIERA.documentos.models import (
  FinancialDocuments,
)

from .forms import (
  RequirementsForm,
  RequirementItemForm,
  RequestTrackingForm,
  requirementsQuotesForm,
  PettyCashForm,
  PettyCashItemForm,
  PurchaseOrderInvoiceForm,
  requirementsInvoiceForm,
  )

from django.forms import inlineformset_factory

# ==================== DASHBOARD COMERCIAL ====================

class NewQuoteRequirementCreateView(AdminClientsPermisoMixin,CreateView):
    """
        VISTA PARA ADJUNTAR COTIZACIONES
    """
    template_name = "COMERCIAL/requirement/nueva_cotizacion_id.html"
    model = requirementsQuotes
    form_class = requirementsQuotesForm
    success_url = reverse_lazy('compras_app:dashboard')

    def get_context_data(self, **kwargs):
        context = super(NewQuoteRequirementCreateView, self).get_context_data(**kwargs)
        pk = requirements.objects.get(id = self.kwargs['pk'])
        context['pk'] = pk
        return context
    
class NewVoucherRequirementCreateView(AdminClientsPermisoMixin,CreateView):
    """
        VISTA PARA ADJUNTAR VOUCHER
    """
    template_name = "COMERCIAL/requirement/nuevo_voucher_id.html"
    model = requirementsQuotes
    form_class = requirementsQuotesForm
    success_url = reverse_lazy('compras_app:dashboard')

    def get_context_data(self, **kwargs):
        context = super(NewQuoteRequirementCreateView, self).get_context_data(**kwargs)
        pk = requirements.objects.get(id = self.kwargs['pk'])
        context['pk'] = pk
        return context
    

# ==================== REQUERIMIENTOS (MI ESPACIO - PERSONAL) ====================
class MyRequirementListView(LoginRequiredMixin, ListView):
    """Vista personal: muestra solo los requerimientos del usuario logueado"""
    template_name = "COMERCIAL/purchase/mis-requerimientos.html"
    context_object_name = 'documentos'

    def get_queryset(self, **kwargs):
        user = self.request.user
        intervalDate = self.request.GET.get("dateKword", '')
        if not intervalDate or intervalDate == "today":
            intervalDate = str(date.today() - timedelta(days=120)) + " to " + str(date.today())

        payload = {
            "intervalDate": intervalDate,
            "documentation": requirements.objects.ListaRequerimientosPorUsuario(
                intervalo=intervalDate,
                idPetitioner=user.id
            ),
        }
        return payload

# ==================== REQUERIMIENTOS (COMERCIAL - GESTIÓN DE ÁREA) ====================
class RequirementListView(ComercialMixin, ListView):
    """Vista de área: gestión de todos los requerimientos de todos los colaboradores"""
    template_name = "COMERCIAL/purchase/requirement-lista.html"
    context_object_name = 'documentos'

    def get_queryset(self, **kwargs):
        intervalDate = self.request.GET.get("dateKword", '')
        if not intervalDate or intervalDate == "today":
            intervalDate = str(date.today() - timedelta(days=120)) + " to " + str(date.today())

        return {
            "intervalDate": intervalDate,
            "documentation": requirements.objects.ListaRequerimientosForBoss(intervalo=intervalDate),
        }

class BaseRequirementItemFormSet(BaseFormSet):
    """Formset personalizado que pasa el request a cada formulario"""
    
    def get_form_kwargs(self, index):
        """Retorna kwargs para cada formulario individual"""
        kwargs = super().get_form_kwargs(index)
        # Pasamos el request si está disponible
        if hasattr(self, 'request') and self.request:
            kwargs['request'] = self.request
        return kwargs

class RequirementCreateView(LoginRequiredMixin, CreateView):
    model = requirements
    form_class = RequirementsForm
    template_name = 'COMERCIAL/purchase/requirement_form.html'
    success_url = reverse_lazy('compras_app:list_requirement')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            item_formset = RequirementItemFormSet(self.request.POST)
        else:
            item_formset = RequirementItemFormSet()
        
        # Asignamos el request al formset DESPUÉS de crearlo
        item_formset.request = self.request
        context['item_formset'] = item_formset
        
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        item_formset = context['item_formset']
        
        if item_formset.is_valid():
            self.object = form.save()
            
            items_data = []
            for item_form in item_formset:
                if item_form.cleaned_data and not item_form.cleaned_data.get('DELETE', False):
                    items_data.append(item_form.cleaned_data)
            
            # Usamos transaction.on_commit para asegurarnos de que el requerimiento
            # ya está guardado en la base de datos
            transaction.on_commit(lambda: self.create_requirement_items(self.object, items_data))
            
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
    
    def create_requirement_items(self, requirement, items_data):
        for item_data in items_data:
            requirementItems.objects.create(
                idRequirement=requirement,
                quantity=item_data.get('quantity'),
                #currency=item_data.get('currency'),
                price=item_data.get('price'),
                product=item_data.get('product'),
                type=item_data.get('type')
            )

# Creamos el formset para los items
RequirementItemFormSet = formset_factory(
    RequirementItemForm, 
    formset=BaseRequirementItemFormSet, 
    extra=1, 
    can_delete=True,
    can_order=False,
)

# Creamos el inlineformset para los items de requerimiento (para edición)
RequirementItemInlineFormSet = inlineformset_factory(
    requirements,
    requirementItems,
    form=RequirementItemForm,
    extra=0,
    can_delete=True,
)

class RequirementDetailView(LoginRequiredMixin, ListView):
    model = requirements
    template_name = 'COMERCIAL/purchase/requirement-detalle.html'
    context_object_name = 'requirement'
    
    def get_queryset(self, **kwargs):
        pk = self.kwargs['pk']

        result = {}
        result["req"] = requirements.objects.obtenerRequerimientoPorId(pk)
        result["items"] = requirementItems.objects.obtenerTrackingPorIdRequerimiento(pk)
        result["track"] = RequestTracking.objects.obtenerTrackingPorIdRequerimiento(pk)

        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = self.object_list.get('items', [])
        context['has_transformer_items'] = any(
            item.type == requirementItems.TRANSFORMADOR for item in items
        )
        return context

class RequirementEditView(LoginRequiredMixin, UpdateView):
    model = requirements
    form_class = RequirementsForm
    template_name = 'COMERCIAL/purchase/requirement_form.html'
    success_url = reverse_lazy('compras_app:list_requirement')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['item_formset'] = RequirementItemInlineFormSet(self.request.POST, instance=self.object)
        else:
            context['item_formset'] = RequirementItemInlineFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        item_formset = context['item_formset']
        if item_formset.is_valid():
            self.object = form.save()
            item_formset.instance = self.object
            item_formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

class RequirementDeleteView(LoginRequiredMixin,DeleteView):
  template_name = "COMERCIAL/purchase/requirement-eliminar.html"
  model = requirements
  success_url = reverse_lazy('compras_app:list_requirement')

# ============== REQUERIMIENTOS LOGISTICOS =================
class LogisticRequirementListView(LoginRequiredMixin,ListView):
  template_name = "COMERCIAL/purchase/logistic-requirement-lista.html"
  context_object_name = 'documentos'

  def get_queryset(self,**kwargs):
    #compania_id = self.request.session.get('compania_id')
    user = self.request.user

    intervalDate = self.request.GET.get("dateKword", '')
    if intervalDate == "today" or intervalDate =="":
      intervalDate = str(date.today() - timedelta(days = 120)) + " to " + str(date.today())

    documentation = requirements.objects.ListaRequerimientosPorArea(
      intervalo = intervalDate,
      #idArea = user.position
      idArea = user.empleado.departamento.idArea
      )
    
    allDocumentation = []

    isBoss = self.request.user.is_boss
    if isBoss:
        allDocumentation = requirements.objects.ListaRequerimientosForBoss(
        intervalo = intervalDate,
        )

    payload = {}
    payload["intervalDate"] = intervalDate
    payload["documentation"] = documentation
    payload["allDocumentation"] = allDocumentation
    
    return payload

# ==================== ORDENES DE COMPRA ====================
class PurchaseOrderListView(ComercialMixin, ListView):
    """
        VISTA DE ORDENES DE COMPRA PARA AREA DE COMPRAS
    """
    template_name = "COMERCIAL/purchase/orden-compra-lista.html"
    context_object_name = 'documentos'

    def get_queryset(self,**kwargs):
        #compania_id = self.request.session.get('compania_id')
        user = self.request.user

        intervalDate = self.request.GET.get("dateKword", '')
        if intervalDate == "today" or intervalDate =="":
            intervalDate = str(date.today() - timedelta(days = 120)) + " to " + str(date.today())

        documentation = requirements.objects.ListaOrdenesdeCompra(
            intervalo = intervalDate
            )
    
        payload = {}
        payload["intervalDate"] = intervalDate
        payload["documentation"] = documentation
        
        return payload

class PurchaseInvoiceCreateView(AdminClientsPermisoMixin,CreateView):
    """
        VISTA PARA ADJUNTAR FACTURAS O BOLETAS DE VENTA A ORDENES DE COMPRA
    """
    template_name = "COMERCIAL/purchase/crear_compra_id.html"
    model = requirementsInvoice
    form_class = PurchaseOrderInvoiceForm
    success_url = reverse_lazy('compras_app:compras-lista')

    def get_context_data(self, **kwargs):
        context = super(PurchaseInvoiceCreateView, self).get_context_data(**kwargs)
        pk = requirements.objects.get(id = self.kwargs['pk'])
        context['pk'] = pk
        return context

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
    
# ==================== COMPRAS ====================
class PurchaseListView(LoginRequiredMixin,ListView):
  template_name = "COMERCIAL/purchase/compras-lista.html"
  context_object_name = 'documentos'

  def get_queryset(self,**kwargs):
    compania_id = self.request.session.get('compania_id')
    selectedType = self.request.GET.get("DocKword", '')

    intervalDate = self.request.GET.get("dateKword", '')
    if intervalDate == "today" or intervalDate =="":
      intervalDate = str(date.today() - timedelta(days = 120)) + " to " + str(date.today())

    if selectedType == "Todo" or selectedType == None or selectedType =="" :
      selectedType = 5

    documentation = requirementsInvoice.objects.ListaDocumentosPorTipo(
      intervalo = intervalDate,
      tipo = int(selectedType),
      compania_id = compania_id
      )
  
    payload = {}
    payload["intervalDate"] = intervalDate
    payload["selected"] = selectedType
    payload["documentation"] = documentation
    
    return payload

# ==================== TRACKING REQUERIMIENTOS ====================
class RequestTrackingCreateView(LoginRequiredMixin, CreateView):
    template_name = 'COMERCIAL/purchase/request-tracking-crear.html'
    model = RequestTracking
    form_class = RequestTrackingForm
    success_url = reverse_lazy('compras_app:list_requirement')

    def get_context_data(self, **kwargs):
        context = super(RequestTrackingCreateView, self).get_context_data(**kwargs)
        pk = requirements.objects.get(id = self.kwargs['pk'])
        context['pk'] = pk
        return context

# ==================== CAJA CHICA ====================
class PettyCashListView(LoginRequiredMixin,ListView):
  template_name = "COMERCIAL/pettyCash/cajachica-lista.html"
  context_object_name = 'documentos'

  def get_queryset(self,**kwargs):
    #compania_id = self.request.session.get('compania_id')
    user = self.request.user

    intervalDate = self.request.GET.get("dateKword", '')
    if intervalDate == "today" or intervalDate =="":
      intervalDate = str(date.today() - timedelta(days = 120)) + " to " + str(date.today())

    documentation = PettyCash.objects.ListaCajaChicaPorUsuario(
      intervalo = intervalDate,
      idPetitioner = user.id
      )
  
    payload = {}
    payload["intervalDate"] = intervalDate
    payload["documentation"] = documentation
    
    return payload

class PettyCashCreateView(LoginRequiredMixin, CreateView):
    model = PettyCash
    form_class = PettyCashForm
    template_name = 'COMERCIAL/pettyCash/cajachica_form.html'
    success_url = reverse_lazy('compras_app:lista_cajachica')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['item_formset'] = PettyCashItemFormSet(self.request.POST)
        else:
            context['item_formset'] = PettyCashItemFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        item_formset = context['item_formset']
        
        if item_formset.is_valid():
            self.object = form.save()
            
            items_data = []
            for item_form in item_formset:
                if item_form.cleaned_data and not item_form.cleaned_data.get('DELETE', False):
                    items_data.append(item_form.cleaned_data)
            
            # Usamos transaction.on_commit para asegurarnos de que el requerimiento
            # ya está guardado en la base de datos
            transaction.on_commit(lambda: self.create_pettyCash_items(self.object, items_data))
            
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
    
    def create_pettyCash_items(self, pettyCash, items_data):
        for item_data in items_data:
            PettyCashItems.objects.create(
                idPettyCash=pettyCash,
                quantity=item_data.get('quantity'),
                price=item_data.get('price'),
                product=item_data.get('product'),
                category=item_data.get('category')
            )

# Creamos el formset para los items
PettyCashItemFormSet = formset_factory(
    PettyCashItemForm, 
    extra=1, 
    can_delete=True,
    can_order=False
)

class PettyCashDetailView(LoginRequiredMixin, ListView):
    model = PettyCash
    template_name = 'COMERCIAL/pettyCash/cajachica-detalle.html'
    context_object_name = 'requirement'
    
    def get_queryset(self, **kwargs):
        pk = self.kwargs['pk']

        result = {}
        result["req"] = PettyCash.objects.obtenerCajaChicaPorId(pk)
        result["items"] = PettyCashItems.objects.obtenerPettyCashItemsPorId(pk)

        return result

class PettyCashDeleteView(LoginRequiredMixin,DeleteView):
    template_name = "COMERCIAL/pettyCash/eliminar-cajachica.html"
    model = PettyCash
    success_url = reverse_lazy('compras_app:lista_cajachica')

# ==================== DOCUMENTOS ====================

class requirementsInvoiceListView(AdminClientsPermisoMixin,ListView):
  template_name = "COMERCIAL/purchase/compras-lista.html"
  context_object_name = 'documentos'

  def get_queryset(self,**kwargs):
    compania_id = self.request.session.get('compania_id')
    selectedType = self.request.GET.get("DocKword", '')

    intervalDate = self.request.GET.get("dateKword", '')
    if intervalDate == "today" or intervalDate =="":
      intervalDate = str(date.today() - timedelta(days = 120)) + " to " + str(date.today())

    if selectedType == "Todo" or selectedType == None or selectedType =="" :
      selectedType = 5

    documentation = requirementsInvoice.objects.ListaDocumentosPorTipo(
      intervalo = intervalDate,
      tipo = int(selectedType),
      compania_id = compania_id
      )
  
    payload = {}
    payload["intervalDate"] = intervalDate
    payload["selected"] = selectedType
    payload["documentation"] = documentation
    
    return payload

class requirementsInvoiceCreateView(AdminClientsPermisoMixin,CreateView):
  template_name = "COMERCIAL/purchase/compras-nuevo.html"
  model = requirementsInvoice
  form_class = requirementsInvoiceForm
  success_url = reverse_lazy('compras_app:compras-lista')
  
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

class requirementsInvoiceEditView(AdminClientsPermisoMixin,UpdateView):
  template_name = "COMERCIAL/purchase/compras-editar.html"
  model = requirementsInvoice
  form_class =requirementsInvoiceForm
  success_url = reverse_lazy('compras_app:compras-lista')

class requirementsInvoiceDetailView(AdminClientsPermisoMixin,ListView):
  
  template_name = "COMERCIAL/purchase/compras-detalle.html"
  context_object_name = 'doc'
  
  def get_queryset(self,**kwargs):
    pk = self.kwargs['pk']
    payload = {}
    document = requirementsInvoice.objects.DocumentosPorId(id = int(pk))
    payload["document"] = document
    return payload
  
class requirementsInvoiceDeleteView(AdminClientsPermisoMixin,DeleteView):

  template_name = "COMERCIAL/purchase/compras-eliminar.html"
  model = requirementsInvoice
  success_url = reverse_lazy('compras_app:compras-lista')


# ==================== TRANSFORMER KANBAN ====================

class RequirementTransformerKanbanView(ComercialMixin, DetailView):
    """
    Kanban de cotizaciones a proveedores para requerimientos con
    items de tipo TRANSFORMADOR.

    Izquierda: transformadores sin cotización de proveedor asignada.
    Derecha:   columnas de cotizaciones a proveedores (requirementsQuotes).
    Panel superior: IntQuotes del sistema de ventas vinculados vía idItem.
    """
    model = requirements
    template_name = 'COMERCIAL/purchase/transformer-kanban.html'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        req = self.object

        transformer_items = requirementItems.objects.filter(
            idRequirement=req,
            type=requirementItems.TRANSFORMADOR,
        ).select_related('idTrafo', 'idItem', 'idSupplierQuote')

        unassigned = [i for i in transformer_items if i.idSupplierQuote_id is None]

        supplier_quotes = requirementsQuotes.objects.filter(
            idRequirement=req
        ).select_related('idSupplier')

        kanban_columns = []
        for sq in supplier_quotes:
            items = [i for i in transformer_items if i.idSupplierQuote_id == sq.pk]
            total = sum((i.price or 0) * (i.quantity or 1) for i in items)
            kanban_columns.append({
                'quote': sq,
                'items': items,
                'total': total,
            })

        # IntQuotes vinculadas via idItem → idTrafoIntQuote
        linked_intquotes = {}
        for ri in transformer_items:
            if ri.idItem and ri.idItem.idTrafoIntQuote_id:
                iq = ri.idItem.idTrafoIntQuote
                linked_intquotes[iq.pk] = iq

        context.update({
            'req': req,
            'unassigned_items': unassigned,
            'kanban_columns': kanban_columns,
            'total_items': len(transformer_items),
            'unassigned_count': len(unassigned),
            'linked_intquotes': linked_intquotes.values(),
            'suppliers': Supplier.objects.all(),
        })
        return context


class CreateSupplierQuoteColumnAPI(ComercialMixin, CreateView):
    """AJAX: crea una nueva columna de cotización de proveedor en el kanban"""
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        req_pk = kwargs.get('req_pk')
        try:
            req = requirements.objects.get(pk=req_pk)
        except requirements.DoesNotExist:
            return JsonResponse({'error': 'Requerimiento no encontrado'}, status=404)

        supplier_id = request.POST.get('supplier_id')
        description = request.POST.get('description', '')
        currency = request.POST.get('currency', requirementsQuotes.SOLES)

        if not supplier_id:
            return JsonResponse({'error': 'Proveedor requerido'}, status=400)

        sq = requirementsQuotes.objects.create(
            idRequirement=req,
            idSupplier_id=supplier_id,
            shortDescription=description,
            typeCurrency=currency,
        )
        return JsonResponse({
            'success': True,
            'quote_id': sq.pk,
            'supplier_name': str(sq.idSupplier),
            'description': sq.shortDescription or '',
        })


class AssignTransformerItemAPI(ComercialMixin, View):
    """AJAX: asigna o desasigna un item transformador a una cotización de proveedor"""
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        import json
        try:
            data = json.loads(request.body)
        except Exception:
            return JsonResponse({'error': 'JSON inválido'}, status=400)

        item_ids = data.get('item_ids', [])
        quote_id = data.get('quote_id')  # None or '' → unassign

        try:
            items = requirementItems.objects.filter(pk__in=item_ids)
            if quote_id:
                sq = requirementsQuotes.objects.get(pk=quote_id)
                items.update(idSupplierQuote=sq)
            else:
                items.update(idSupplierQuote=None)
        except requirementsQuotes.DoesNotExist:
            return JsonResponse({'error': 'Cotización no encontrada'}, status=404)

        return JsonResponse({'success': True, 'updated': len(item_ids)})


class ApproveSupplierQuoteAPI(ComercialMixin, View):
    """AJAX: aprueba una cotización de proveedor, crea tracking y marca como OC"""
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        quote_pk = kwargs.get('quote_pk')
        try:
            sq = requirementsQuotes.objects.select_related('idRequirement').get(pk=quote_pk)
        except requirementsQuotes.DoesNotExist:
            return JsonResponse({'error': 'Cotización no encontrada'}, status=404)

        sq.is_approved = True
        sq.save(update_fields=['is_approved'])

        req = sq.idRequirement
        if req:
            req.isPurchaseOrder = True
            req.save(update_fields=['isPurchaseOrder'])
            RequestTracking.objects.create(
                idRequirement=req,
                status=RequestTracking.APROBADO,
                area=request.user.area or RequestTracking.COMERCIAL,
            )

        return JsonResponse({
            'success': True,
            'quote_id': sq.pk,
            'supplier': str(sq.idSupplier),
        })


class SendSupplierQuoteEmailView(ComercialMixin, DetailView):
    """
    Envía un correo al proveedor con la cotización aprobada.
    El remitente es el email corporativo de la empresa subsidiaria del usuario.
    """
    model = requirementsQuotes
    template_name = 'COMERCIAL/purchase/supplier-quote-email.html'
    pk_url_kwarg = 'quote_pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sq = self.object
        # Email origen: email corporativo de la compañia del usuario
        company = getattr(getattr(self.request.user, 'empleado', None), 'company', None)
        context['from_email'] = (company.email if company and company.email else
                                  getattr(django_settings, 'DEFAULT_FROM_EMAIL', ''))
        context['to_email'] = sq.idSupplier.email if sq.idSupplier else ''
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        sq = self.object

        to_email = request.POST.get('to_email', '').strip()
        subject = request.POST.get('subject', f'Cotización REQ-{sq.idRequirement_id} – {sq.idSupplier}')
        body = request.POST.get('body', '')

        company = getattr(getattr(request.user, 'empleado', None), 'company', None)
        from_email = (company.email if company and company.email else
                      getattr(django_settings, 'DEFAULT_FROM_EMAIL', ''))

        if not to_email:
            messages.error(request, 'El proveedor no tiene correo registrado.')
            return redirect(request.path)

        try:
            email = EmailMessage(subject=subject, body=body, from_email=from_email, to=[to_email])
            if sq.pdf_file:
                email.attach_file(sq.pdf_file.path)
            email.send()
            messages.success(request, f'Correo enviado a {to_email}')
        except Exception as exc:
            messages.error(request, f'Error al enviar correo: {exc}')

        return redirect(reverse_lazy('compras_app:req-transformer-kanban',
                                     kwargs={'pk': sq.idRequirement_id}))
