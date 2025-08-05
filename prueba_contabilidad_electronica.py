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

log = Log("logs/log_constancia.log")

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
#options.add_argument('--headless')
driver = webdriver.Chrome(options=options);

try:
    driver.get('https://wwwmat.sat.gob.mx/consultas/login/16203/consulta-tus-acuses-generados-en-la-aplicacion-contabilidad-electronica')
    log.write("info",f"Acceso al sitio del SAT, intento: {init.rfc}")
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
    time.sleep(5)

except Exception as ex:
    log.write("error","No fue posible logearse, intentar mas tarde!")

try:
    print(driver)
    
    WebDriverWait(driver,15)\
    .until(EC.element_to_be_clickable((By.ID,
                                    'rdoCriterios')))\
                                    .click()
    
    time.sleep(10)
    #comenzamos a iterar en las declaracion a partir del 2019
    select1 = Select(WebDriverWait(driver,10)\
    .until(EC.element_to_be_clickable((By.ID,'ddlAnio'))))

    time.sleep(1)
    select1.select_by_value("2015")

    select2 = Select(WebDriverWait(driver,10)\
    .until(EC.element_to_be_clickable((By.ID,'ddlMesInicio'))))

    time.sleep(1)
    select2.select_by_value("1")

    select3 = Select(WebDriverWait(driver,10)\
    .until(EC.element_to_be_clickable((By.ID,'ddlMesFin'))))

    time.sleep(1)
    select3.select_by_value("13")
    time.sleep(10)


    


except:
    print("ocurrio un error!")
    pass