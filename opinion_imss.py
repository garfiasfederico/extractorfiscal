from selenium import webdriver;
from selenium.webdriver.support.ui import WebDriverWait;
from selenium.webdriver.support import expected_conditions as EC;
from selenium.webdriver.common.by import By;
import time;
import pandas as pd;
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
import getdatacompany
from clases.logs import Log
from pathlib import Path
from selenium.common.exceptions import InvalidArgumentException
import parsepdf
import pathlib, os
from selenium.webdriver.chrome.service import Service

log = Log("logs/extractor.log")

def getopinionimss(rfc_c:str):
    resultados = {}
    rfc = rfc_c
    descarga = "/root/"+rfc+"/IMSS"
    folder_path = Path(descarga)
    folder_path.mkdir(parents=True, exist_ok=True)
    for file in pathlib.Path(descarga).glob('*.*'):
        try:
            file.unlink()
        except:
            pass

    getdatacompany.getDataCompany(rfc)
    if(getdatacompany.contribuyente!=""):
        persona = "moral" if len(getdatacompany.contribuyente)==12 else "fisica"
        #Opciones de navegacion

        options = webdriver.ChromeOptions() #Options()
        prefs = {'download.default_directory' : descarga}
        options.add_experimental_option('prefs', prefs)
        #options.add_argument("--user-data-dir=/tmp/selenium-user-data/")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')
        service = Service('/usr/bin/chromedriver')
        driver = webdriver.Chrome(service=service,options=options);

        try:
            driver.get('https://buzon.imss.gob.mx/buzonimss/login')
            log.write("info",f"Acceso a buzon imss, intento: {getdatacompany.contribuyente}")
            time.sleep(5);

            iframe = driver.find_element(By.ID, "formFirmaDigital")
            driver.switch_to.frame(iframe)

            WebDriverWait(driver, 10)\
                .until(EC.element_to_be_clickable((By.ID,
                                                'inputRFC')))\
                .send_keys(getdatacompany.contribuyente)   
            
            WebDriverWait(driver, 15)\
                .until(EC.element_to_be_clickable((By.ID,
                                                'inputCertificado')))\
                .send_keys(getdatacompany.path_cert)
            log.write("info","Seteo path del cert")
            time.sleep(5)

            
            WebDriverWait(driver, 15)\
                .until(EC.element_to_be_clickable((By.ID,
                                                'inputKey')))\
                .send_keys(getdatacompany.path_key)
            log.write("info","Seteo path del key")
            time.sleep(1);
            WebDriverWait(driver, 15)\
                .until(EC.element_to_be_clickable((By.ID,
                                                'inputPassword')))\
                .send_keys(getdatacompany.password_fiel)
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
            return {
                    "result" : "error",
                    "message" : "No fue posible logearse en buzon IMSS, intente más tarde!",
                    "doc": None
                }              
        
        try:              
            log.write("info",f"Procedemos a la descarga del documento de opinion: {getdatacompany.contribuyente}")
            time.sleep(15)
            driver.get('https://buzon.imss.gob.mx/buzonimss/opinionCumplimiento/consultaMiOpinion') 
            WebDriverWait(driver,5)\
                        .until(EC.element_to_be_clickable((By.XPATH,"/html/body/main/div[3]/div/form/div/div/div[2]/div/a")))\
                                                        .click()
            time.sleep(15)
            doc=""
            path_doc_opinion = descarga + "/MiOpinion_"+ getdatacompany.contribuyente + ".pdf"
            if(os.path.exists(path_doc_opinion)):
                            doc = parsepdf.pdf_to_base64(path_doc_opinion)

            return {
                    "result" : "success",
                    "message" : "El documento de opinión ha sido descargado satisfactoriamente!",
                    "doc":  doc
                }

        except TimeoutException as ex:
            driver.close()
            return {
                    "result" : "error",
                    "message" : "No fue posible logearse en buzon IMSS, intente más tarde!",
                    "doc": None
                } 
    else:
        log.write("info",f"EL contribuyente: {rfc} no está registrado en la base!")    
        driver.close()                           
        return {
            "result" : "not_found",
            "message" : f"Contribuyente: {rfc} no localizado en la base",
            "doc" : None
        }
