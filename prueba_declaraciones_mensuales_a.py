from selenium import webdriver;
from selenium.webdriver.support.ui import WebDriverWait;
from selenium.webdriver.support import expected_conditions as EC;
from selenium.webdriver.common.by import By;
import time;
import pandas as pd;
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
import init
import pathlib
import parsepdf
import time
import os,glob


def renombra_ultima_descarga(repo, nuevo_nombre):
    files = glob.glob(repo + '/*')
    print( len(files))
    max_file = max(files, key=os.path.getctime)
    nombre_archivo = max_file.split("/")[-1]#.split(".")[0]
    nueva_ruta = max_file.replace(nombre_archivo, nuevo_nombre+".pdf")
    os.rename(max_file, nueva_ruta)
    return nueva_ruta


meses = {"Enero":"ene","Febrero":"feb","Marzo":"mar","Abril":"abr","Mayo":"may","Junio":"jun","Julio":"jul","Agosto":"ago","Septiembre":"sep","Octubre":"oct","Noviembre":"nov","Diciembre":"dic"}
tipo_declaracion = {"Normal":"nor","Complementaria":"com"}
archivos = []
persona = "moral" if len(init.rfc)==12 else "fisica"
resultados = {}
#Opciones de navegacion
for file in pathlib.Path(init.path_descarga).glob('*.*'):
        try:
            file.unlink()
        except:
            pass

options = webdriver.ChromeOptions() #Options()
prefs = {'download.default_directory' : init.path_descarga}
options.add_experimental_option('prefs', prefs)
#options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options);

time.sleep(1);


#inicializamos el navegador

driver.get('https://ptscdecprov.clouda.sat.gob.mx/')

time.sleep(1);

WebDriverWait(driver, 10)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                      'button#buttonFiel')))\
    .click()

time.sleep(3);

js = "document.getElementById('fileCertificate').style.display = 'block';"
driver.execute_script(js)
WebDriverWait(driver, 15)\
    .until(EC.element_to_be_clickable((By.XPATH,
                                      '/html/body/main/div/div/div[1]/form/div[1]/div/input[2]')))\
    .send_keys(init.path_cert)

time.sleep(3);
js = "document.getElementById('filePrivateKey').style.display = 'block';"
driver.execute_script(js)
WebDriverWait(driver, 15)\
    .until(EC.element_to_be_clickable((By.XPATH,
                                      '/html/body/main/div/div/div[1]/form/div[2]/div/input[2]')))\
    .send_keys(init.path_key)

time.sleep(1);
WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.XPATH,
                                      '/html/body/main/div/div/div[1]/form/div[3]/input')))\
    .send_keys(init.password)


time.sleep(1);

WebDriverWait(driver,10)\
.until(EC.element_to_be_clickable((By.XPATH,
                                  '/html/body/main/div/div/div[1]/form/div[5]/div/input[2]')))\
                                  .click()
time.sleep(3);


try:
    if WebDriverWait(driver,3).until(EC.alert_is_present()) != None:
        print ("Alert is present")
        print ("Alert closed")
        alert = driver.switch_to.alert
        alert.dismiss()
except:
    pass

driver.get('https://ptscdecprov.clouda.sat.gob.mx/Paginas/ReimpresionAcuse.aspx')

time.sleep(3);


anios = []
for x in range(2018,2018+1):
    anios.append(x)
print(anios)
moral2019 = 0;

for i in anios:

    if i > 2021: #and persona=="moral":
        #ACTUAL SITIO DE DESCARGA DE PROVISIONALES
        if moral2019==0:           
           #accedemos al nuevo sitio de declaraciones que tiene la repo de los anios 2019 en adelante
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

                time.sleep(2)                    
                WebDriverWait(declara,5)\
                    .until(EC.element_to_be_clickable((By.ID,"linkDescargaPDF")))\
                                                .click()
                time.sleep(2)                    
                renombra_ultima_descarga(init.path_descarga,nombre_archivo)
                time.sleep(2)
                cuenta_n = cuenta_n+1

        time.sleep(2)
        archivos = ""
        for pdf_file in pathlib.Path(init.path_descarga).glob(f'*{str(i)}*.pdf'):    
            archivos = archivos + str(pdf_file) + "|"                      
        resultados[str(i)] = archivos
        #driver.close()
        #exit()
    else:    
        #ANTERIOR SITIO DE DESCARGA DE PROVISIONALES
        select_ = Select(WebDriverWait(driver,10)\
        .until(EC.element_to_be_clickable((By.ID,'MainContent_wucConsultasDeclaracion_wucDdlEjercicioFiscal_ddlCatalogo'))))

        select_.select_by_value(str(i))
        time.sleep(1)


        #Click en el botón buscar que es el mismo para persona moral y para persona fisica   
        WebDriverWait(driver,10)\
        .until(EC.element_to_be_clickable((By.ID,
                                        'MainContent_btnBuscar')))\
                                        .click()

        
        time.sleep(10)
        

        try:
            
            #La tabla es la misma tanto para pesonas fisicas como morales
            tabla = WebDriverWait(driver,1).until(EC.element_to_be_clickable((By.ID,'MainContent_wucConsultasDeclaracion_gvDeclaraciones')))                                                                                     
            declaraciones_ = tabla.find_elements(By.TAG_NAME,"tr")
            print("declaraciones provisionales: "+ str(len(declaraciones_)))
            cuenta = -1;
            time.sleep(2)
            
            
            for declara in declaraciones_:
                if(cuenta!=-1):
                    nombre_archivo=""
                    xpatho = ""
                    xpatht = ""
                    xpathp = ""


                              
                    xpatho = "/html/body/form/div[3]/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[10]/div/div/table/tbody/tr["+str(cuenta+2)+"]/td[1]"
                    operacion = WebDriverWait(driver,5)\
                        .until(EC.element_to_be_clickable((By.XPATH,xpatho)))\
                                                    .text
                        
                    xpatht = "/html/body/form/div[3]/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[10]/div/div/table/tbody/tr["+str(cuenta+2)+"]/td[2]"
                    tipo = WebDriverWait(driver,5)\
                        .until(EC.element_to_be_clickable((By.XPATH,xpatht)))\
                                                    .text
                
                    xpathp = "/html/body/form/div[3]/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[10]/div/div/table/tbody/tr["+str(cuenta+2)+"]/td[6]"
                    periodo = WebDriverWait(driver,5)\
                        .until(EC.element_to_be_clickable((By.XPATH,xpathp)))\
                                                    .text 
                    #print("Tipo: "+tipo_declaracion[tipo]+" Periodo:"+meses[periodo])
                    nombre_archivo = tipo_declaracion[tipo] + "_" +meses[periodo]+"_"+operacion+"_"+str(i)
                    #print(nombre_archivo)
                     


                    WebDriverWait(driver,5)\
                    .until(EC.element_to_be_clickable((By.ID,"MainContent_wucConsultasDeclaracion_gvDeclaraciones_lbtnNumOp_"+str(cuenta))))\
                                                .click()
                
                    time.sleep(2)   

                

                    element = WebDriverWait(driver,10)\
                    .until(EC.element_to_be_clickable((By.ID,"btnDescargaPdf")))                                          

                    #driver.execute_script("arguments[0].scrollIntoView();", element)
                    driver.execute_script("window.scrollTo(0, 0);")
                    
                    element.click()
                    
                    time.sleep(5)                       

                    renombra_ultima_descarga(init.path_descarga,nombre_archivo)

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
            for pdf_file in pathlib.Path(init.path_descarga).glob(f'*{str(i)}*.pdf'):    
                archivos = archivos + str(pdf_file) + "|"                      
            resultados[str(i)] = archivos
        except TimeoutException:
            #Si no existe la tabla de declaraciones entonces clic en el boton cancelar
            WebDriverWait(driver,10)\
                        .until(EC.element_to_be_clickable((By.XPATH,
                                                    'MainContent_btnCacelar')))\
                                                    .click()                                                              
            print(f"No Existen Declaraciones que Descargar para: {i}")        

print(resultados)                                  
time.sleep(2); 


