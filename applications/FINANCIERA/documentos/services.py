import json
from io import StringIO

def corregir_codificacion(texto_mal_codificado):
    """
    Corrige caracteres mal codificados (mojibake) comunes cuando UTF-8 se interpreta como Latin-1
    Ejemplo: "Dï¿½LARES" -> "DÓLARES"
    """
    try:
        texto_bytes = texto_mal_codificado.encode('latin1')
        return texto_bytes.decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        return texto_mal_codificado

def procesar_linea(linea, encabezados):
    """
    Procesa una línea individual y devuelve un diccionario con los datos
    """
    valores = [v.strip() for v in linea.split('|') if v.strip()]
    registro = {}
    
    for i, encabezado in enumerate(encabezados):
        valor = valores[i] if i < len(valores) else ""
        registro[encabezado] = corregir_codificacion(valor)
    
    return registro

def procesar_datos(texto):
    """
    Procesa el texto completo y devuelve un diccionario estructurado
    """
    try:
        # Configurar lectura en formato UTF-8
        datos = StringIO(texto)
        lineas = [linea.strip() for linea in datos.readlines() if linea.strip()]
        
        if not lineas:
            return {"error": "El texto está vacío"}
        
        # Obtener encabezados
        encabezados = [h.strip() for h in lineas[0].split('|') if h.strip()]
        
        # Procesar registros
        registros = []
        anotaciones = []
        
        for linea in lineas[1:]:
            try:
                registro = procesar_linea(linea, encabezados)
                registros.append(registro)
            except Exception as e:
                anotaciones.append(f"Error al procesar línea: {linea} - {str(e)}")
        
        # Ensamblar resultado final en formato JSON estructurado
        return {
            "metadata": {
                "total_registros": len(registros),
                "campos": encabezados,
                "anotaciones": anotaciones if anotaciones else "No hay anotaciones"
            },
            "data": registros
        }
        
    except Exception as e:
        return {"error": f"Error al procesar los datos: {str(e)}"}

# Datos de entrada
#TEXTO_EJEMPLO = """Fecha de Emisión|Tipo Doc. Emitido|Nro. Doc. Emitido|Estado Doc. Emitido|Tipo de Doc. Emisor|Nro. Doc. Emisor|Apellidos y Nombres, Denominación o Razón Social del Emisor|Tipo de Renta|Gratuito|Descripción|Observación|Moneda de Operación|Renta Bruta|Impuesto a la Renta|Renta Neta|Monto Neto Pendiente de Pago|
#07/04/2025|RH|E001-51|NO ANULADO|RUC|10474308061|RIVAS CHAMORRO JOSE ANTONIO                                                                         |A|NO|SERVICIO DE SUPERVISIÓN EN PRUEBAS A TRANSFORMADORES |- |SOLES|2768.46|0.00|2768.46|0.00|
#10/04/2025|RH|E001-32|REVERTIDO|RUC|10434919954|HANCCO PACCORI JOEL JAFET                                                                           |A|NO|SERVICIO DE PROGRAMACIÓN DE SISTEMA INFORMÁTICO Y DE AUTOMATIZACIÓN |- |Dï¿½LARES DE NORTE AMï¿½RICA|3000.00|0.00|3000.00|0.00|
#14/04/2025|RH|E001-33|NO ANULADO|RUC|10434919954|HANCCO PACCORI JOEL JAFET                                                                           |A|NO|SERVICIO DE PROGRAMACIÓN DE SISTEMA INFORMÁTICO Y DE AUTOMATIZACIÓN |- |Dï¿½LARES DE NORTE AMï¿½RICA|3000.00|0.00|3000.00|0.00|"""

# Procesamiento y salida
#if __name__ == "__main__":
#    resultado = procesar_datos(TEXTO_EJEMPLO)
    
    # Convertir a JSON con formato legible y asegurando caracteres Unicode
#    json_resultado = json.dumps(resultado, indent=4, ensure_ascii=False)
    
#    print(json_resultado)
    
    # Opcional: Guardar en un archivo
    #with open('resultado_procesado.json', 'w', encoding='utf-8') as f:
    #    f.write(json_resultado)