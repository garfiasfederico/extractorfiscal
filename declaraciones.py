from selenium import webdriver;
from selenium.webdriver.support.ui import WebDriverWait;
from selenium.webdriver.support import expected_conditions as EC;
from selenium.webdriver.common.by import By;
import time;
import pandas as pd;
from selenium.webdriver.chrome.options import Options
import pyautogui
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
import init


persona = "moral" if len(init.rfc)==12 else "fisica"
#Opciones de navegacion

options = webdriver.ChromeOptions() #Options()
prefs = {'download.default_directory' : init.path_descarga}
options.add_experimental_option('prefs', prefs)
#options.add_argument('headless')
driver = webdriver.Chrome(options=options);


#Inicializar en la pantalla 2 

#driver.set_window_position(2000,0)
#driver.maximize_window();
#driver.minimize_window()
time.sleep(1);


#inicializamos el navegador

#driver.get('https://www.sat.gob.mx/personas/declaraciones')
driver.get('https://anualpf.clouda.sat.gob.mx/')

time.sleep(1);

WebDriverWait(driver, 10)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                      'button#buttonFiel')))\
    .click()

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

time.sleep(1);

WebDriverWait(driver,10)\
.until(EC.element_to_be_clickable((By.XPATH,
                                  '/html/body/div[1]/div/ul/li[2]/a/span')))\
                                  .click()

time.sleep(1);

anios = []
for x in range(2015,2025):
    anios.append(x)


for i in anios:
    select_ = Select(WebDriverWait(driver,10)\
    .until(EC.element_to_be_clickable((By.ID,'IdEjercicio'))))

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
                                        '/html/body/div[2]/div/form/div/div[2]/div/div[6]/div[2]/button[1]')))\
                                        .click()

    
    time.sleep(3)

    try:
        if persona=="fisica":
            tabla = WebDriverWait(driver,1).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div/form/div/div[3]/div[2]')))
        else:
            tabla = WebDriverWait(driver,1).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/div/form/div/div[3]/div[2]')))
        
        declaraciones_ = driver.find_elements(By.XPATH,"//*[@id='accordion']/div")
        print("declaraciones: "+ str(len(declaraciones_)))
        time.sleep(2)

        for declara in declaraciones_:

            WebDriverWait(declara,5)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,"img[alt='Generar pdf']")))\
                                        .click()

            time.sleep(2)
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
                                  
time.sleep(2);                                  

