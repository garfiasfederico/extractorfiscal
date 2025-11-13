from selenium import webdriver;
from selenium.webdriver.support.ui import WebDriverWait;
from selenium.webdriver.support import expected_conditions as EC;
from selenium.webdriver.common.by import By;
from selenium.webdriver.common.action_chains import ActionChains
import time;
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
import init
import requests
from clases.logs import Log
import traceback
import os,glob
import pathlib
from clases.metas import writeMeta

log = Log("logs/log_constancia.log")

options = webdriver.ChromeOptions() #Options()
prefs = {
        'download.default_directory' : init.path_descarga,
        'download.prompt_for_download': False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True,
        "safebrowsing.enabled": True
         }
options.add_experimental_option('prefs', prefs)
#options.add_argument("--user-data-dir=/tmp/selenium-user-data/")
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
#options.add_argument('--headless=new')
#options.add_argument('--disable-gpu')
#options.add_argument('--disable-extensions')
#options.add_argument('--remote-debugging-port=9222')  # Specify a port
#options.add_argument('--disable-setuid-sandbox')
#options.add_argument("--incognito")
#options.add_argument("--disable-application-cache")
#options.add_argument("--enable-do-not-track")
#options.add_argument("--disable-popup-blocking")
#service = Service('/usr/bin/chromedriver')
#options.add_argument('--headless')
driver = webdriver.Chrome(options=options);

try:
    driver.get('https://wwwmat.sat.gob.mx/personas/iniciar-sesion')
    log.write("info",f"Acceso al buzón tributario, intento: {init.rfc}")
    time.sleep(5);

    iframe = driver.find_element(By.ID, "iframetoload")
    driver.switch_to.frame(iframe)

    WebDriverWait(driver, 10)\
        .until(EC.element_to_be_clickable((By.ID,
                                        'buttonFiel')))\
        .click()
    log.write("info","Click en acceso por fiel")
    time.sleep(2);
    js = "document.getElementById('fileCertificate').style.display = 'block';"
    driver.execute_script(js)
    WebDriverWait(driver, 15)\
        .until(EC.element_to_be_clickable((By.XPATH,
                                        '/html/body/main/div/div/div[1]/form/div[1]/div/input[2]')))\
        .send_keys(init.path_cert)
    log.write("info","Seteo path del cert")
    time.sleep(3);
    js = "document.getElementById('filePrivateKey').style.display = 'block';"
    driver.execute_script(js)
    WebDriverWait(driver, 15)\
        .until(EC.element_to_be_clickable((By.XPATH,
                                        '/html/body/main/div/div/div[1]/form/div[2]/div/input[2]')))\
        .send_keys(init.path_key)
    log.write("info","Seteo path del key")
    time.sleep(1);
    WebDriverWait(driver, 15)\
        .until(EC.element_to_be_clickable((By.XPATH,
                                        '/html/body/main/div/div/div[1]/form/div[3]/input')))\
        .send_keys(init.password)
    log.write("info","Seteo password")

    time.sleep(1);

    WebDriverWait(driver,15)\
    .until(EC.element_to_be_clickable((By.XPATH,
                                    '/html/body/main/div/div/div[1]/form/div[5]/div/input[2]')))\
                                    .click()
    log.write("info","Click Acceso")
    time.sleep(3)

    error_login = ""

except Exception as ex:
    traceback.print_exc()
    print("Ocurrio un error mientras se intentaba logear")
    log.write("error","No fue posible logearse, intentar mas tarde!")
    driver.close()
    exit()

if(error_login==""):
    try:    
        print("Procedemos a realizar la consulta de los documentos de los expedientes")
        time.sleep(15)
        driver.get('https://wwwmat.sat.gob.mx/iniciar-expediente/mis-documentos/') 
        #iframe = driver.find_element(By.ID, "iframetoload")  
        iframe = WebDriverWait(driver, 15)\
                            .until(EC.element_to_be_clickable((By.ID,
                                                            'iframetoload')))

        WebDriverWait(driver, 30).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "iframetoload")))           
        #driver.switch_to.frame(iframe)
        
        time.sleep(5)
        
        #Documentos de Cobranza en el buzon tributario
        array_lineas_captura = []

        criterios = driver.find_element(By.ID,"aClasificadorCinco")
        criterios.click()
        
        
        time.sleep(5)


        lineas_captura = driver.find_element(By.ID,"lvClasificadorCinco_ctrl0_lknBtnVerDetalleFive")
        lineas_captura.click()

        time.sleep(5)

        resultado_lineas_captura = driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr/td[2]/div/div[2]/div[1]/div[2]/div/table/tbody/tr/td").text
        if(resultado_lineas_captura=="No existe información"):
            array_lineas_captura = None
        else:
            array_lineas_captura.append(1)    
        
        print(array_lineas_captura)
        time.sleep(5)


        #comenzamos a iterar en las declaracion a partir del 2019
        resultados_p = {}         
    except Exception as ex:
        traceback.print_exc()
        print("Error")
        #driver.close()
        exit()

driver.close()
exit()