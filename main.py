# From system
import os
import time
import random
import pyautogui
# From selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
# For solving recaptcha
import speech_recognition as sr
import urllib
import pydub

# Define download path
path_to_download = os.getcwd() + '/outputs'

# Define a new instance of firefox with specific options
options = Options()
# options.headless = True # Hide firefox window
options.set_preference('browser.download.folderList', 2) # use specific folder
options.set_preference('browser.download.dir', path_to_download) # Se path to download
options.set_preference('browser.helperApps.alwaysAsk.force', False) # Do not ask anything (no pop up)
options.set_preference('browser.download.manager.showWhenStarting', False) # Do not show anything (no pop up)
options.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/zip') # MIME type for zip
print('[INFO] Preferences: OK')

# Define a new firefox instance
driver = webdriver.Firefox(options = options)
width = height = 800
ss_w, ss_h= pyautogui.size() # Cross-platform to get screen resolution
driver.set_window_size(width, height)
driver.set_window_position(ss_w / 2 - width / 2, ss_h / 2 - height / 2) # Center the window
print('[INFO] Firefox: opened OK')

ppgcc_2020 = [
    '5376253015721742' , #1 Antonio Jorge Gomes Abelém
    '3032638002357978' , #2 Bianchi Serique Meiguins
    '2948406243474342' , #3 Carlos Gustavo Resque dos Santos
    '4742268936279649' , #4 Claudomiro de Souza de Sales Junior
    '6490014244112888' , #5 Cleidson Ronald Botelho de Souza
    '8273198217435163' , #6 Denis Lima do Rosário
    '1497269209026542' , #7 Eloi Luiz Favero
    '5883877669437870' , #8 Filipe de Oliveira Saraiva
    '1631238943341152' , #9 Gustavo Henrique Lima Pinto
    '5219735119295290' , #10 Jefferson Magalhães de Morais
    '8158963767870649' , #11 Josivaldo de Souza Araújo
    '2130563131041136' , #12 Marcelle Pereira Mota
    '9756167788721062' , #13 Nelson Cruz Sampaio Neto
    '6894507054383644' , #14 Roberto Samarone dos Santos Araújo
    '2080791630485427' , #15 Sandro Ronaldo Bezerra Oliveira
    '1596629769697284' , #16 ALDEBARO BARRETO DA ROCHA KLAUTAU JUNIOR
    '7458287841862567' , #17 CARLOS RENATO LISBOA FRANCES
    '1028151705135221' , #18 EDUARDO COELHO CERQUEIRA
    '0232988306987805' , #19 GUSTAVO PESSIN
    '9622051867672434' , #20 JOAO CRISOSTOMO WEYL ALBUQUERQUE COSTA
    '1274395392752454' , #21 ROMMEL THIAGO JUCA RAMOS
    '9014616733186520' , #22 Ronnie Cley de Oliveira Alves
    '7676631005873564',  #23 Fabiola Pantoja Oliveira Araújo
    '9157422386900321',  #24 Reginaldo Cordeiro dos Santos Filho
    '1468872219964148',  #25 Helder May Nunes da Silva Oliveira
    '0970111009687779',  #26 Lídio Mauro Lima de Campos
    '2949449810540513',  #27 André Figueira Riker
    '2484200467965399',  #28 Vinicius Augusto Carvalho de Abreu
]

# Define default URL
# # Note that the last option (idcnpq) is the professor lattes ID
lattes_url = 'http://buscatextual.cnpq.br/buscatextual/download.do?metodo=apresentar&idcnpq='

# Iterate through all professor's id
for idcnpq in ppgcc_2020:
    location = lattes_url + idcnpq
    driver.get(location)
    print('[INFO] Firefox: page loaded OK')

    # Find iframe tag and switch to that iframe context
    frames = driver.find_elements(By.TAG_NAME, 'iframe')
    driver.switch_to.frame(frames[0])

    # Click on recaptcha checkbox and switch to default context
    driver.find_element(By.CLASS_NAME, 'recaptcha-checkbox-border').click()
    driver.switch_to.default_content()

    # Investigate submit button
    button = driver.find_element(By.ID, 'submitBtn')
    time.sleep(random.randint(1, 2))

    # If true, do recaptcha
    # if button.get_attribute('disabled'):
    if not button.is_enabled():
        print('[INFO] Firefox: solve recaptcha for idcnpq {}'.format(idcnpq))
        # Find iframe tag and switch to that iframe context
        frames = driver.find_element(By.XPATH, '/html/body/div[2]/div[4]').find_elements(By.TAG_NAME, 'iframe')
        driver.switch_to.frame(frames[0])

        # Click on recaptcha audio button (alternative way to solve recaptcha)
        time.sleep(random.randint(1, 2))
        driver.find_element(By.ID, 'recaptcha-audio-button').click()

        # Switch to default context again
        driver.switch_to.default_content()

        # Find iframe tag and switch to the last context
        frames = driver.find_elements(By.TAG_NAME, 'iframe')
        driver.switch_to.frame(frames[-1])

        # [Optional] Wait 1 second and play audio
        time.sleep(1)
        driver.find_element(By.XPATH, '/html/body/div/div/div[3]/div/button').click()

        #================================================#
        # From now on: download the mp3 audio source,
        # convert to wav format,
        # feed speech recognition algorithm,
        # translate to string,
        # and send string back to recaptcha frame
        #================================================#

        # Download mp3 file
        src = driver.find_element(By.ID, 'audio-source').get_attribute('src')
        file_name = path_to_download + '/sample.mp3'
        urllib.request.urlretrieve(src, file_name)
        print('[INFO] Firefox: download audio OK')

        # Get file and convert to wav extension
        sound = pydub.AudioSegment.from_mp3(file_name)
        file_name = file_name.replace('.mp3', '.wav')
        sound.export(file_name, format = 'wav')
        print('[INFO] Firefox: converted audio OK')

        # Submit audio to a speechrecognition algorithm from Google
        sample_audio = sr.AudioFile(file_name)
        r = sr.Recognizer()
        with sample_audio as source:
            audio = r.record(source)

        key = r.recognize_google(audio)
        print('[INFO] Recaptcha code: {}'.format(key))

        # Send string (key) back to recaptcha page and switch to default context again
        driver.find_element(By.ID, 'audio-response').send_keys(key.lower())
        driver.find_element(By.ID, 'audio-response').send_keys(Keys.ENTER)
        driver.switch_to.default_content()

        # Submit solution by clicking the button
        time.sleep(1)
        driver.find_element(By.ID, 'submitBtn').click()
        print('[INFO] Firefox: download zip file OK\n')

    else: # If false, just click and download zip file
        print('[INFO] Firefox: no recaptcha to solve for {}'.format(idcnpq))
        time.sleep(1)
        button.click()
        print('[INFO] Firefox: download zip file OK\n')

driver.quit()
