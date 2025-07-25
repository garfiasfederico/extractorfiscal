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
from selenium.webdriver.chrome.service import Service
import os,glob

log = Log("logs/extractor.log")

def renombra_ultima_descarga(repo, nuevo_nombre):
    files = glob.glob(repo + '/*')
    print( len(files))
    max_file = max(files, key=os.path.getctime)
    nombre_archivo = max_file.split("/")[-1]#.split(".")[0]
    nueva_ruta = max_file.replace(nombre_archivo, nuevo_nombre+".pdf")
    os.rename(max_file, nueva_ruta)
    return nueva_ruta

def getdeclaramensualesp(rfc_c:str,inicial:int,final:int):
    meses = {"Enero":"ene","Febrero":"feb","Marzo":"mar","Abril":"abr","Mayo":"may","Junio":"jun","Julio":"jul","Agosto":"ago","Septiembre":"sep","Octubre":"oct","Noviembre":"nov","Diciembre":"dic"}
    tipo_declaracion = {"Normal":"nor","Complementaria":"com"}
    archivos = []
    resultados = {}
    rfc = rfc_c
    descarga = "/root/"+rfc+"/DMP"
    folder_path = Path(descarga)
    folder_path.mkdir(parents=True, exist_ok=True)
    #for file in pathlib.Path(descarga).glob('*.*'):
    #    try:
    #        file.unlink()
    #    except:
    #        pass

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

        time.sleep(1);


        #inicializamos el navegador

        #driver.get('https://www.sat.gob.mx/personas/declaraciones')
        try:
            driver.get('https://ptscdecprov.clouda.sat.gob.mx/')
            log.write("info",f"Acceso al sitio del SAT, intento-declaraciones-provisionales-acuse {inicial}-{final}: {getdatacompany.contribuyente}")
            time.sleep(1);

            WebDriverWait(driver, 10)\
                .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                'button#buttonFiel')))\
                .click()
            log.write("info",f"{rfc} - Click en acceso por fiel")
            time.sleep(2)          
           
            js = "document.getElementById('fileCertificate').style.display = 'block';"
            driver.execute_script(js)
            WebDriverWait(driver, 15)\
                .until(EC.element_to_be_clickable((By.XPATH,
                                                '/html/body/main/div/div/div[1]/form/div[1]/div/input[2]')))\
                .send_keys(getdatacompany.path_cert)
            log.write("info",f"{rfc} - Seteo path del cert")
            time.sleep(3);
            js = "document.getElementById('filePrivateKey').style.display = 'block';"
            driver.execute_script(js)
            WebDriverWait(driver, 15)\
                .until(EC.element_to_be_clickable((By.XPATH,
                                                '/html/body/main/div/div/div[1]/form/div[2]/div/input[2]')))\
                .send_keys(getdatacompany.path_key)
            log.write("info",f"{rfc} - Seteo path del key")
            time.sleep(1);
            WebDriverWait(driver, 5)\
                .until(EC.element_to_be_clickable((By.XPATH,
                                                '/html/body/main/div/div/div[1]/form/div[3]/input')))\
                .send_keys(getdatacompany.password_fiel)
            log.write("info",f"{rfc} - Seteo password")

            time.sleep(1);

            WebDriverWait(driver,10)\
            .until(EC.element_to_be_clickable((By.XPATH,
                                            '/html/body/main/div/div/div[1]/form/div[5]/div/input[2]')))\
                                            .click()
            log.write("info",f"{rfc} - Click Acceso")
            time.sleep(1);

            try:
                if WebDriverWait(driver,3).until(EC.alert_is_present()) != None:                    
                    alert = driver.switch_to.alert
                    alert.dismiss()
            except:
                pass

            driver.get('https://ptscdecprov.clouda.sat.gob.mx/Paginas/ConsultaDeclaracionesPagadas.aspx')

            log.write("info",f"{rfc} - Acceso a de las declaraciones provisionales pagadas")
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

        time.sleep(3);

        anios = []
        for x in range(inicial,final+1):
            anios.append(x)

        moral2019 = 0;
        for i in anios:
            if i > 2021:
                #ACTUAL SITIO DE DESCARGA DE PROVISIONALES
                if moral2019==0:           
                    #accedemos al nuevo sitio de declaraciones que tiene la repo de los anios 2019 en adelante
                    time.sleep(3)          
                    driver.get('https://pstcdypisr.clouda.sat.gob.mx/')
                    time.sleep(3)
                    driver.get('https://pstcdypisr.clouda.sat.gob.mx/Consulta/Consulta?tipoDocumento=3')           
                    time.sleep(3)
                    moral2019=1
                
                                                            
                #comenzamos a iterar en las declaracion a partir del 2019
                select_2 = Select(WebDriverWait(driver,10)\
                .until(EC.element_to_be_clickable((By.ID,'Ejercicio'))))

                time.sleep(1)
                select_2.select_by_value(str(i))
                #click en el boton buscar de las declaraciones
                WebDriverWait(driver,10)\
                    .until(EC.element_to_be_clickable((By.ID,
                                                    'btnBuscar')))\
                                                    .click()  

                time.sleep(3)

                #Obtenemos las declaraciones del periodo    
                declaraciones_news = driver.find_elements(By.XPATH,"//*[@id='tableBody']/tr")
                
                print(f"Para {i}:existen {len(declaraciones_news)} para descargar")
                #sino existen declaraciones clickeamos el boton de cerrar en la ventana de resultado que informa que no existen declaraciones
                if len(declaraciones_news)==0:
                    WebDriverWait(driver,5)\
                        .until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[10]/div/div/div[3]/button"))).click()
                else:
                    #si existen declaraciones que descargar entonces comenzamos a iterar en la tabla correspodiente para la descarga de todas las declaraciones             
                    cuenta_n = 1;
                    for declara in declaraciones_news:
                        #obtenemos los campos para la construcción del nombre del archivo provisional
                        xoperacion = "/html/body/div[3]/div[10]/table/tbody/tr["+str(cuenta_n)+"]/td[2]"
                        xtipo = "/html/body/div[3]/div[10]/table/tbody/tr["+str(cuenta_n)+"]/td[3]"
                        xperiodo = "/html/body/div[3]/div[10]/table/tbody/tr["+str(cuenta_n)+"]/td[8]"
                        
                        op = WebDriverWait(driver,5)\
                            .until(EC.element_to_be_clickable((By.XPATH,xoperacion)))\
                                                        .text                
                        tip = WebDriverWait(driver,5)\
                            .until(EC.element_to_be_clickable((By.XPATH,xtipo)))\
                                                        .text
                        per = WebDriverWait(driver,5)\
                            .until(EC.element_to_be_clickable((By.XPATH,xperiodo)))\
                                                        .text
                        nombre_archivo = tipo_declaracion[tip] + "_" +meses[per]+"_"+op+"_"+str(i)
                        if not (os.path.exists(descarga+"/"+nombre_archivo+".pdf")):
                            time.sleep(2)                    
                            WebDriverWait(declara,5)\
                                .until(EC.element_to_be_clickable((By.ID,"linkDescargaPDF")))\
                                                            .click()
                            time.sleep(2)                    
                            renombra_ultima_descarga(descarga,nombre_archivo)
                            time.sleep(2)
                        cuenta_n = cuenta_n+1

                time.sleep(2)
                archivos = ""
                for pdf_file in pathlib.Path(descarga).glob(f'*{str(i)}*.pdf'):    
                    archivos = archivos + str(pdf_file) + "|"                      
                resultados[str(i)] = archivos
                #driver.close()
                #exit()                           
            else:

                #ANTERIOR SITIO DE DESCARGA DE PROVISIONALES
                select_ = Select(WebDriverWait(driver,10)\
                .until(EC.element_to_be_clickable((By.ID,'MainContent_wucConsultasDeclaracion_wucDdlEjercicioFiscal_ddlCatalogo'))))

                select_.select_by_value(str(i))
                log.write("info",f"{rfc} - Se selecciona anio:{i}")
                time.sleep(1)


                #Click en el botón buscar que es el mismo para persona moral y para persona fisica   
                WebDriverWait(driver,10)\
                .until(EC.element_to_be_clickable((By.ID,
                                                'MainContent_btnBuscar')))\
                                                .click()

                log.write("info",f"{rfc} - Click en Buscar")

                time.sleep(2)                                

                try:
                    #La tabla es la misma tanto para pesonas fisicas como morales
                    tabla = WebDriverWait(driver,1).until(EC.element_to_be_clickable((By.ID,'MainContent_wucConsultasDeclaracion_gvDeclaraciones')))            
                    
                    declaraciones_ = tabla.find_elements(By.TAG_NAME,"tr")
                    log.write("info",f"{rfc} - declaraciones localizadas: "+ str(len(declaraciones_)))
                    cuenta = -1;
                    time.sleep(2)                                        

                    for declara in declaraciones_:
                        if(cuenta!=-1):
                            nombre_archivo=""
                            xpatho = ""
                            xpatht = ""
                            xpathp = ""



                            xpatho = "/html/body/form/div[3]/div/div[3]/div/div/div/div[2]/div/div/div[1]/div/div[10]/div/div/table/tbody/tr["+str(cuenta+2)+"]/td[1]"
                            operacion = WebDriverWait(driver,5)\
                                .until(EC.element_to_be_clickable((By.XPATH,xpatho)))\
                                                            .text
                                
                            xpatht = "/html/body/form/div[3]/div/div[3]/div/div/div/div[2]/div/div/div[1]/div/div[10]/div/div/table/tbody/tr["+str(cuenta+2)+"]/td[2]"
                            tipo = WebDriverWait(driver,5)\
                                .until(EC.element_to_be_clickable((By.XPATH,xpatht)))\
                                                            .text
                        
                            xpathp = "/html/body/form/div[3]/div/div[3]/div/div/div/div[2]/div/div/div[1]/div/div[10]/div/div/table/tbody/tr["+str(cuenta+2)+"]/td[6]"
                            periodo = WebDriverWait(driver,5)\
                                .until(EC.element_to_be_clickable((By.XPATH,xpathp)))\
                                                            .text 
                            #print("Tipo: "+tipo_declaracion[tipo]+" Periodo:"+meses[periodo])
                            nombre_archivo = tipo_declaracion[tipo] + "_" +meses[periodo]+"_"+operacion+"_"+str(i)
                            #print(nombre_archivo)
                            

                            if not (os.path.exists(descarga+"/"+nombre_archivo+".pdf")):
                                WebDriverWait(driver,5)\
                                .until(EC.element_to_be_clickable((By.ID,"MainContent_wucConsultasDeclaracion_gvDeclaraciones_lbtnNumOp_"+str(cuenta))))\
                                                            .click()
                            
                                time.sleep(5)   
                                element = WebDriverWait(driver,10)\
                                .until(EC.element_to_be_clickable((By.ID,"btnDescargaPdf")))                                          

                                #driver.execute_script("arguments[0].scrollIntoView();", element)
                                driver.execute_script("window.scrollTo(0, 0);")
                                
                                element.click()
                                
                                time.sleep(20)                       

                                renombra_ultima_descarga(descarga,nombre_archivo)

                                time.sleep(2)
                    
                                WebDriverWait(driver,10)\
                                .until(EC.element_to_be_clickable((By.XPATH,"/html/body/form/div[3]/div/div[3]/div/div/div/div[3]/div/div[2]/div/input[2]")))\
                                                            .click()                 
                                                            
                                time.sleep(3)
                        cuenta = cuenta+1                                            
                    print(f"Existen Declaraciones que descargar para: {i}")
                    WebDriverWait(driver,10)\
                                .until(EC.element_to_be_clickable((By.ID,
                                                            'MainContent_btnCacelar')))\
                                                            .click()                                                              
                    archivos = ""
                    for pdf_file in pathlib.Path(descarga).glob(f'*{str(i)}*.pdf'):    
                        archivos = archivos + str(pdf_file) + "|"                      
                    resultados[str(i)] = archivos
                except TimeoutException:
                    #Si no existe la tabla de declaraciones entonces clic en el boton cancelar
                    WebDriverWait(driver,10)\
                                .until(EC.element_to_be_clickable((By.ID,
                                                            'MainContent_btnCacelar')))\
                                                            .click()                   
                    print(f"No Existen Declaraciones que Descargar para: {i}")
                    log.write("info",f"{rfc} - No Existen Declaraciones que Descargar para: {i}")                                                                                        
        time.sleep(2);         
        driver.close()
        return {
            "result" : "success",
            "message" : "Proceso concluido satisfactoriamente",
            "files": resultados
        }
    else:
        log.write("info",f"EL contribuyente: {rfc} no está registrado en la base!")                               
        return {
            "result" : "not_found",
            "message" : f"Contribuyente: {rfc} no localizado en la base",
            "files" : None
        }
