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
    time.sleep(3)

except Exception as ex:
    print("Ocurrio un error mientras se intentaba logear")
    log.write("error","No fue posible logearse, intentar mas tarde!")
    driver.close()
    exit()

try:
    print("Procedemos a realizar la consulta de los acuses correspondientes ")
    time.sleep(15)
    driver.get('https://wwwmat.sat.gob.mx/operacion/16203/consulta-tus-acuses-generados-en-la-aplicacion-contabilidad-electronica') 
    iframe = driver.find_element(By.ID, "iframetoload")    
    WebDriverWait(driver, 30).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "iframetoload")))           
    #driver.switch_to.frame(iframe)
    
    time.sleep(5)
    
    criterios = driver.find_element(By.ID,"rdoCriterios")
    criterios.click()
    
    
    #time.sleep(10)
    #comenzamos a iterar en las declaracion a partir del 2019
    resultados_p = {}
    anios = []
    for x in range(2015,2020+1):
        anios.append(x)

    for i in anios:
        #Si el archivo de meta de este anio esta creado entonces procedemos a eliminarlo

        try:
            if(os.path.exists(init.path_descarga+"/meta"+str(i)+".txt")):
                os.remove(init.path_descarga+"/meta"+str(i)+".txt")
        except:
            pass

        select1 = Select(WebDriverWait(driver,10)\
        .until(EC.element_to_be_clickable((By.ID,'ddlAnio'))))

        time.sleep(1)
        select1.select_by_value(str(i))

        select2 = Select(WebDriverWait(driver,10)\
        .until(EC.element_to_be_clickable((By.ID,'ddlMesInicio'))))

        time.sleep(1)
        select2.select_by_value("1")

        select3 = Select(WebDriverWait(driver,10)\
        .until(EC.element_to_be_clickable((By.ID,'ddlMesFin'))))    

        time.sleep(1)
        select3.select_by_value("13")

        select4 = Select(WebDriverWait(driver,10)\
        .until(EC.element_to_be_clickable((By.ID,'ddlMotivo'))))    

        time.sleep(1)
        select4.select_by_value("0")

        select5 = Select(WebDriverWait(driver,10)\
        .until(EC.element_to_be_clickable((By.ID,'ddlTipoArchivo'))))    

        time.sleep(1)
        select5.select_by_value("0")

        select6 = Select(WebDriverWait(driver,10)\
        .until(EC.element_to_be_clickable((By.ID,'ddlEstatus'))))    

        time.sleep(1)
        select6.select_by_value("0")

        #select7 = Select(WebDriverWait(driver,10)\
        #.until(EC.element_to_be_clickable((By.ID,'ddlTipoEnvio'))))    

        #time.sleep(1)
        #select7.select_by_value("0")

        WebDriverWait(driver,15)\
        .until(EC.element_to_be_clickable((By.ID,
                                        'btnBuscar')))\
                                        .click()

        time.sleep(5)


        

        registros = driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div/div/form/div/div[1]/label")
        dat = registros.text.split(":")

        if(dat[1].strip()!="0"):
            for file in pathlib.Path(init.path_descarga).glob(f'{init.rfc}{i}*.zip'):
                try:
                    file.unlink()
                except:
                    pass
            cuenta_n = 2
            print(f"Hay acuses que descargar para este periodo: {i}, acuses totales:{dat[1]}")
            #Procedemos a desacargas los archivos de contabilidad                        
            tabla_acuses = driver.find_elements(By.XPATH,"/html/body/div[1]/div[1]/div/div/form/div/div[2]/div/table/tbody/tr")  
            print(len(tabla_acuses))
            original_window = driver.current_window_handle
            if(len(tabla_acuses)>1):
                resultados_p[str(i)] = init.path_descarga+"/meta"+str(i)+".txt"
                for acu in tabla_acuses:
                    print(cuenta_n)
                    if(cuenta_n<=len(tabla_acuses)):
                        periodo = "/html/body/div[1]/div[1]/div/div/form/div/div[2]/div/table/tbody/tr["+str(cuenta_n)+"]/td[2]"
                        nombre_archivo = "/html/body/div[1]/div[1]/div/div/form/div/div[2]/div/table/tbody/tr["+str(cuenta_n)+"]/td[6]"
                        folio = "/html/body/div[1]/div[1]/div/div/form/div/div[2]/div/table/tbody/tr["+str(cuenta_n)+"]/td[7]"
                        estatus = "/html/body/div[1]/div[1]/div/div/form/div/div[2]/div/table/tbody/tr["+str(cuenta_n)+"]/td[9]"
                        
                        #procedemos a obtener los datos generales de cada registro
                        periodo_v_s = WebDriverWait(driver,5)\
                            .until(EC.element_to_be_clickable((By.XPATH,periodo)))
                                                        

                        periodo_v = WebDriverWait(driver,5)\
                            .until(EC.element_to_be_clickable((By.XPATH,periodo)))\
                                                        .text
                        
                        nombre_archivo_v = WebDriverWait(driver,5)\
                            .until(EC.element_to_be_clickable((By.XPATH,nombre_archivo)))\
                                                        .text
                        
                        folio_v = WebDriverWait(driver,5)\
                            .until(EC.element_to_be_clickable((By.XPATH,folio)))\
                                                        .text
                        
                        estatus_v = WebDriverWait(driver,5)\
                            .until(EC.element_to_be_clickable((By.XPATH,estatus)))\
                                                        .text


                        #colocamos el scroll en el elemento que corresponde para que pueda ser descargado
                        ActionChains(driver).move_to_element(periodo_v_s).perform()

                        #comenzamos a realizar la descarga de cada uno de los archivos contenidos por cada registro
                        xml = "/html/body/div[1]/div[1]/div/div/form/div/div[2]/div/table/tbody/tr["+str(cuenta_n)+"]/td[12]/img"  
                        sello_digital = "/html/body/div[1]/div[1]/div/div/form/div/div[2]/div/table/tbody/tr["+str(cuenta_n)+"]/td[13]/img"  


                        #Si el archivo Zip de la columna XML no ha sido descargado, entonces procedemos a descargarlo
                        #if not (os.path.exists(init.path_descarga+"/"+nombre_archivo_v)):
                        WebDriverWait(driver,5)\
                            .until(EC.element_to_be_clickable((By.XPATH,xml)))\
                                                            .click()
                    
                        time.sleep(3)
                        #Si el archivo xml que contiene el sello digital no ha sido descargado entonces lo descargamos    
                        if not (os.path.exists(init.path_descarga+"/SelloDigital_"+folio_v+".xml")):
                            WebDriverWait(driver,5)\
                                .until(EC.element_to_be_clickable((By.XPATH,sello_digital)))\
                                                            .click()
                            time.sleep(2)

                        if not (os.path.exists(init.path_descarga+"/AR_"+folio_v+".pdf")):
                            recepcion = "/html/body/div[1]/div[1]/div/div/form/div/div[2]/div/table/tbody/tr["+str(cuenta_n)+"]/td[10]/img"  
                            WebDriverWait(driver,5)\
                                .until(EC.element_to_be_clickable((By.XPATH,recepcion)))\
                                                            .click()
                            time.sleep(3)
                            #driver.switch_to.default_content()
                            all_windows = driver.window_handles
                            # Switch to the new window
                            for window_handle in all_windows:
                                if window_handle != original_window:
                                    driver.switch_to.window(window_handle)
                                    break
                            
                            src = WebDriverWait(driver,5)\
                                .until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/div/iframe")))\
                                                            .get_attribute("src")
                            
                            #print(src)
                            driver.get(src)
                            time.sleep(3)                          
                            WebDriverWait(driver,5)\
                                .until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/div/div/input")))\
                                                            .click()
                            driver.switch_to.window(original_window)
                            driver.switch_to.frame(iframe)

                            time.sleep(2)

                        #Si el archivo del resultado de la recepción no ha sido descargado entonces lo descargamos
                        nombre_resultado = "APA_" if(estatus_v=="Aceptado") else "APR_"
                        nombre_resultado = nombre_resultado + folio_v + ".pdf"    
                        if not (os.path.exists(init.path_descarga+"/"+nombre_resultado)):
                            resultados = "/html/body/div[1]/div[1]/div/div/form/div/div[2]/div/table/tbody/tr["+str(cuenta_n)+"]/td[11]/img"  
                            WebDriverWait(driver,5)\
                                .until(EC.element_to_be_clickable((By.XPATH,resultados)))\
                                                            .click()
                            time.sleep(3)
                            #driver.switch_to.default_content()
                            all_windows = driver.window_handles
                            # Switch to the new window
                            for window_handle in all_windows:
                                if window_handle != original_window:
                                    driver.switch_to.window(window_handle)
                                    break
                            
                            src = WebDriverWait(driver,5)\
                                .until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/div/iframe")))\
                                                            .get_attribute("src")
                            
                            #print(src)
                            driver.get(src)
                            time.sleep(3)                          
                            WebDriverWait(driver,5)\
                                .until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/div/div/input")))\
                                                            .click()
                            driver.switch_to.window(original_window)
                            driver.switch_to.frame(iframe)
                        registro = folio_v +"|"+estatus_v+"&"
                        writeMeta(init.path_descarga+"/meta"+str(i)+".txt",registro)
                        cuenta_n = cuenta_n + 1                                                                                                            
        else:
            resultados_p[str(i)] = "Sin acuses de contabililidad"
            print(f"No se presento informacion para este periodo: {i}")                               
        
    time.sleep(5)
    print (resultados_p)    
except Exception as ex:
    traceback.print_exc()
    print("Error")
    driver.close()
    exit()

driver.close()
exit()