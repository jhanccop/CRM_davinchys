from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import (
    requirements,
    requirementItems,
    RequestTracking,
    PettyCash,
    requirementsQuotes,
    PurchaseOrderInvoice
)

# =============================== SIGNALS QUOTES ===============================
@receiver(post_save, sender=requirementsQuotes)
def quote_update_tracking(sender, instance, created, **kwargs):
    """
    Crea un registro de treacking cond se crea una cotizacion
    """
    if created:
        RequestTracking.objects.create(
            idRequirement=instance.idRequirement,
            status=RequestTracking.COTIZACIONRECIBIDA,  # Estado inicial 'Creado'
        )

#@receiver(pre_delete, sender=requirementsQuotes)
#def requirement_delete_tracking(sender, instance, **kwargs):
#    """
#    Crea un registro de tracking cuando se elimina un requerimiento
#    con un estado que indique que fue eliminado
#    """
#
#    print("2******************",instance.idRequirement)
#    # Verifica si existe un tracking previo para este requerimiento
#    if RequestTracking.objects.filter(idRequirement=instance.idRequirement).exists():
#        # Crea un nuevo registro de tracking con estado "Eliminado"
#        RequestTracking.objects.create(
#            idRequirement=instance.idRequirement,
#            status=RequestTracking.SOLICITADO,  # Asegúrate de tener este estado definido en tu modelo
#            comments="Requerimiento eliminado del sistema"
#        )

# =============================== SIGNALS Purchase Order Invoice ===============================
@receiver(post_save, sender=PurchaseOrderInvoice)
def PurchaseOrderInvoice_update_tracking(sender, instance, created, **kwargs):
    """
    Crea un registro de tracking al adjuntar una factura
    """
    if created:
        RequestTracking.objects.create(
            idRequirement=instance.idRequirement,
            status=RequestTracking.FACTURADA,  # Estado inicial 'Creado'
        )

#@receiver(pre_delete, sender=PurchaseOrderInvoice)
#def PurchaseOrderInvoice_delete_tracking(sender, instance, **kwargs):
#    """
#    Crea un registro de tracking cuando se elimina un invoice
#    con un estado que indique que fue eliminado
#    """
#    # Verifica si existe un tracking previo para este requerimiento
#    if RequestTracking.objects.filter(idRequirement=instance).exists():
#        # Crea un nuevo registro de tracking con estado "Eliminado"
#        RequestTracking.objects.create(
#            idRequirement=instance.idRequirement,
#            status=RequestTracking.COTIZACIONRECIBIDA,  # Asegúrate de tener este estado definido en tu modelo
#            comments="Requerimiento eliminado del sistema"
#        )

# =============================== SIGNALS REQUIREMENTS ===============================
@receiver(post_save, sender=requirements)
def save_requirement_items(sender, instance, created, **kwargs):
    """
    Signal para crear items segun requerimiento
    """
    if created and hasattr(instance, '_requirement_items'):
        for item_data in instance._requirement_items:
            requirementItems.objects.create(
                idRequirement=instance,
                quantity=item_data.get('quantity'),
                #currency=item_data.get('currency'),
                price=item_data.get('price'),
                product=item_data.get('product')
            )
        # Eliminamos el atributo temporal después de usarlo
        del instance._requirement_items

@receiver(post_save, sender=requirements)
def create_initial_tracking(sender, instance, created, **kwargs):
    """
    Crea un registro de tracking inicial cuando se crea un nuevo requerimiento
    """
    if created:
        RequestTracking.objects.create(
            idRequirement=instance,
            status=RequestTracking.RECIBIDO,  # Estado inicial 'Creado'
            area=RequestTracking.AREAMANAGER  # Área inicial 'Usuario'
        )


# =============================== SIGNALS CAJA CHICA ===============================
@receiver(post_save, sender=PettyCash)
def save_PettyCash_items(sender, instance, created, **kwargs):
    """
    Signal para crear items segun requerimiento
    """
    if created and hasattr(instance, '_requirement_items'):
        for item_data in instance._requirement_items:
            requirementItems.objects.create(
                idRequirement=instance,
                category=item_data.get('category'),
                quantity=item_data.get('quantity'),
                currency=item_data.get('currency'),
                price=item_data.get('price'),
                product=item_data.get('product')
            )
        # Eliminamos el atributo temporal después de usarlo
        del instance._requirement_items