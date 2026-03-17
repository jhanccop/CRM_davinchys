"""
FINANTIAL/signals.py
====================
Signals de la app FINANTIAL.

Registro: se conectan automáticamente desde apps.py → FINANTIALConfig.ready()
No importar directamente desde models.py.
"""

import re
from decimal import Decimal

from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from .models import (
    BankMovements,
    Conciliation,
    FinancialDocuments,
    bankAccountsClient,
)


# ─────────────────────────────────────────────────────────────────────────────
# BankMovements — pre_save
# ─────────────────────────────────────────────────────────────────────────────
@receiver(pre_save, sender=BankMovements)
def auto_assign_tin_and_detect_client(sender, instance, **kwargs):
    """
    1. Auto-asigna Tin desde la cuenta bancaria si todavía no está definido.
    2. Intenta auto-detectar el cliente buscando su número de cuenta
       dentro de la descripción del movimiento.
    """
    # Auto-asignar Tin
    if not instance.tin_id and instance.idAccount_id:
        try:
            instance.tin = instance.idAccount.idTin
        except Exception:
            pass

    # Auto-detectar cliente desde número en descripción
    try:
        text = instance.description or ''
        code = re.sub(r'\D', '', text)
        if code:
            ac = bankAccountsClient.objects.filter(account__startswith=code).first()
            if ac:
                instance.originDestination = ac.idClient
    except Exception:
        pass


# ─────────────────────────────────────────────────────────────────────────────
# Conciliation — post_save
# ─────────────────────────────────────────────────────────────────────────────
@receiver(post_save, sender=Conciliation)
def update_after_conciliation(sender, instance, **kwargs):
    """
    Al guardar una Conciliation:
      1. Marca status = True en la propia conciliación.
      2. Recalcula amountReconcilied en el movimiento origen.
      3. Si type=DOC → actualiza amountReconcilied en el FinancialDocument.
      4. Si type=MOV → recalcula el movimiento destino y crea la conciliación
         espejo (bidireccional) si aún no fue procesada.
    """
    # Marcar como procesada
    Conciliation.objects.filter(id=instance.id).update(status=True)

    # Recalcular movimiento origen
    try:
        instance.idMovOrigin.recalculate_reconciled()
    except Exception:
        pass

    # Evitar re-procesar una conciliación ya marcada (p.ej. la espejo)
    if instance.status:
        return

    if instance.type == Conciliation.DOC and instance.idDoc_id:
        doc     = FinancialDocuments.objects.filter(id=instance.idDoc_id)
        new_amt = Conciliation.objects.SumaMontosConciliadosPorDocumentos(instance.idDoc_id)
        doc.update(amountReconcilied=new_amt.get('sum') or 0)

    elif instance.type == Conciliation.MOV and instance.idMovArrival_id:
        # Recalcular movimiento destino
        try:
            instance.idMovArrival.recalculate_reconciled()
        except Exception:
            pass

        # Conciliación espejo (bidireccional)
        curr_or   = instance.idMovOrigin.idAccount.currency
        curr_ar   = instance.idMovArrival.idAccount.currency
        same_curr = (curr_or == curr_ar)

        Conciliation.objects.create(
            status=True,
            type=instance.type,
            source=instance.source,
            idMovOrigin=instance.idMovArrival,
            idMovArrival=instance.idMovOrigin,
            amountReconcilied=instance.amountReconcilied if same_curr else instance.equivalentAmount,
            equivalentAmount=0 if same_curr else instance.amountReconcilied,
        )


# ─────────────────────────────────────────────────────────────────────────────
# Conciliation — post_delete
# ─────────────────────────────────────────────────────────────────────────────
@receiver(post_delete, sender=Conciliation)
def update_after_delete_conciliation(sender, instance, **kwargs):
    """
    Al eliminar una Conciliation:
      1. Recalcula amountReconcilied en el movimiento origen.
      2. Si type=DOC → recalcula el monto conciliado del FinancialDocument.
      3. Si type=MOV → recalcula el movimiento destino.
    """
    try:
        instance.idMovOrigin.recalculate_reconciled()
    except Exception:
        pass

    if instance.type == Conciliation.DOC and instance.idDoc_id:
        try:
            doc     = FinancialDocuments.objects.filter(id=instance.idDoc_id)
            new_amt = Conciliation.objects.SumaMontosConciliadosPorDocumentos(instance.idDoc_id)
            doc.update(amountReconcilied=new_amt.get('sum') or Decimal('0'))
        except Exception:
            pass

    elif instance.type == Conciliation.MOV and instance.idMovArrival_id:
        try:
            instance.idMovArrival.recalculate_reconciled()
        except Exception:
            pass