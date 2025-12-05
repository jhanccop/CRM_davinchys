from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import Items, ItemTracking, Trafo
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

        
# Signal para eliminar archivos cuando se elimina el registro ITEMS
@receiver(post_delete, sender=Items)
def delete_files_on_delete(sender, instance, **kwargs):
    """
    Elimina todos los archivos del sistema cuando se elimina el registro
    """
    # Eliminar fat_file
    if instance.fat_file:
        if os.path.isfile(instance.fat_file.path):
            os.remove(instance.fat_file.path)
       
    # Eliminar plate_file
    if instance.plate_file:
        if os.path.isfile(instance.plate_file.path):
            os.remove(instance.plate_file.path)

# Signal para eliminar archivos cuando se elimina el registro TRAFO
@receiver(post_delete, sender=Trafo)
def delete_files_on_delete(sender, instance, **kwargs):
    """
    Elimina todos los archivos del sistema cuando se elimina el registro
    """
    # Eliminar drawing_file
    if instance.drawing_file:
        if os.path.isfile(instance.drawing_file.path):
            os.remove(instance.drawing_file.path)

# Signal para eliminar archivos anteriores cuando se actualizan ITEMS
@receiver(pre_save, sender=Items)
def delete_old_files_on_update(sender, instance, **kwargs):
    """
    Elimina los archivos anteriores cuando se actualizan con nuevos archivos
    """
    if not instance.pk:
        return False

    try:
        old_instance = Items.objects.get(pk=instance.pk)
    except Items.DoesNotExist:
        return False

    # Verificar y eliminar fat_file anterior
    if old_instance.fat_file and old_instance.fat_file != instance.fat_file:
        if os.path.isfile(old_instance.fat_file.path):
            os.remove(old_instance.fat_file.path)

    # Verificar y eliminar plate_file anterior
    if old_instance.plate_file and old_instance.plate_file != instance.plate_file:
        if os.path.isfile(old_instance.plate_file.path):
            os.remove(old_instance.plate_file.path)

# Signal para eliminar archivos anteriores cuando se actualizan TRAFOA
@receiver(pre_save, sender=Trafo)
def delete_old_files_on_update(sender, instance, **kwargs):
    """
    Elimina los archivos anteriores cuando se actualizan con nuevos archivos
    """
    if not instance.pk:
        return False

    try:
        old_instance = Trafo.objects.get(pk=instance.pk)
    except Trafo.DoesNotExist:
        return False

    # Verificar y eliminar drawing_file anterior
    if old_instance.drawing_file and old_instance.drawing_file != instance.drawing_file:
        if os.path.isfile(old_instance.drawing_file.path):
            os.remove(old_instance.drawing_file.path)
