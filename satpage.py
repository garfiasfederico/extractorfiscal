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

#Opciones de navegacion

#options = webdriver.ChromeOptions();
#options.add_argument('--start-maximized');
#options.add_argument('--disable-extensions');\
#import selenium;
#print(selenium.__version__);
options = webdriver.ChromeOptions() #Options()
#options.add_argument("--window-size=1920x1080")
#options.add_argument("--verbose")
#prefs = {'download.default_directory' : 'E:\\Dropbox\\PROYECTO BURO FISCAL\\extractor_fiscal\\declaraciones'}
prefs = {'download.default_directory' : init.path_descarga}
options.add_experimental_option('prefs', prefs)
#options.add_argument("download.default_directory=E:\Dropbox\PROYECTO BURO FISCAL\extractor_fiscal\declaraciones\\")

#chromedriver_path = '/Library/WebServer/Documents/declaraciones/chromedriver';
driver = webdriver.Chrome(options=options);


#Inicializar en la pantalla 2 

driver.set_window_position(2000,0);
driver.maximize_window();
time.sleep(1);


#inicializamos el navegador

#driver.get('https://www.sat.gob.mx/personas/declaraciones')
driver.get('https://anualpf.clouda.sat.gob.mx/')


#WebDriverWait(driver,10)\
#.until(EC.element_to_be_clickable((By.XPATH,
 #                                 '/html/body/div[4]/div[6]/div[1]/div[2]/div[1]/div[1]/div/span[1]/a')))\
  #                                .click()
time.sleep(1);

WebDriverWait(driver, 10)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                      'button#buttonFiel')))\
    .click()

time.sleep(2);
WebDriverWait(driver,10)\
.until(EC.element_to_be_clickable((By.XPATH,
                                  '/html/body/main/div/div/div[1]/form/div[1]/div/span/button')))\
.click()
time.sleep(1);
#pyautogui.write(u"E:\\Dropbox\\FIEL_SAGF8705279C8_20190131113307\\NUEVA_FIEL_SAGF870527\\C00001000000517898266.cer",interval=.08)
pyautogui.write(init.path_cert,interval=.08)
pyautogui.press('enter')
time.sleep(4);
#pyautogui.press('enter')

WebDriverWait(driver,10)\
.until(EC.element_to_be_clickable((By.XPATH,
                                  '/html/body/main/div/div/div[1]/form/div[2]/div/span/button')))\
                                  .click()


time.sleep(2);
#pyautogui.typewrite(u'E:\\Dropbox\\FIEL_SAGF8705279C8_20190131113307\\NUEVA_FIEL_SAGF870527\\Claveprivada_FIEL_SAGF8705279C8_20230215_204341.key',interval=.08)
pyautogui.typewrite(init.path_key,interval=.08)
pyautogui.press('enter')
time.sleep(1);
#pyautogui.press('enter')

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

anios = ['2020','2021','2022','2023','2024','2025']

for i in anios:
    select_ = Select(WebDriverWait(driver,10)\
    .until(EC.element_to_be_clickable((By.ID,'IdEjercicio'))))

    select_.select_by_value(i)
    time.sleep(1)

    WebDriverWait(driver,10)\
    .until(EC.element_to_be_clickable((By.XPATH,
                                    '/html/body/div[1]/div/form/div/div[2]/div/div[6]/div[2]/button[1]')))\
                                    .click()

    time.sleep(3);

    try:
        tabla = WebDriverWait(driver,1).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div/form/div/div[3]/div[2]')))
        time.sleep(2)
        WebDriverWait(driver,10)\
        .until(EC.element_to_be_clickable((By.XPATH,
                                    '/html/body/div[1]/div/form/div/div[3]/div[2]/div/div/div/div[2]/div/div[3]/div/div/img')))\
                                    .click()
        time.sleep(2)
        WebDriverWait(driver,10)\
        .until(EC.element_to_be_clickable((By.XPATH,
                                    '/html/body/div[6]/div/div/div[2]/button[2]')))\
                                    .click()
        
        time.sleep(2)
        WebDriverWait(driver,10)\
        .until(EC.element_to_be_clickable((By.XPATH,
                                    '/html/body/div[6]/div/div/div[2]/button[1]')))\
                                    .click()
        
        print("Existen Declaraciones que descargar")
    except TimeoutException:
        WebDriverWait(driver,10)\
        .until(EC.element_to_be_clickable((By.XPATH,
                                    '/html/body/div[3]/div/div/div[2]/button')))\
                                    .click()
        
        print("No Existen Declaraciones que Descargar")
                                  
time.sleep(2);                                  

