from datetime import date, timedelta

from csv import DictReader
from io import TextIOWrapper
import pandas as pd

from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages

from django.views.generic.edit import ModelFormMixin

from applications.users.mixins import (
  AdminPermisoMixin,
  AdminClientsPermisoMixin, # Adquisiciones, Finanzas, Tesoreria, contabilidad y administrador
  ContabilidadPermisoMixin,
  ComprasContabilidadPermisoMixin
)

from django.views.generic import (
    DetailView,
    DeleteView,
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    View
)

from .models import (
  DocumentsUploaded,
  BankMovements,
  Documents,

  Transactions,
  InternalTransfers,
  Conciliation
)

from applications.cuentas.models import Account

from .forms import (
  InternalTransfersForm,
  BankMovementsForm,
  UploadFileForm,
  ConciliationDocumentsForm,
  ConciliationBankMovementsForm,
  
  DocumentsForm,
  DocReconciliationUpdateForm,
  ConciliationMovDocForm,
  ConciliationMovMovForm,
  EditConciliationMovMovForm,
  EditConciliationMovDocForm
  #BankReconciliationUpdateForm
)

class MainReport(AdminPermisoMixin,ListView):
  template_name = "movimientos/reporte-principal.html"
  context_object_name = 'general'
  
  def get_queryset(self):
    intervalDate = self.request.GET.get("dateKword", '')
    if intervalDate == "today" or intervalDate =="":
      intervalDate = str(date.today() - timedelta(days = 7)) + " to " + str(date.today())
    
    payload = {}
    payload["intervalDate"] = intervalDate
    payload["movimientos"] = Transactions.objects.SaldosGeneralPorIntervalo(intervalo = intervalDate)
    
    return payload

class ListAccount(AdminPermisoMixin,ListView):
  template_name = "movimientos/reporte-cuentas.html"
  context_object_name = 'cuentas'

  def get_queryset(self):
    payload = {}
    payload['cuenta'] = Account.objects.CuentasByCajaChica(cajaChica = False)

    return payload

class AccountDetail(AdminPermisoMixin,ListView):
  template_name = "movimientos/reporte-cuentas-detalle.html"
  context_object_name = 'cuenta'

  def get_queryset(self,**kwargs):
    pk = self.kwargs['pk']
    intervalDate = self.request.GET.get("dateKword", '')
    if intervalDate == "today" or intervalDate =="":
      intervalDate = str(date.today() - timedelta(days = 7)) + " to " + str(date.today())

    payload = {}
    payload["intervalDate"] = intervalDate
    payload["datos"] = Transactions.objects.ReportePorCuenta(intervalo = intervalDate, cuenta = int(pk)) # 1:dolares

    return payload

class AccountReport(AdminPermisoMixin,ListView):
  template_name = "movimientos/reporte-cuentas.html"
  context_object_name = 'cuentas'
  
  def get_queryset(self):
    intervalDate = self.request.GET.get("dateKword", '')
    if intervalDate == "today" or intervalDate =="":
      intervalDate = str(date.today())
    
    payload = {}
    payload["intervalDate"] = intervalDate
    payload["PEN"] = Transactions.objects.ReportePorCuenta_v0(intervalo = intervalDate, moneda = "0", cajaChica = False) # 1:dolares
    payload["DOLLAR"] = Transactions.objects.ReportePorCuenta_v0(intervalo = intervalDate, moneda = "1", cajaChica = False) # 1:dolares
    #payload["DailyResume"] = Transactions.objects.ResumenDiario(intervalDate)

    return payload

class CajaChicaDetail(AdminPermisoMixin,ListView):
  template_name = "movimientos/reporte-cajaChica-detalle.html"
  context_object_name = 'cuenta'

  def get_queryset(self,**kwargs):
    pk = self.kwargs['pk']
    intervalDate = self.request.GET.get("dateKword", '')
    if intervalDate == "today" or intervalDate =="":
      intervalDate = str(date.today() - timedelta(days = 7)) + " to " + str(date.today())

    payload = {}
    payload["intervalDate"] = intervalDate
    payload["datos"] = Transactions.objects.ReportePorCajaChica(intervalo = intervalDate, cuenta = int(pk))

    return payload

class ListCajaChica(ComprasContabilidadPermisoMixin,ListView):
  template_name = "movimientos/reporte-cajaChica.html"
  context_object_name = 'cuentas'

  def get_queryset(self):
    payload = {}
    payload["cuenta"] = Account.objects.CuentasByCajaChica(cajaChica = True)

    
    return payload
  
class CajaChicaReport(ComprasContabilidadPermisoMixin,ListView):
  template_name = "movimientos/reporte-cajaChica.html"
  context_object_name = 'cajaChica'

class TransfersReport(AdminPermisoMixin,ListView):
  template_name = "movimientos/reporte-transferencias.html"
  context_object_name = 'reportePrincipal'

# ================= DOCUMENTACION ========================
class DocumentacionListView(AdminClientsPermisoMixin,ListView):
  template_name = "movimientos/lista-documentos.html"
  context_object_name = 'documentos'

  def get_queryset(self,**kwargs):
      selectedType = self.request.GET.get("DocKword", '')

      intervalDate = self.request.GET.get("dateKword", '')
      if intervalDate == "today" or intervalDate =="":
        intervalDate = str(date.today() - timedelta(days = 120)) + " to " + str(date.today())

      if selectedType == "Todo" or selectedType == None or selectedType =="" :
        selectedType = 5

      documentation = Documents.objects.ListaDocumentosPorTipo(intervalo = intervalDate, tipo = int(selectedType))
   
      payload = {}
      payload["intervalDate"] = intervalDate
      payload["selected"] = selectedType
      payload["documentation"] = documentation
      
      return payload

class DocumentacionCreateView(AdminClientsPermisoMixin,CreateView):
  template_name = "movimientos/crear-documentos.html"
  model = Documents
  form_class = DocumentsForm
  success_url = reverse_lazy('movimientos_app:lista-documentacion')

class DocumentacionEditView(AdminClientsPermisoMixin,UpdateView):
  template_name = "movimientos/editar-documentos.html"
  model = Documents
  form_class = DocumentsForm
  success_url = reverse_lazy('movimientos_app:lista-documentacion')

class DocumentacionDetailView(AdminClientsPermisoMixin,ListView):
  template_name = "movimientos/documentacion-detalle.html"
  context_object_name = 'doc'
  
  def get_queryset(self,**kwargs):
    pk = self.kwargs['pk']
    payload = {}
    document = Documents.objects.DocumentosPorId(id = int(pk))
    payload["document"] = document
    return payload

# ================= MOVIMIENTOS ========================
class MovimientosListView(AdminClientsPermisoMixin,ListView):
  template_name = "movimientos/lista-movimientos.html"
  context_object_name = 'movimientos'

  def get_queryset(self,**kwargs):
    selectedAccount = self.request.GET.get("AccountKword", '')
    intervalDate = self.request.GET.get("dateKword", '')
    if intervalDate == "today" or intervalDate =="":
      intervalDate = str(date.today() - timedelta(days = 30)) + " to " + str(date.today())

    if selectedAccount == "None" or selectedAccount == None or selectedAccount =="" :
      idSelected = Account.objects.CuentasByLastUpdate()
      selectedAccount = idSelected.id # seleccionar por default la primera cuenta

    bankMovements = BankMovements.objects.ListaMovimientosPorCuenta(intervalo = intervalDate, cuenta = int(selectedAccount))
    payload = {}
    payload["intervalDate"] = intervalDate
    payload["selectedAccount"] = Account.objects.CuentasById(int(selectedAccount))
    payload["listAccount"] = Account.objects.listarcuentas()
    payload["lastBalance"] = BankMovements.objects.ObtenerSaldo(cuenta=int(selectedAccount))

    payload["bankMovements"] = bankMovements
    return payload

class MovimientosEditView(AdminClientsPermisoMixin,UpdateView):
  template_name = "movimientos/editar-movimientos.html"
  model = BankMovements
  form_class = BankMovementsForm
  success_url = reverse_lazy('movimientos_app:lista-movimientos')

class MovimientosCreateView(AdminClientsPermisoMixin,CreateView):
  template_name = "movimientos/crear-movimientos.html"
  model = BankMovements
  form_class = BankMovementsForm
  success_url = reverse_lazy('movimientos_app:lista-movimientos')

class MovimientosDeleteView(AdminClientsPermisoMixin,DeleteView):
  template_name = "movimientos/eliminar-movimientos.html"
  model = BankMovements
  success_url = reverse_lazy('movimientos_app:lista-movimientos')
  
class ConciliarMovimientoConDocumentoCreateView(AdminClientsPermisoMixin,CreateView):
  template_name = "movimientos/conciliar-movimiento-con-documento.html"
  model = Conciliation
  form_class = ConciliationMovDocForm

  def get_success_url(self, *args, **kwargs):
    pk = self.kwargs["pk"]
    #return reverse_lazy('movimientos_app:asignar-montos-documento', kwargs={'pk':pk})
    return reverse_lazy('movimientos_app:movimientos-detalle', kwargs={'pk':pk})

  def get_context_data(self, **kwargs):
    context = super(ConciliarMovimientoConDocumentoCreateView, self).get_context_data(**kwargs)
    bankMovement = BankMovements.objects.get(id = self.kwargs['pk'])
    context['mov'] = bankMovement
    context['sum'] = Conciliation.objects.SumaMontosConciliadosPorMovimientosOr(bankMovement.id)
    return context

class ConciliarMovimientoConMovimientoCreateView(AdminClientsPermisoMixin,CreateView):
  template_name = "movimientos/conciliar-movimiento-con-movimiento.html"
  model = Conciliation
  form_class = ConciliationMovMovForm
  #success_url = reverse_lazy('movimientos_app:lista-movimientos')

  def get_success_url(self, *args, **kwargs):
    pk = self.kwargs["pk"]
    #return reverse_lazy('movimientos_app:asignar-montos-documento', kwargs={'pk':pk})
    return reverse_lazy('movimientos_app:movimientos-detalle', kwargs={'pk':pk})


  def get_form_kwargs(self):
    kwargs = super(ConciliarMovimientoConMovimientoCreateView, self).get_form_kwargs()
    kwargs.update({'pk': self.kwargs["pk"]})
    return kwargs

  def get_context_data(self, **kwargs):
    context = super(ConciliarMovimientoConMovimientoCreateView, self).get_context_data(**kwargs)
    bankMovement = BankMovements.objects.get(id = self.kwargs['pk'])
    context['mov'] = bankMovement
    context['sum'] = Conciliation.objects.SumaMontosConciliadosPorMovimientosOr(bankMovement.id)
    return context
 
class EditarMovimientoConMovimientoUpdateView(AdminClientsPermisoMixin,UpdateView):
  template_name = "movimientos/editar-movimiento-con-movimiento.html"
  model = Conciliation
  form_class = EditConciliationMovMovForm

  def get_success_url(self, **kwargs):
    idOr = self.kwargs["pk"]
    idMov = Conciliation.objects.get(id = idOr)
    return reverse_lazy('movimientos_app:movimientos-detalle', kwargs={'pk':idMov.idMovOrigin.id})

class EditarMovimientoConDocumentoUpdateView(AdminClientsPermisoMixin,UpdateView):
  template_name = "movimientos/editar-movimiento-con-documento.html"
  model = Conciliation
  form_class = EditConciliationMovDocForm

  def get_success_url(self, **kwargs):
    idOr = self.kwargs["pk"]
    idMov = Conciliation.objects.get(id = idOr)
    return reverse_lazy('movimientos_app:movimientos-detalle', kwargs={'pk':idMov.idMovOrigin.id})

# ======================= UPDATE DOC ===============================
class MovimientosConciliarUpdateView(AdminClientsPermisoMixin,UpdateView):
  template_name = "movimientos/editar-conciliar-movimientos.html"
  model = Documents
  form_class = DocReconciliationUpdateForm

  def get_success_url(self, *args, **kwargs):
    pk = self.object.idBankMovements.all()[0].id
    return reverse_lazy('movimientos_app:movimientos-detalle', kwargs={'pk':pk})

class MovimientosDetailView(AdminClientsPermisoMixin,ListView):
  template_name = "movimientos/detalle-movimiento.html"
  context_object_name = 'mov'
  def get_queryset(self,**kwargs):
    pk = self.kwargs['pk']
    payload = {}
    bankMovement = BankMovements.objects.MovimientosPorId(id = int(pk))
    #documentation = Documents.objects.ListaConciliacionPorIdMovimiento(bankMovement.id)
    suma = BankMovements.objects.SumaDocsPorId(bankMovement.id)[0].sum
    payload["bankMovement"] = bankMovement
    payload["sum"] = suma
    return payload

class MovimientosConciliarDeleteView(AdminClientsPermisoMixin,DeleteView):
  template_name = "movimientos/eliminar-conciliacion.html"
  model = Conciliation
  def get_success_url(self, *args, **kwargs):
    pk = self.object.idMovOrigin.id
    #model = Documents.objects.get(id=self.kwargs["pk"])
    #model.delete()
    return reverse_lazy('movimientos_app:movimientos-detalle', kwargs={'pk':pk})
  #success_url = reverse_lazy('movimientos_app:lista-transferencias')

# ====================  DOCUMENTS UPLOAD ===========================
def upload_file(request):
  if request.method == 'POST':
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
      file = request.FILES['file']
      
      try:
        df = pd.read_excel(file,header=None)

        print(df)

        accountNumber = df.iloc[0,1].split(" - ")[0]
        idAccount = Account.objects.CuentasByNumber(accountNumber)
        print(accountNumber,idAccount)

        # SAVE FILENAME
        DocumentsUploaded.objects.create(
          idAccount=idAccount,
          fileName=file,
        )

        idoc = DocumentsUploaded.objects.idLastDocument()

        repReg = []

        flag_read = False
        lastBalance = 0
        for index, row in df.iloc[::-1].iterrows():

          if row[0] == "Fecha":
            break;
          else:
            tipo = "0"
            if row[3] >= 0:
              tipo = "1"
            dateR = "-".join(row[0].split("/")[::-1])
            searchFlag = BankMovements.objects.BusquedaRegistros(idAccount=idAccount,balance=row[4],opNumber=row[6])

            if not searchFlag:
              lastBalance = row[4]
              BankMovements.objects.create(
                idDoc=idoc,
                idAccount = idAccount,
                date=dateR,
                description=row[2],
                amount=abs(row[3]),
                balance=lastBalance,
                opNumber=row[6],
                transactionType=tipo
              )
              
            else:
              repReg.append(searchFlag)

        obs = 'Datos importados exitosamente!' + ' con ' + str(len(repReg)) + ' coincidencias'
      
        # OBSERVATION FROM UPDATE FILES
        docsUp = DocumentsUploaded.objects.get(id=idoc.id)
        docsUp.observations=obs
        docsUp.save()

        # SAVE AMOUNT IN ACCOUNT MODEL
        account = Account.objects.get(accountNumber=accountNumber)
        account.observations=lastBalance
        account.save()

        messages.success(request, obs)

        return redirect('/movimientos/subir-excel/')
      except Exception as e:
          messages.error(request, f'Error procesando el archivo: {e}')
  else:
    form = UploadFileForm()
    docs = DocumentsUploaded.objects.ListaNArchivos(5)
  return render(request, 'movimientos/upload.html', {'form':form,'docs':docs})

# ================= Transferencias ========================
class TransferenciasListView(AdminClientsPermisoMixin,ListView):
  template_name = "movimientos/lista-transferencias.html"
  context_object_name = 'transferencias'
  def get_queryset(self):
    intervalDate = self.request.GET.get("dateKword", '')
    if intervalDate == "today" or intervalDate =="":
        intervalDate = str(date.today() - timedelta(days = 7)) + " to " + str(date.today())
        print(intervalDate)
    payload = {}
    payload["intervalDate"] = intervalDate
    payload["transferencia"] = InternalTransfers.objects.ListarPorIntervalo(intervalDate)
        
    return payload
  #model = InternalTransfers

class TransferenciasCreateView(AdminClientsPermisoMixin,CreateView):
  template_name = "movimientos/crear-transferencia.html"
  model = InternalTransfers
  form_class = InternalTransfersForm
  success_url = reverse_lazy('movimientos_app:lista-transferencias')

class TransferenciasDeleteView(AdminClientsPermisoMixin,DeleteView):
  template_name = "movimientos/eliminar-transferencia.html"
  model = InternalTransfers
  success_url = reverse_lazy('movimientos_app:lista-transferencias')

class TransferenciasUpdateView(AdminClientsPermisoMixin,UpdateView):
  template_name = "movimientos/editar-transferencia.html"
  model = InternalTransfers
  form_class = InternalTransfersForm
  success_url = reverse_lazy('movimientos_app:lista-transferencias')


