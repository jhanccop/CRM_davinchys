from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

import time
import random
import logging

class SunatSeleniumConsulta:
    CONSULTA_URL = 'https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/FrameCriterioBusquedaWeb.jsp'
    
    def __init__(self, headless=True):
        self.driver = None
        self.headless = headless
        self._setup_driver()
    
    def _setup_driver(self):
        """Configura el driver de Chrome con opciones optimizadas"""
        chrome_options = Options()
        
        chrome_options.binary_location = "/usr/bin/google-chrome"  # O la ruta correcta
    
        if self.headless:
            chrome_options.add_argument('--headless')
        
        # Opciones para evitar detección
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # User agent realista
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Tamaño de ventana
        chrome_options.add_argument('--window-size=1920,1080')
        
        # Deshabilitar imágenes para acelerar (opcional)
        # chrome_options.add_argument('--disable-images')
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        except Exception as e:
            logging.error(f"Error al inicializar Chrome driver: {e}")
            raise
    
    def consultar_ruc(self, ruc):
        """
        Consulta RUC usando Selenium - Versión corregida para el error 'or_'
        """
        try:
            if not self.validar_ruc(ruc):
                return {'error': 'RUC inválido'}
            
            logging.info(f"Consultando RUC: {ruc}")
            
            # Navegar a la página
            self.driver.get(self.CONSULTA_URL)
            
            # Esperar que cargue la página completamente
            wait = WebDriverWait(self.driver, 20)
            
            # Esperar a que el formulario esté presente
            wait.until(EC.presence_of_element_located((By.ID, "form01")))
            
            # Asegurarse que el modo de búsqueda sea "Por RUC"
            try:
                btn_por_ruc = wait.until(EC.element_to_be_clickable((By.ID, "btnPorRuc")))
                if "active" not in btn_por_ruc.get_attribute("class"):
                    self.driver.execute_script("arguments[0].click();", btn_por_ruc)
                    time.sleep(1)
            except:
                pass
            
            # Localizar el campo de RUC correcto
            ruc_input = wait.until(EC.element_to_be_clickable((By.ID, "txtRuc")))
            
            # Limpiar el campo (método robusto)
            self.driver.execute_script("arguments[0].value = '';", ruc_input)
            ruc_input.clear()
            time.sleep(0.5)
            
            # Escribir el RUC caracter por caracter
            for char in ruc:
                ruc_input.send_keys(char)
                time.sleep(random.uniform(0.05, 0.15))
            
            time.sleep(1)
            
            # Localizar y hacer clic en el botón de búsqueda
            boton_buscar = wait.until(EC.element_to_be_clickable((By.ID, "btnAceptar")))
            
            # Desplazarse al botón y hacer clic con JavaScript
            self.driver.execute_script("arguments[0].scrollIntoView(true);", boton_buscar)
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].click();", boton_buscar)
            
            # Esperar a que cargue la página de resultados (versión alternativa sin or_)
            try:
                # Intenta primero encontrar el panel de resultados
                try:
                    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "panel-primary")))
                except TimeoutException:
                    # Si no encuentra resultados, busca mensajes de error
                    wait.until(EC.presence_of_element_located((By.ID, "divError")))
                
                time.sleep(random.uniform(2, 3))
            except TimeoutException:
                return {'error': 'Timeout esperando resultados'}
            
            # Verificar si hay errores
            if self._verificar_errores():
                return {'error': 'SUNAT reportó un error en la consulta'}
            
            # Extraer los datos
            return self._extraer_datos(ruc)
            
        except TimeoutException:
            return {'error': 'Timeout en la operación'}
        except Exception as e:
            logging.error(f"Error en consulta: {str(e)}", exc_info=True)
            return {'error': f'Error en la consulta: {str(e)}'}
        
    def _verificar_errores(self):
        """Verifica si la página contiene mensajes de error"""
        try:
            # Buscar elementos que indiquen error
            selectores_error = [
                ".error",
                ".msg",
                "[class*='error']",
                "[class*='problema']"
            ]
            
            for selector in selectores_error:
                try:
                    elementos = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for elemento in elementos:
                        texto = elemento.text.lower()
                        if any(palabra in texto for palabra in ['problema', 'error', 'surgieron']):
                            logging.error(f"Error encontrado: {elemento.text}")
                            return True
                except:
                    continue
            
            return False
        except:
            return False
    
    def _extraer_datos(self, ruc):
        """Extrae los datos de la página de resultados - Versión actualizada para el nuevo formato SUNAT"""
        try:
            datos = {'ruc': ruc}
            
            # Buscar todos los elementos de list-group-item
            items = self.driver.find_elements(By.CLASS_NAME, "list-group-item")
            
            for item in items:
                try:
                    # Obtener las columnas
                    columns = item.find_elements(By.CLASS_NAME, "row")[0].find_elements(By.CLASS_NAME, "col-sm-5") + \
                              item.find_elements(By.CLASS_NAME, "row")[0].find_elements(By.CLASS_NAME, "col-sm-7")
                    
                    # Si hay al menos 2 columnas (etiqueta y valor)
                    if len(columns) >= 2:
                        campo = columns[0].text.strip().lower()
                        valor = columns[1].text.strip()
                        
                        # Mapear campos específicos
                        if 'número de ruc' in campo:
                            # Extraer RUC y razón social
                            parts = valor.split('-')
                            if len(parts) > 1:
                                datos['ruc'] = parts[0].strip()
                                datos['razon_social'] = parts[1].strip()
                        elif 'tipo contribuyente' in campo:
                            datos['tipo_contribuyente'] = valor
                        elif 'nombre comercial' in campo:
                            datos['nombre_comercial'] = valor if valor != '-' else ''
                        elif 'estado del contribuyente' in campo:
                            datos['estado'] = valor.split('\n')[0].strip()
                            # Extraer fecha de baja si existe
                            if 'Fecha de Baja:' in valor:
                                datos['fecha_baja'] = valor.split('Fecha de Baja:')[-1].strip()
                        elif 'condición del contribuyente' in campo:
                            datos['condicion'] = valor.split('\n')[0].strip()
                        elif 'domicilio fiscal' in campo:
                            datos['direccion'] = ' '.join(valor.split())
                        elif 'actividad(es) económica(s)' in campo:
                            # Extraer actividades económicas
                            actividades = []
                            rows = item.find_elements(By.TAG_NAME, "tr")
                            for row in rows:
                                cell_text = row.text.strip()
                                if cell_text:
                                    actividades.append(cell_text)
                            datos['actividades_economicas'] = actividades
                        elif 'fecha de inscripción' in campo:
                            datos['fecha_inscripcion'] = valor
                        elif 'fecha de inicio de actividades' in campo:
                            datos['fecha_inicio_actividades'] = valor
                        elif 'comprobantes de pago' in campo.lower():
                            # Extraer comprobantes autorizados
                            comprobantes = []
                            rows = item.find_elements(By.TAG_NAME, "tr")
                            for row in rows:
                                cell_text = row.text.strip()
                                if cell_text:
                                    comprobantes.append(cell_text)
                            datos['comprobantes_autorizados'] = comprobantes
                            
                except Exception as e:
                    logging.warning(f"Error procesando item: {e}")
                    continue
            
            # Verificar si se encontraron datos
            if len(datos) <= 1:  # Solo tiene el RUC
                return {'error': 'No se encontraron datos para el RUC'}
            
            return datos
            
        except Exception as e:
            logging.error(f"Error extrayendo datos: {str(e)}")
            return {'error': f'Error extrayendo datos: {str(e)}'}

    def _verificar_errores(self):
        """Verifica si la página contiene mensajes de error - Versión actualizada"""
        try:
            # Buscar elementos de error específicos
            selectores_error = [
                ".list-group-item-danger",  # Mensajes importantes (pueden ser errores)
                ".alert-danger",
                "#divError"
            ]
            
            for selector in selectores_error:
                try:
                    elementos = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for elemento in elementos:
                        texto = elemento.text.lower()
                        if any(palabra in texto for palabra in ['error', 'no existe', 'inválido', 'vuelva a intentar']):
                            logging.error(f"Error encontrado: {elemento.text}")
                            return True
                except:
                    continue
            
            return False
        except:
            return False
    
    def validar_ruc(self, ruc):
        """Valida formato del RUC"""
        if not ruc or len(ruc) != 11 or not ruc.isdigit():
            return False
        
        try:
            factores = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
            suma = sum(int(ruc[i]) * factores[i] for i in range(10))
            resto = suma % 11
            digito_verificador = 11 - resto if resto >= 2 else resto
            return int(ruc[10]) == digito_verificador
        except:
            return False
    
    def close(self):
        """Cierra el driver"""
        if self.driver:
            self.driver.quit()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

# Función de uso fácil
def consultar_ruc_selenium(ruc, headless=True):
    """
    Función helper para consultar RUC con Selenium
    """
    logging.basicConfig(level=logging.INFO)
    
    with SunatSeleniumConsulta(headless=headless) as consultor:
        resultado = consultor.consultar_ruc(ruc)
        """
        if 'error' in resultado:
            print(f"❌ Error: {resultado['error']}")
        else:
            print("✅ Datos encontrados:")
            for campo, valor in resultado.items():
                print(f"  📋 {campo}: {valor}")
        """
        return resultado

# Ejemplo de uso
if __name__ == "__main__":
    # Necesitas tener chromedriver instalado
    # pip install selenium
    # También puedes usar webdriver-manager para instalar automáticamente:
    # pip install webdriver-manager
    
    #ruc_ejemplo = "20100047218"  # BCP
    ruc_ejemplo = "20613820001"
    resultado = consultar_ruc_selenium(ruc_ejemplo, headless=True)  # headless=False para ver el navegador