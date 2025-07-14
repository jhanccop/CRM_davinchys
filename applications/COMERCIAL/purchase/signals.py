from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import (
    requirements,
    requirementItems,
    RequestTracking,
    PettyCash
)
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
                currency=item_data.get('currency'),
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