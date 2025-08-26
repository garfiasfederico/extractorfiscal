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
import parsepdf

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

for file in pathlib.Path(init.path_descarga).glob('*.*'):
        try:
            file.unlink()
        except:
            pass
try:
    driver.get('https://buzon.imss.gob.mx/buzonimss/login')
    log.write("info",f"Acceso a buzon imss, intento: {init.rfc}")
    time.sleep(5);

    iframe = driver.find_element(By.ID, "formFirmaDigital")
    driver.switch_to.frame(iframe)

    WebDriverWait(driver, 10)\
        .until(EC.element_to_be_clickable((By.ID,
                                        'inputRFC')))\
        .send_keys(init.rfc)   
    
    WebDriverWait(driver, 15)\
        .until(EC.element_to_be_clickable((By.ID,
                                        'inputCertificado')))\
        .send_keys(init.path_cert)
    log.write("info","Seteo path del cert")
    time.sleep(5)

    
    WebDriverWait(driver, 15)\
        .until(EC.element_to_be_clickable((By.ID,
                                        'inputKey')))\
        .send_keys(init.path_key)
    log.write("info","Seteo path del key")
    time.sleep(1);
    WebDriverWait(driver, 15)\
        .until(EC.element_to_be_clickable((By.ID,
                                        'inputPassword')))\
        .send_keys(init.password)
    log.write("info","Seteo password")

    time.sleep(1);

    WebDriverWait(driver,15)\
    .until(EC.element_to_be_clickable((By.ID,
                                    'botonValidarCert')))\
                                    .click()
    log.write("info","Click Acceso")
    time.sleep(3)
    
except Exception as ex:
    print("Ocurrio un error mientras se intentaba logear en el sitio del buzon del IMSS")
    log.write("error","No fue posible logearse, intentar mas tarde!")
    driver.close()
    exit()

try:    
    print("Procedemos a la descarga del documento de opinion")
    time.sleep(15)
    driver.get('https://buzon.imss.gob.mx/buzonimss/opinionCumplimiento/consultaMiOpinion') 
    WebDriverWait(driver,5)\
                .until(EC.element_to_be_clickable((By.XPATH,"/html/body/main/div[3]/div/form/div/div/div[2]/div/a")))\
                                                   .click()
    time.sleep(30)
    doc=""
    path_doc_opinion = init.path_descarga + "/MiOpinion_"+ init.rfc + ".pdf"

    for i in range(0,5):
        if(os.path.exists(path_doc_opinion)):
            doc = parsepdf.pdf_to_base64(path_doc_opinion)
            break;
        else:
            time.sleep(10)


    print(doc)
except TimeoutException as ex:
    #traceback.print_exc()
    print("Este contribuyente no cuenta con la descarga del documento de opinión")
    driver.close()
    exit()

driver.close()
exit()