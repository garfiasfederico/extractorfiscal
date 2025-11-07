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

log = Log("logs/extract.log")

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

    driver.get('https://rpc.economia.gob.mx/siger2/xhtml/login/login2.xhtml')
    log.write("info",f"Acceso al SIGER 2.0, intento-SIGER: {init.rfc}")
    time.sleep(3);
   # WebDriverWait(driver, 10)\
   #     .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
   #                                     'button#buttonFiel')))\
   #     .click()
   # log.write("info","Click en acceso por fiel")
   # time.sleep(2);
    
    WebDriverWait(driver, 15)\
        .until(EC.element_to_be_clickable((By.ID,
                                        'formulario:usuario')))\
        .send_keys("motogruassanchez@gmail.com")
    log.write("info","Seteo de la contrasenia")
    time.sleep(5);

    WebDriverWait(driver, 15)\
        .until(EC.element_to_be_clickable((By.ID,
                                        'formulario:contrasenia')))\
        .send_keys("F3d3r1k01987g#")
    log.write("info","Seteo de la contrasenia")


    captcha = WebDriverWait(driver, 15)\
        .until(EC.element_to_be_clickable((By.ID,
                                        'formulario:mainCaptcha')))\
        .text
    
    WebDriverWait(driver, 15)\
        .until(EC.element_to_be_clickable((By.ID,
                                        'formulario:txtInput')))\
        .send_keys(captcha)
    
    log.write("info","Seteo de captcha")

    WebDriverWait(driver, 15)\
        .until(EC.element_to_be_clickable((By.XPATH,
                                        '/html/body/main/div/div[3]/div/form/div[4]/div/div[2]')))\
        .click()

    
    


    time.sleep(5);
except Exception as Ex:
    pass