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

archivos = []
persona = "moral" if len(init.rfc)==12 else "fisica"
#Opciones de navegacion
for file in pathlib.Path(init.path_descarga).glob('*.*'):
        try:
            file.unlink()
        except:
            pass

options = webdriver.ChromeOptions() #Options()
prefs = {'download.default_directory' : init.path_descarga}
options.add_experimental_option('prefs', prefs)
options.add_argument('headless')
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


#WebDriverWait(driver,10)\
#.until(EC.element_to_be_clickable((By.XPATH,
#                                '/html/body/form/div[3]/div/div[1]/nav/div/div[3]/div/div/ul/li[3]/ul/li[1]/a/span')))\
#                                .click()


driver.get('https://ptscdecprov.clouda.sat.gob.mx/Paginas/ConsultaDeclaracion.aspx')

time.sleep(3);


anios = []
for x in range(2018,2024+1):
    anios.append(x)
print(anios)
moral2019 = 0;

for i in anios:

    if i > 2021: #and persona=="moral":
        if moral2019==0:           
           #accedemos al nuevo sitio de declaraciones que tiene la repo de los anios 2019 en adelante
           driver.get('https://pstcdypisr.clouda.sat.gob.mx/')
           #WebDriverWait(driver, 10).until(EC.url_to_be("https://anualpm.clouda.sat.gob.mx/MoralesV2"))
           #Accedemos al apartado de las declaraciones
           #WebDriverWait(driver,10)\
           #     .until(EC.element_to_be_clickable((By.ID,
           #                                 'navbarDropdownMenuLink')))\
           #                                 .click()                                                    
           #WebDriverWait(driver,10)\
           #     .until(EC.element_to_be_clickable((By.XPATH,
           #                                 '/html/body/nav/div/div/ul[1]/li[2]/div/a[1]')))\
           #                                 .click()
           time.sleep(3)
           driver.get('https://pstcdypisr.clouda.sat.gob.mx/Consulta/Consulta?tipoDocumento=1')
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
        declaraciones_news = driver.find_elements(By.XPATH,"//*[@id='accordionResult']/div")
        
        print(f"Para {i}:existen {len(declaraciones_news)} para descargar")
        #sino existen declaraciones clickeamos el boton de cerrar en la ventana de resultado que informa que no existen declaraciones
        if len(declaraciones_news)==0:
            WebDriverWait(driver,5)\
                .until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[12]/div/div/div[3]/button")))\
                                            .click()
        else:
            #si existen declaraciones que descargar entonces comenzamos a iterar en la tabla correspodiente para la descarga de todas las declaraciones 
            for declara in declaraciones_news:
                WebDriverWait(declara,5)\
                    .until(EC.element_to_be_clickable((By.ID,"linkDescargaPDF")))\
                                                .click()
                time.sleep(3)
               
        time.sleep(2)
        for pdf_file in pathlib.Path(init.path_descarga).glob(f'*{str(i)}*.pdf'):    
                archivos.append(parsepdf.pdf_to_base64(pdf_file))
        #driver.close()
        #exit()
    else:    
        select_ = Select(WebDriverWait(driver,10)\
        .until(EC.element_to_be_clickable((By.ID,'MainContent_wucConsultasDeclaracion_wucDdlEjercicioFiscal_ddlCatalogo'))))

        select_.select_by_value(str(i))
        time.sleep(1)

        if persona == "fisica":
            WebDriverWait(driver,10)\
            .until(EC.element_to_be_clickable((By.XPATH,
                                            '/html/body/div[1]/div/form/div/div[2]/div/div[6]/div[2]/button[1]')))\
                                            .click()
           
        else:
            WebDriverWait(driver,10)\
            .until(EC.element_to_be_clickable((By.XPATH,
                                            '/html/body/form/div[3]/div/div[3]/div/div/div/div[2]/div/div/div/div[3]/div/input[1]')))\
                                            .click()

        
        time.sleep(10)
        

        try:
            if persona=="fisica":
                tabla = WebDriverWait(driver,1).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div/form/div/div[3]/div[2]')))
            else:
                tabla = WebDriverWait(driver,1).until(EC.element_to_be_clickable((By.ID,'MainContent_wucConsultasDeclaracion_gvDeclaraciones')))
            
            declaraciones_ = tabla.find_elements(By.TAG_NAME,"tr")
            print("declaraciones provisionales: "+ str(len(declaraciones_)))
            cuenta = -1;
            time.sleep(2)
            

            for declara in declaraciones_:

                if(cuenta!=-1):
                    WebDriverWait(driver,5)\
                    .until(EC.element_to_be_clickable((By.ID,"MainContent_wucConsultasDeclaracion_gvDeclaraciones_lbtnNumOp_"+str(cuenta))))\
                                                .click()
                
                    time.sleep(2)   

                

                    element = WebDriverWait(driver,10)\
                    .until(EC.element_to_be_clickable((By.ID,"btnDescargaPdf")))                                          

                    #driver.execute_script("arguments[0].scrollIntoView();", element)
                    driver.execute_script("window.scrollTo(0, 0);")
                    
                    element.click()
                    
                    time.sleep(2)                       
        
                    WebDriverWait(driver,10)\
                    .until(EC.element_to_be_clickable((By.XPATH,"/html/body/form/div[3]/div/div[3]/div/div/div/div[3]/div/div[2]/div/input[2]")))\
                                                .click()                 
                                                
                    time.sleep(3)

                    

                    #if(persona=="fisica"):
                    #    WebDriverWait(driver,10)\
                    #    .until(EC.element_to_be_clickable((By.XPATH,
                    #                                '/html/body/div[6]/div/div/div[2]/button[1]')))\
                    #                                .click()
                    #else:
                    #    WebDriverWait(driver,10)\
                    #    .until(EC.element_to_be_clickable((By.XPATH,
                    #                                '/html/body/div[7]/div/div/div[2]/button[1]')))\
                    #                                .click()  
                cuenta = cuenta+1
                      
            print(f"Existen Declaraciones que descargar para: {i}")        
            for pdf_file in pathlib.Path(init.path_descarga).glob(f'*{str(i)}*.pdf'):    
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

#print(archivos)                                  
time.sleep(2); 