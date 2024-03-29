import datetime
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert

def esta_na_hora(hora, minuto, segundos, data_atual):
    if data_atual.hour == hora and data_atual.minute == minuto and data_atual.second == segundos:
        return True
    return False


def processa_dias_da_semana(dias_da_semana):
    dias_da_semana_int = []
    for dia in dias_da_semana:
        if dia == "seg":
            dias_da_semana_int.append(0)
        if dia == "ter":
            dias_da_semana_int.append(1)
        if dia == "qua":
            dias_da_semana_int.append(2)
        if dia == "qui":
            dias_da_semana_int.append(3)
        if dia == "sex":
            dias_da_semana_int.append(4)
        if dia == "sab":
            dias_da_semana_int.append(5)
        if dia == "dom":
            dias_da_semana_int.append(6)
    return dias_da_semana_int


def esta_no_dia_da_semana(dias_da_semana, data_atual):
    if data_atual.weekday() in dias_da_semana:
        return True

    return False


print("+++++++++++++++++++++++++++++++")
print("+++++++Agenda Prenot@mi++++++++")
print("+++++++++++++++++++++++++++++++")

hora_string = input("Que horas quer agendar? (hh:mm:sg): ")

dia_da_semana_string = input(
    "Quais dias da semana? (seg ter qua qui sex sab dom): ")
email = input("Digite seu email cadastrado: ")
senha = input("Digite sua senha: ")
path = input("Digite o caminho do arquivo completo com barras invertidas /: ")

hora = int(hora_string.split(':')[0])
minuto = int(hora_string.split(':')[1])
segundos = int(hora_string.split(':')[2])

dias_da_semana = dia_da_semana_string.split(' ')
dias_da_semana_int = processa_dias_da_semana(dias_da_semana)

ativo = True
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
while ativo:
    agora = datetime.datetime.now()
    print(agora)
    if esta_na_hora(hora, minuto, segundos, agora) and esta_no_dia_da_semana(dias_da_semana_int, agora):
        ativo = False
        navegador = webdriver.Chrome(chrome_options=chrome_options)
        navegador.get("https://prenotami.esteri.it")
        time.sleep(3)
        navegador.find_element(
            By.ID, "login-email").send_keys(email)
        navegador.find_element(
            By.ID, "login-password").send_keys(senha)
        navegador.find_element(
            By.XPATH, '//*[@id="login-form"]/button').click()
        time.sleep(3)
        navegador.find_element(By.ID, "advanced").click()
        time.sleep(2)
        navegador.find_element(
            By.XPATH, '//*[@id="dataTableServices"]/tbody/tr[2]/td[4]/a/button').click()
        time.sleep(2)
        i = 1
        while navegador.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div/div/div/div/div/div/div[4]/button') == navegador.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div/div/div/div/div/div/div[4]/button'):
            print("Tentativa Nº - " + str(i))
            navegador.find_element(
                By.XPATH, '/html/body/div[2]/div[2]/div/div/div/div/div/div/div/div[4]/button').click()
            delay = 10  # segundos
            try:
                elemento = WebDriverWait(navegador, delay).until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="dataTableServices"]/tbody/tr[2]/td[4]/a/button')))
                elemento.click()
            except TimeoutException:
                print("elemento nao encontrado")
            i = i + 1
    time.sleep(1)
navegador.find_element(By.ID, 'File_0').send_keys(path)
navegador.find_element(By.ID, 'PrivacyCheck').click()
navegador.find_element(By.ID, 'btnAvanti').click()
alert = Alert(navegador)
alert.accept()
ativo = True
while ativo:
    if navegador.find_element(By.CLASS_NAME, 'day availableDay').is_enabled:
        navegador.find_element(By.CLASS_NAME, 'day availableDay').click()
        ativo = False
navegador.find_element(
    By.CLASS_NAME, 'table-condensed > dtpicker-next').click()
navegador.find_element(By.ID, 'btnPrenota').click()


#Melhoria para o futuro.
'''
# Locate the calendar buttons: backwards, month and forward
loc = navegador.find_element(By.CLASS_NAME, 'calendar')

# Flag to indicate whether is any day available in the month or no
no_available_days = True

# Initialize assuming no green days available
green_days = []

# Try for max 18 months
max_tries = 18

# Count each iteration
iter_count = 0

# Iterate the calendar until find and available day
while no_available_days:
    try:
        # Find all the available days in a month
        green_days = navegador.find_elements(
            by='class_name', value=loc['GREEN_DAYS'])
        if green_days == None:
            green_days = []
    except:
        pass

        # Logic to walk around the months
    if len(green_days) == 0:
        # Compare iteration number with stop limit
        if iter_count > max_tries:
            # No available days within 18 months
            no_available_days = False
            # Print a message
            print('Sem dias disponíveis!')
        else:
            # Continue searching for available days in next month
            navegador.find_elements(
                by=loc['BY'], value=loc['FORWARD']).click()
            # Sum one iteration
            iter_count += 1
            # Print the count
            print(f'Remaining attempts: {max_tries-iter_count}')
            # Wait until everything is loaded
            time.sleep(2)
            # Continue the loop
            continue
    else:
        # Change the flag
        no_available_days = False

        # Click on the first available day
        green_days[0].click()

        # Find the first available hour
        hours = navegador.find_elements(
            by='class_name', value=loc['HOURS'])

        # Click on the first available hour
        hours[0].click()

        # Submit the form
        navegador.find_elements(by=loc['BY'], value=loc['SUBMIT']).click()

        # If there is an OTP code to insert, wait until the user writes it
        try:
            otp = navegador.find_elements(by=loc['BY'], value=loc['OTP'])
        except:
            pass
        else:
            # Click on the input of the OTP window
            otp[0].click()

            # Get the OTP ok button
            otp_ok = navegador.find_elements(by=loc['BY'],
                                             value=loc['OTP_OK'])

            # Wait until the user inserts the OTP code
            time.sleep(1)

            # Submit the OTP form
            otp_ok[0].click()

            # Print a message
            print('Process succeed!')
'''