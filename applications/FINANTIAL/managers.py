from django.db import models
from django.db.models import Sum, Q
#from django.db.models.signals import pre_save, post_save, post_delete

# ─────────────────────────────────────────────────────────────────────────────
# MANAGERS
# ─────────────────────────────────────────────────────────────────────────────
class PaymentDocumentManager(models.Manager):
    def for_tin(self, tin):
        return self.filter(Q(tin_issuer=tin) | Q(tin_receiver=tin))
    def pending(self):
        return self.filter(status__in=['PENDING', 'PARTIAL'])
    def by_quote(self, quote):
        return self.filter(allocations__item__idTrafoQuote=quote).distinct()
    def by_int_quote(self, int_quote):
        return self.filter(allocations__item__idTrafoIntQuote=int_quote).distinct()
    def by_work_order(self, work_order):
        return self.filter(allocations__item__idWorkOrder=work_order).distinct()

class PaymentTransactionManager(models.Manager):
    def for_tin(self, tin):
        return self.filter(Q(tin_payer=tin) | Q(tin_receiver=tin))
    def for_account(self, account):
        return self.filter(bank_account=account)
    def pending_reconciliation(self):
        return self.filter(reconciled_amount__lt=F('amount'))
    def drafts(self):
        return self.filter(status='DRAFT')
    def confirmed(self):
        return self.filter(status='CONFIRMED')
    
class BankMovementsManager0(models.Manager):

    def for_account(self, account):
        return self.filter(idAccount=account).order_by('date')

    def for_tin(self, tin):
        return self.filter(tin=tin).order_by('-date')

    def pending_conciliation(self):
        return self.filter(conciliated=False)

    def by_date_range(self, date_from, date_to):
        return self.filter(date__range=(date_from, date_to))

    def egresos(self):
        return self.filter(movementType__flow=MovementType.EGRESO)

    def ingresos(self):
        return self.filter(movementType__flow=MovementType.INGRESO)

    def SumaMontosConciliadosPorMovimientosOr(self, movement_id):
        return Conciliation.objects.filter(
            idMovOrigin_id=movement_id
        ).aggregate(
            sumDoc=Sum('amountReconcilied', filter=Q(type=Conciliation.DOC)),
            sumMov=Sum('amountReconcilied', filter=Q(type=Conciliation.MOV)),
        )

    def SumaMontosConciliadosPorMovimientosDest(self, movement_id):
        return Conciliation.objects.filter(
            idMovArrival_id=movement_id
        ).aggregate(sum=Sum('amountReconcilied'))

class BankMovementsManager(models.Manager):
    def for_account(self, account):
        return self.filter(idAccount=account).order_by('date')
    def for_tin(self, tin):
        return self.filter(tin=tin).order_by('-date')
    def pending_conciliation(self):
        return self.filter(conciliated=False)
    def by_date_range(self, date_from, date_to):
        return self.filter(date__range=(date_from, date_to))
    def egresos(self):
        return self.filter(movementType__flow=MovementType.EGRESO)
    def ingresos(self):
        return self.filter(movementType__flow=MovementType.INGRESO)
    def SumaMontosConciliadosPorMovimientosOr(self, movement_id):
        return Conciliation.objects.filter(idMovOrigin_id=movement_id).aggregate(
            sumDoc=Sum('amountReconcilied', filter=Q(type=Conciliation.DOC)),
            sumMov=Sum('amountReconcilied', filter=Q(type=Conciliation.MOV)),
        )
    def SumaMontosConciliadosPorMovimientosDest(self, movement_id):
        return Conciliation.objects.filter(idMovArrival_id=movement_id).aggregate(sum=Sum('amountReconcilied'))

class ConciliationManager0(models.Manager):

    def SumaMontosConciliadosPorDocumentos(self, document_id):
        return self.filter(payment_document_id=document_id).aggregate(sum=Sum('amountReconcilied'))

    def SumaMontosConciliadosPorMovimientosOr(self, movement_id):
        return self.filter(idMovOrigin_id=movement_id).aggregate(
            sumDoc=Sum('amountReconcilied', filter=Q(type=Conciliation.DOC)),
            sumMov=Sum('amountReconcilied', filter=Q(type=Conciliation.MOV)),
        )

    def SumaMontosConciliadosPorMovimientosDest(self, movement_id):
        return self.filter(idMovArrival_id=movement_id).aggregate(sum=Sum('amountReconcilied'))

    def for_movement(self, movement):
        return self.filter(Q(idMovOrigin=movement) | Q(idMovArrival=movement))

    def for_document(self, doc):
        return self.filter(idDoc=doc)

class ConciliationManager(models.Manager):
    def SumaMontosConciliadosPorDocumentos(self, document_id):
        return self.filter(payment_document_id=document_id).aggregate(sum=Sum('amountReconcilied'))
    def SumaMontosConciliadosPorMovimientosOr(self, movement_id):
        return self.filter(idMovOrigin_id=movement_id).aggregate(
            sumDoc=Sum('amountReconcilied', filter=Q(type=Conciliation.DOC)),
            sumMov=Sum('amountReconcilied', filter=Q(type=Conciliation.MOV)),
        )
    def SumaMontosConciliadosPorMovimientosDest(self, movement_id):
        return self.filter(idMovArrival_id=movement_id).aggregate(sum=Sum('amountReconcilied'))
    def for_movement(self, movement):
        return self.filter(Q(idMovOrigin=movement) | Q(idMovArrival=movement))
