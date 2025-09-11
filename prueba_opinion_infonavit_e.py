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
options.add_argument("--incognito")
options.add_argument("--disable-application-cache")
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
    driver.get('https://empresarios.infonavit.org.mx/')
    log.write("info",f"Acceso a buzon INFONAVIT, intento: {init.rfc}")
    time.sleep(5);
    
    
    WebDriverWait(driver, 15)\
        .until(EC.element_to_be_clickable((By.ID,
                                        'nrp')))\
        .send_keys("J2517061102")
    
    
    WebDriverWait(driver, 15)\
        .until(EC.element_to_be_clickable((By.ID,
                                        'correo')))\
        .send_keys("grupo.constructorcica@gmail.com")
    
    WebDriverWait(driver, 15)\
        .until(EC.element_to_be_clickable((By.ID,
                                        'pwd')))\
        .send_keys("Cicofi204.")

    time.sleep(5)    
    #captcha = WebDriverWait(driver, 15)\
    #    .until(EC.element_to_be_clickable((By.XPATH,
    #                                    '//*[@id="root"]/div[1]/div[2]/div/div[5]/div/div[1]/svg/text')))\
    #    .text
    
    svg_text_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[local-name()='svg']//*[local-name()='text']"))
        )
    text_content = svg_text_element.text
    
    WebDriverWait(driver, 15)\
        .until(EC.element_to_be_clickable((By.NAME,
                                        'captchaInput')))\
        .send_keys(text_content)
    

    WebDriverWait(driver, 15)\
        .until(EC.element_to_be_clickable((By.XPATH,
                                        '/html/body/div/div[1]/div[2]/div/div[6]/button[1]')))\
        .click()
    

    
    time.sleep(10)
    
    
except Exception as ex:
    traceback.print_exc()
    print("Ocurrio un error mientras se intentaba logear en el sitio del buzon del IMSS")
    log.write("error","No fue posible logearse, intentar mas tarde!")
    driver.close()
    exit()

