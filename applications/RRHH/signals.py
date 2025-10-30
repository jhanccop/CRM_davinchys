from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import datetime, time, timedelta
from decimal import Decimal
from .models import RegistroAsistencia

@receiver(pre_save, sender=RegistroAsistencia)
def procesar_registro_asistencia(sender, instance, **kwargs):
    """
    Signal que procesa automáticamente los datos de asistencia antes de guardar:
    - Determina el tipo de jornada diaria (laborable/feriado/fin de semana)
    - Divide y crea registros según tipo de jornada horaria
    - Calcula horas trabajadas
    - Establece estado según tipo de jornada
    """

    # Solo procesar si hay hora_inicio y hora_final
    if not instance.hora_inicio or not instance.hora_final:
        return
    
    # 1. DETERMINAR TIPO DE JORNADA DIARIA
    instance.jornada_diaria = determinar_jornada_diaria(instance.fecha)
    
    # 2. DETERMINAR TIPO DE JORNADA HORARIA Y DIVIDIR SI ES NECESARIO
    segmentos = dividir_por_jornada_horaria(instance.hora_inicio, instance.hora_final)
    
    # Si hay múltiples segmentos, procesamos el primero en la instancia actual
    # y creamos los adicionales
    if len(segmentos) > 0:
        # Procesar primer segmento en la instancia actual
        primer_segmento = segmentos[0]
        instance.hora_inicio = primer_segmento['hora_inicio']
        instance.hora_final = primer_segmento['hora_final']
        instance.jornada_horaria = primer_segmento['tipo']
        
        # 3. CALCULAR HORAS
        instance.horas = calcular_horas(instance.hora_inicio, instance.hora_final)
        
        # 4. DETERMINAR ESTADO
        instance.estado = determinar_estado(
            instance.jornada_horaria,
            instance.jornada_diaria,
            instance.estado
        )
        
        # 5. CREAR REGISTROS ADICIONALES PARA LOS DEMÁS SEGMENTOS
        # Solo si estamos creando (no actualizando)
        if not instance.pk and len(segmentos) > 1:
            # Guardamos los segmentos adicionales para crearlos después del save
            # usando un atributo temporal
            instance._segmentos_adicionales = segmentos[1:]


def determinar_jornada_diaria(fecha):
    """
    Determina el tipo de jornada diaria según la fecha.
    
    Args:
        fecha: objeto date
    
    Returns:
        str: código de jornada diaria (LABORABLE, FERIADO, FINDESEMANA)
    """
    # Obtener día de la semana (0=Lunes, 6=Domingo)
    dia_semana = fecha.weekday()
    
    # Fin de semana (Sábado=5, Domingo=6)
    if dia_semana >= 5:
        return RegistroAsistencia.FINDESEMANA
    
    # Verificar si es feriado
    if es_feriado(fecha):
        return RegistroAsistencia.FERIADO
    
    # Día laborable normal
    return RegistroAsistencia.LABORABLE


def es_feriado(fecha):
    """
    Verifica si una fecha es feriado consultando el modelo Feriados.
    
    Args:
        fecha: objeto date
    
    Returns:
        bool: True si es feriado
    """
    from .models import Feriados
    return Feriados.objects.filter(fecha=fecha).exists()


def dividir_por_jornada_horaria(hora_inicio, hora_final):
    """
    Divide un rango horario en segmentos según el tipo de jornada horaria.
    
    Args:
        hora_inicio: objeto time
        hora_final: objeto time
    
    Returns:
        list: lista de diccionarios con segmentos {tipo, hora_inicio, hora_final}
    """
    # Definir rangos horarios
    rangos = [
        {
            'tipo': RegistroAsistencia.REGULAR,
            'inicio': time(9, 0),
            'fin': time(18, 0)
        },
        {
            'tipo': RegistroAsistencia.HEXTRA1,
            'inicio': time(18, 1),
            'fin': time(22, 0)
        },
        {
            'tipo': RegistroAsistencia.HEXTRA2,
            'inicio': time(22, 1),
            'fin': time(23, 59)
        },
        {
            'tipo': RegistroAsistencia.HEXTRA2,
            'inicio': time(0, 0),
            'fin': time(6, 0)
        },
    ]
    
    segmentos = []
    
    # Manejar caso cuando hora_final es menor que hora_inicio (cruza medianoche)
    if hora_final < hora_inicio:
        # Dividir en dos partes: hasta medianoche y desde medianoche
        segmentos.extend(
            procesar_rango_simple(hora_inicio, time(23, 59, 59), rangos)
        )
        segmentos.extend(
            procesar_rango_simple(time(0, 0), hora_final, rangos)
        )
    else:
        segmentos = procesar_rango_simple(hora_inicio, hora_final, rangos)
    
    return segmentos


def procesar_rango_simple(hora_inicio, hora_final, rangos):
    """
    Procesa un rango horario que no cruza medianoche.
    """
    segmentos = []
    hora_actual = hora_inicio
    
    while hora_actual < hora_final:
        # Encontrar el rango correspondiente
        for rango in rangos:
            if rango['inicio'] <= hora_actual <= rango['fin']:
                # Calcular fin del segmento
                fin_segmento = min(hora_final, rango['fin'])
                
                segmentos.append({
                    'tipo': rango['tipo'],
                    'hora_inicio': hora_actual,
                    'hora_final': fin_segmento
                })
                
                # Avanzar al siguiente minuto después del fin del segmento
                hora_actual = agregar_minuto(fin_segmento)
                break
        else:
            # Si no encontramos rango, asignar como REGULAR y avanzar
            fin_segmento = hora_final
            segmentos.append({
                'tipo': RegistroAsistencia.REGULAR,
                'hora_inicio': hora_actual,
                'hora_final': fin_segmento
            })
            break
    
    return segmentos


def agregar_minuto(hora):
    """
    Agrega un minuto a un objeto time.
    """
    dt = datetime.combine(datetime.today(), hora)
    dt += timedelta(minutes=1)
    return dt.time()


def calcular_horas(hora_inicio, hora_final):
    """
    Calcula las horas trabajadas entre dos tiempos.
    
    Args:
        hora_inicio: objeto time
        hora_final: objeto time
    
    Returns:
        Decimal: horas trabajadas con 2 decimales
    """
    # Convertir a datetime para calcular diferencia
    dt_inicio = datetime.combine(datetime.today(), hora_inicio)
    dt_final = datetime.combine(datetime.today(), hora_final)
    
    # Si hora_final es menor, significa que cruzó medianoche
    if dt_final < dt_inicio:
        dt_final += timedelta(days=1)
    
    # Calcular diferencia en horas
    diferencia = dt_final - dt_inicio
    horas = Decimal(diferencia.total_seconds() / 3600)
    
    # Redondear a 2 decimales
    return round(horas, 2)


def determinar_estado(jornada_horaria, jornada_diaria, estado_actual):
    """
    Determina el estado del registro según tipo de jornada.
    Solo cambia a PENDIENTE si el estado actual es el default (PENDIENTE).
    
    Args:
        jornada_horaria: código de jornada horaria
        jornada_diaria: código de jornada diaria
        estado_actual: estado actual del registro
    
    Returns:
        str: código de estado
    """
    # Si ya tiene un estado diferente a PENDIENTE, no lo cambiamos
    if estado_actual != RegistroAsistencia.PENDIENTE:
        return estado_actual
    
    # Determinar si requiere aprobación
    requiere_aprobacion = (
        jornada_horaria in [RegistroAsistencia.HEXTRA1, RegistroAsistencia.HEXTRA2] or
        jornada_diaria in [RegistroAsistencia.FERIADO, RegistroAsistencia.FINDESEMANA]
    )
    
    return RegistroAsistencia.PENDIENTE if requiere_aprobacion else RegistroAsistencia.APROBADO

# Signal post_save para crear registros adicionales
from django.db.models.signals import post_save

@receiver(post_save, sender=RegistroAsistencia)
def crear_segmentos_adicionales(sender, instance, created, **kwargs):
    """
    Crea registros adicionales si la jornada fue dividida en múltiples segmentos.
    """
    if created and hasattr(instance, '_segmentos_adicionales'):
        for segmento in instance._segmentos_adicionales:
            RegistroAsistencia.objects.create(
                empleado=instance.empleado,
                fecha=instance.fecha,
                hora_inicio=segmento['hora_inicio'],
                hora_final=segmento['hora_final'],
                idLocal=instance.idLocal,
                ubicacion=instance.ubicacion,
                jornada_horaria=segmento['tipo'],
                jornada_diaria=instance.jornada_diaria,
                observaciones=instance.observaciones,
                horas=calcular_horas(segmento['hora_inicio'], segmento['hora_final']),
                estado=determinar_estado(
                    segmento['tipo'],
                    instance.jornada_diaria,
                    RegistroAsistencia.PENDIENTE
                )
            )