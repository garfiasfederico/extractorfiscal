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
driver.get('http://127.0.0.1:8000/login')

time.sleep(2);
WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.XPATH,
                                      '/html/body/div[1]/div/div/div/div/form/div[2]/input')))\
    .send_keys("SIIBIEN.APE")

time.sleep(2);
WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.XPATH,
                                      '/html/body/div[1]/div/div/div/div/form/div[3]/input[1]')))\
    .send_keys("g4b1n3t3")

time.sleep(2);
WebDriverWait(driver,10)\
.until(EC.element_to_be_clickable((By.XPATH,
                                  '/html/body/div[1]/div/div/div/div/form/div[4]/button')))\
                                    .click()

time.sleep(5);
WebDriverWait(driver,10)\
.until(EC.element_to_be_clickable((By.XPATH,
                                  '/html/body/div[1]/ul/li[5]/a')))\
                                  .click()


time.sleep(1);
WebDriverWait(driver,10)\
.until(EC.element_to_be_clickable((By.XPATH,
                                  '/html/body/div[1]/div/div/div/main/div/div/div[2]/center/div/table/tbody/tr[1]/td[3]/a/button')))\
                                  .click()

time.sleep(3);



