from selenium import webdriver;
from selenium.webdriver.support.ui import WebDriverWait;
from selenium.webdriver.support import expected_conditions as EC;
from selenium.webdriver.common.by import By;
import time;
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
import init
import requests
from clases.logs import Log
import getdatacompany
from selenium.common.exceptions import InvalidArgumentException
import parsepdf
import pathlib
from pathlib import Path

log = Log("logs/log_constancia.log")

def getcsf(rfc_c:str):
    archivos = []
    rfc = rfc_c
    descarga = "/root/"+rfc+"/CSF"
    folder_path = Path(descarga)
    folder_path.mkdir(parents=True, exist_ok=True)

    getdatacompany.getDataCompany(rfc)
    if(getdatacompany.contribuyente!=""):    
        options = webdriver.ChromeOptions() #Options()
        prefs = {
                'download.default_directory' : init.path_descarga,
                'download.prompt_for_download': False,
                "download.directory_upgrade": True,
                "plugins.always_open_pdf_externally": True
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
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options);

        try:

            driver.get('https://wwwmat.sat.gob.mx/app/seg/faces/pages/lanzador.jsf?url=/operacion/43824/reimprime-tus-acuses-del-rfc&tipoLogeo=c&target=principal&hostServer=https://wwwmat.sat.gob.mx')
            log.write("info",f"Acceso al sitio del SAT, intento: {init.rfc}")
            time.sleep(1);

            WebDriverWait(driver, 10)\
                .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                'button#buttonFiel')))\
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
            time.sleep(5);
        
        except InvalidArgumentException as ex:
            return {
                "result" : "error",
                "message" : "La ruta de la fiel es incorrecta",
                "files" : None
            }
        except TimeoutException as ext:
            return {
                    "result" : "error",
                    "message" : "No fue posible logearse correctamente",
                    "files": None
                }

        try:
            #Procedemos a cambiar el foco del driver hacia el Iframe
            iframe = driver.find_element(By.TAG_NAME, "iframe")
            driver.switch_to.frame(iframe)

            WebDriverWait(driver,50)\
            .until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div[2]/form/table/tbody/tr[6]/td[5]/button[3]')))\
                .click()
            log.write("info","Click descarga de Constancia")
            time.sleep(10);
            driver.switch_to.default_content()
            driver.close()
            time.sleep(5);
            for pdf_file in pathlib.Path(descarga).glob('SAT.pdf'):    
                    archivos.append(parsepdf.pdf_to_base64(pdf_file))
            return {
                "result" : "success",
                "message" : "Constancia de Situacion fiscal descaragada Satisfactoriamente!",
                "files" : archivos
            }
        except:
            driver.close()
            log.write(f"error","No se pudo realizar la descarga de la Constancia de Situación Fiscal")
            return {
                "result" : "error",
                "message" : "No se pudo realizar la descarga de la Constancia de Situación Fiscal",
                "files" : None
            }
    else:
        log.write("info",f"EL contribuyente: {rfc} no está registrado en la base!")                               
        return {
            "result" : "not_found",
            "message" : f"Contribuyente: {rfc} no localizado en la base",
            "files" : None
        }
    


    
