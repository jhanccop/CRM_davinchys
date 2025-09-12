from datetime import date, timedelta

from csv import DictReader
from io import TextIOWrapper
import pandas as pd

from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages

from django.utils import timezone

from django.views.generic.edit import ModelFormMixin

from applications.users.mixins import (
  AdminPermisoMixin,
  AdminClientsPermisoMixin, # Adquisiciones, Finanzas, Tesoreria, contabilidad y administrador
  FinanzasMixin,
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
  IncomeSubCategories,
  ExpenseSubCategories,
  BankMovements,
  Conciliation
)

from applications.cuentas.models import Account
#from applications.documentos.models import FinancialDocuments


from .forms import (
  BankMovementsForm,
  ConciliationIntForm,
  ConciliationMovDocForm,
  ConciliationMovMovForm,
  EditConciliationMovMovForm,
  EditConciliationMovDocForm,
  UploadFileForm,
)

# ================= MOVIMIENTOS ========================
class MovimientosListView(FinanzasMixin,ListView):
  template_name = "FINANCIERA/movimientosBancarios/lista-movimientos.html"
  context_object_name = 'movimientos'

  def get_queryset(self,**kwargs):
    compania_id = self.request.user.company.id
    selectedAccount = self.request.GET.get("AccountKword", '')
    intervalDate = self.request.GET.get("dateKword", '')
    if intervalDate == "today" or intervalDate =="":
      intervalDate = str(date.today() - timedelta(days = 90)) + " to " + str(date.today())

    if selectedAccount == "None" or selectedAccount == None or selectedAccount =="" :
      idSelected = Account.objects.CuentasByLastUpdate(compania_id = compania_id)
      selectedAccount = idSelected.id # seleccionar por default la primera cuenta

    bankMovements = BankMovements.objects.ListaMovimientosPorCuenta(intervalo = intervalDate, cuenta = int(selectedAccount))
    payload = {}
    payload["intervalDate"] = intervalDate
    payload["selectedAccount"] = Account.objects.CuentasById(int(selectedAccount))
    payload["listAccount"] = Account.objects.listarcuentas(compania_id = compania_id)
    payload["lastBalance"] = BankMovements.objects.ObtenerSaldo(cuenta=int(selectedAccount))

    payload["bankMovements"] = bankMovements
    return payload

class MovimientosEditView(FinanzasMixin,UpdateView):
  template_name = "FINANCIERA/movimientosBancarios/editar-movimientos.html"
  model = BankMovements
  form_class = BankMovementsForm
  success_url = reverse_lazy('movimientosBancarios_app:lista-movimientos')

  #def get_queryset(self,**kwargs):
  #  payload = { "compania_id": self.request.session.get('compania_id')}
  #  return payload
  def get_form_kwargs(self):
    kwargs = super().get_form_kwargs()
    kwargs['request'] = self.request
    return kwargs

class MovimientosCreateView(FinanzasMixin,CreateView):
  template_name = "FINANCIERA/movimientosBancarios/crear-movimientos.html"
  model = BankMovements
  form_class = BankMovementsForm
  success_url = reverse_lazy('movimientosBancarios_app:lista-movimientos')

  def get_form_kwargs(self):
    kwargs = super().get_form_kwargs()
    kwargs['request'] = self.request
    return kwargs

class MovimientosDeleteView(FinanzasMixin,DeleteView):
  template_name = "FINANCIERA/movimientosBancarios/eliminar-movimientos.html"
  model = BankMovements
  success_url = reverse_lazy('movimientosBancarios_app:lista-movimientos')

class MovimientosDetailView(FinanzasMixin,ListView):
  template_name = "FINANCIERA/movimientosBancarios/detalle-movimiento.html"
  context_object_name = 'mov'
  def get_queryset(self,**kwargs):
    pk = self.kwargs['pk']
    payload = {}
    bankMovement = BankMovements.objects.MovimientosPorId(id = int(pk))
    #documentation = Documents.objects.ListaConciliacionPorIdMovimiento(bankMovement.id)
    suma = Conciliation.objects.SumaMontosPorIdMov(bankMovement.id)#[0].sum
    payload["bankMovement"] = bankMovement
    payload["sum"] = suma
    return payload

# ================= CONCILIACION ========================
class ConciliarInternoCreateView(FinanzasMixin,CreateView):
  template_name = "FINANCIERA/movimientosBancarios/conciliar-interno.html"
  model = Conciliation
  form_class = ConciliationIntForm

  def get_success_url(self, *args, **kwargs):
    pk = self.kwargs["pk"]
    return reverse_lazy('movimientosBancarios_app:movimientos-detalle', kwargs={'pk':pk})

  def get_form_kwargs(self):
    kwargs = super(ConciliarInternoCreateView, self).get_form_kwargs()
    kwargs.update({'pk': self.kwargs["pk"]})
    return kwargs

  def get_context_data(self, **kwargs):
    context = super(ConciliarInternoCreateView, self).get_context_data(**kwargs)
    bankMovement = BankMovements.objects.get(id = self.kwargs['pk'])
    context['mov'] = bankMovement
    context['sum'] = Conciliation.objects.SumaMontosConciliadosPorMovimientosOr(bankMovement.id)
    return context

class ConciliarMovimientoConDocumentoCreateView(FinanzasMixin,CreateView):
  template_name = "FINANCIERA/movimientosBancarios/conciliar-movimiento-con-documento.html"
  model = Conciliation
  form_class = ConciliationMovDocForm

  def get_success_url(self, *args, **kwargs):
    pk = self.kwargs["pk"]
    #return reverse_lazy('movimientos_app:asignar-montos-documento', kwargs={'pk':pk})
    return reverse_lazy('movimientosBancarios_app:movimientos-detalle', kwargs={'pk':pk})

  def get_context_data(self, **kwargs):
    context = super(ConciliarMovimientoConDocumentoCreateView, self).get_context_data(**kwargs)
    bankMovement = BankMovements.objects.get(id = self.kwargs['pk'])
    context['mov'] = bankMovement
    #context['sum'] = Conciliation.objects.SumaMontosConciliadosPorMovimientosOr(bankMovement.id)
    return context
  
  def get_form_kwargs(self):
        # Obtén los kwargs que normalmente se pasan al formulario
        kwargs = super().get_form_kwargs()
        company_id = self.request.session.get('compania_id')
        kwargs['company_id'] = company_id
        return kwargs

class ConciliarMovimientoConMovimientoCreateView(FinanzasMixin,CreateView):
  template_name = "FINANCIERA/movimientosBancarios/conciliar-movimiento-con-movimiento.html"
  model = Conciliation
  form_class = ConciliationMovMovForm
  #success_url = reverse_lazy('movimientos_app:lista-movimientos')

  def get_success_url(self, *args, **kwargs):
    pk = self.kwargs["pk"]
    #return reverse_lazy('movimientos_app:asignar-montos-documento', kwargs={'pk':pk})
    return reverse_lazy('movimientosBancarios_app:movimientos-detalle', kwargs={'pk':pk})


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
 
class EditarMovimientoConMovimientoUpdateView(FinanzasMixin,UpdateView):
  template_name = "FINANCIERA/movimientosBancarios/editar-movimiento-con-movimiento.html"
  model = Conciliation
  form_class = EditConciliationMovMovForm

  def get_success_url(self, **kwargs):
    idOr = self.kwargs["pk"]
    idMov = Conciliation.objects.get(id = idOr)
    return reverse_lazy('movimientosBancarios_app:movimientos-detalle', kwargs={'pk':idMov.idMovOrigin.id})

class EditarMovimientoConDocumentoUpdateView(FinanzasMixin,UpdateView):
  template_name = "FINANCIERA/movimientosBancarios/editar-movimiento-con-documento.html"
  model = Conciliation
  form_class = EditConciliationMovDocForm

  def get_success_url(self, **kwargs):
    idOr = self.kwargs["pk"]
    idMov = Conciliation.objects.get(id = idOr)
    return reverse_lazy('movimientosBancarios_app:movimientos-detalle', kwargs={'pk':idMov.idMovOrigin.id})

class MovimientosConciliarDeleteView(FinanzasMixin,DeleteView):
  template_name = "FINANCIERA/movimientosBancarios/eliminar-conciliacion.html"
  model = Conciliation
  def get_success_url(self, *args, **kwargs):
    pk = self.object.idMovOrigin.id
    #model = Documents.objects.get(id=self.kwargs["pk"])
    #model.delete()
    return reverse_lazy('movimientosBancarios_app:movimientos-detalle', kwargs={'pk':pk})
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

        return redirect('FINANCIERA/movimientosBancarios/subir-excel/')
      except Exception as e:
          messages.error(request, f'Error procesando el archivo: {e}')
  else:
    form = UploadFileForm()
    docs = DocumentsUploaded.objects.ListaNArchivos(5)
  return render(request, 'FINANCIERA/movimientosBancarios/upload.html', {'form':form,'docs':docs})
