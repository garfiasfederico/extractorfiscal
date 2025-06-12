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
import pathlib


log = Log("logs/log_declaraciones.log")

def getdeclaraanuales(rfc_c:str,inicial:int,final:int):
    archivos = []
    rfc = rfc_c
    descarga = "/root/"+rfc
    folder_path = Path(descarga)
    folder_path.mkdir(parents=True, exist_ok=True)

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
        driver = webdriver.Chrome(options=options);


        #Inicializar en la pantalla 2 

        #driver.set_window_position(2000,0)
        #driver.maximize_window();
        #driver.minimize_window()
        time.sleep(1);


        #inicializamos el navegador

        #driver.get('https://www.sat.gob.mx/personas/declaraciones')
        try:
            driver.get('https://anualpf.clouda.sat.gob.mx/')
            log.write("info",f"Acceso al sitio del SAT, intento: {getdatacompany.contribuyente}")
            time.sleep(1);

            WebDriverWait(driver, 10)\
                .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                'button#buttonFiel')))\
                .click()
            log.write("info","Click en acceso por fiel")
            time.sleep(2);
            time.sleep(1);
            #pyautogui.write(u"E:\\Dropbox\\FIEL_SAGF8705279C8_20190131113307\\NUEVA_FIEL_SAGF870527\\C00001000000517898266.cer",interval=.08)
            #pyautogui.write(init.path_cert,interval=.08)
            #time.sleep(1);
            #pyautogui.press('enter')
            #time.sleep(4);
            js = "document.getElementById('fileCertificate').style.display = 'block';"
            driver.execute_script(js)
            WebDriverWait(driver, 15)\
                .until(EC.element_to_be_clickable((By.XPATH,
                                                '/html/body/main/div/div/div[1]/form/div[1]/div/input[2]')))\
                .send_keys(getdatacompany.path_cert)
            log.write("info","Seteo path del cert")
            time.sleep(3);
            js = "document.getElementById('filePrivateKey').style.display = 'block';"
            driver.execute_script(js)
            WebDriverWait(driver, 15)\
                .until(EC.element_to_be_clickable((By.XPATH,
                                                '/html/body/main/div/div/div[1]/form/div[2]/div/input[2]')))\
                .send_keys(getdatacompany.path_key)
            log.write("info","Seteo path del key")
            time.sleep(1);
            WebDriverWait(driver, 5)\
                .until(EC.element_to_be_clickable((By.XPATH,
                                                '/html/body/main/div/div/div[1]/form/div[3]/input')))\
                .send_keys(getdatacompany.password_fiel)
            log.write("info","Seteo password")

            time.sleep(1);

            WebDriverWait(driver,10)\
            .until(EC.element_to_be_clickable((By.XPATH,
                                            '/html/body/main/div/div/div[1]/form/div[5]/div/input[2]')))\
                                            .click()
            log.write("info","Click Acceso")
            time.sleep(1);

            WebDriverWait(driver,30)\
            .until(EC.element_to_be_clickable((By.XPATH,
                                            '/html/body/div[1]/div/ul/li[2]/a')))\
                                            .click()
            log.write("info","Click en Declaraciones Anuales")
            time.sleep(1);
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



        anios = []
        for x in range(inicial,final+1):
            anios.append(x)


        for i in anios:
            select_ = Select(WebDriverWait(driver,10)\
            .until(EC.element_to_be_clickable((By.ID,'IdEjercicio'))))

            select_.select_by_value(str(i))
            log.write("info",f"Se selecciona anio:{i}")
            time.sleep(1)

            if persona == "fisica":
                WebDriverWait(driver,10)\
                .until(EC.element_to_be_clickable((By.XPATH,
                                                '/html/body/div[1]/div/form/div/div[2]/div/div[6]/div[2]/button[1]')))\
                                                .click()
                
            else:
                WebDriverWait(driver,10)\
                .until(EC.element_to_be_clickable((By.XPATH,
                                                '/html/body/div[2]/div/form/div/div[2]/div/div[6]/div[2]/button[1]')))\
                                                .click()

            log.write("info","Click en Buscar")
            time.sleep(3)

            try:
                if persona=="fisica":
                    tabla = WebDriverWait(driver,1).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div/form/div/div[3]/div[2]')))
                else:
                    tabla = WebDriverWait(driver,1).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/div/form/div/div[3]/div[2]')))
                
                declaraciones_ = driver.find_elements(By.XPATH,"//*[@id='accordion']/div")        
                log.write("info","declaraciones localizadas: "+ str(len(declaraciones_)))
                time.sleep(2)

                for declara in declaraciones_:

                    WebDriverWait(declara,5)\
                    .until(EC.element_to_be_clickable((By.CSS_SELECTOR,"img[alt='Generar pdf']")))\
                                                .click()
                    
                    iframe = driver.find_element(By.ID, "iframePdf")
                    driver.switch_to.frame(iframe)

                    body = WebDriverWait(driver,5)\
                    .until(EC.element_to_be_clickable((By.XPATH,"/html/body")))\
                                                .text                    
                    
                    driver.switch_to.default_content()

                    time.sleep(2)
                    if(body.strip()!="No se puede generar el archivo de la declaración. Inténtelo nuevamente"):
                        if(persona=="fisica"):
                            WebDriverWait(driver,10)\
                            .until(EC.element_to_be_clickable((By.XPATH,
                                                        '/html/body/div[6]/div/div/div[2]/button[2]')))\
                                                        .click()
                        else:
                            WebDriverWait(driver,10)\
                            .until(EC.element_to_be_clickable((By.XPATH,
                                                        '/html/body/div[7]/div/div/div[2]/button[2]')))\
                                                        .click()                                          
                    time.sleep(2)

                    if(persona=="fisica"):
                        WebDriverWait(driver,10)\
                        .until(EC.element_to_be_clickable((By.XPATH,
                                                    '/html/body/div[6]/div/div/div[2]/button[1]')))\
                                                    .click()
                    else:
                        WebDriverWait(driver,10)\
                        .until(EC.element_to_be_clickable((By.XPATH,
                                                    '/html/body/div[7]/div/div/div[2]/button[1]')))\
                                                    .click()
                
                print(f"Existen Declaraciones que descargar para: {i}")
                for pdf_file in pathlib.Path(descarga).glob(f'*{str(i)}*.pdf'):    
                    archivos.append(parsepdf.pdf_to_base64(pdf_file))
            except TimeoutException:
                if(persona=="fisica"):
                    WebDriverWait(driver,10)\
                    .until(EC.element_to_be_clickable((By.XPATH,
                                                '/html/body/div[3]/div/div/div[2]/button')))\
                                                .click()        
                else:
                    WebDriverWait(driver,10)\
                    .until(EC.element_to_be_clickable((By.XPATH,
                                                '/html/body/div[4]/div/div/div[2]/button')))\
                                                .click()                    
                print(f"No Existen Declaraciones que Descargar para: {i}")
                log.write("info",f"No Existen Declaraciones que Descargar para: {i}")                                                                                        
        time.sleep(2); 
        driver.close()          
        return {
            "result" : "success",
            "message" : "Proceso concluido satisfactoriamente",
            "files": archivos
        }
    else:
        log.write("info",f"EL contribuyente: {rfc} no está registrado en la base!")                               
        return {
            "result" : "not_found",
            "message" : f"Contribuyente: {rfc} no localizado en la base",
            "files" : None
        }
