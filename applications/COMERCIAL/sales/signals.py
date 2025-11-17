from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import Items, ItemTracking
import os

@receiver(post_save, sender=Items)
def create_item_tracking(sender, instance, created, **kwargs):
    """
    Signal que crea automáticamente un registro de ItemTracking
    cada vez que se crea un nuevo Item.
    
    Args:
        sender: El modelo que envía la señal (Items)
        instance: La instancia del Item que se guardó
        created: Boolean que indica si es una nueva instancia
        **kwargs: Argumentos adicionales
    """
    if created:
        ItemTracking.objects.create(
            idItem=instance,
            statusItem=ItemTracking.SOLICITADO,
            statusPlate=ItemTracking.SOLICITADO
        )

# Signal para eliminar archivo cuando se elimina el registro
@receiver(post_delete, sender=Items)
def delete_fat_file_on_delete(sender, instance, **kwargs):
    """
    Elimina el archivo del sistema cuando se elimina el registro
    """
    if instance.fat_file:
        if os.path.isfile(instance.fat_file.path):
            os.remove(instance.fat_file.path)


# Signal para eliminar archivo anterior cuando se actualiza con un nuevo archivo
@receiver(pre_save, sender=Items)
def delete_old_fat_file_on_update(sender, instance, **kwargs):
    """
    Elimina el archivo anterior cuando se actualiza con uno nuevo
    """
    if not instance.pk:
        return False

    try:
        old_file = Items.objects.get(pk=instance.pk).fat_file
    except Items.DoesNotExist:
        return False

    # Si hay un archivo anterior y es diferente al nuevo, eliminarlo
    new_file = instance.fat_file
    if old_file and old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)