# wahsapp selenium
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import pyperclip
chromedriver_autoinstaller.install()

options = webdriver.ChromeOptions()
options.add_argument("--disable-extensions")
options.add_argument("--disable-popup-blocking")
options.add_argument("--user-data-dir=/yuser")
options.add_experimental_option('excludeSwitches',['--enable-automation'])
driver = webdriver.Chrome(chrome_options=options)
driver.get("https://web.whatsapp.com")
time.sleep(1000)
ranges = 5
counter = 1
dataz = '/datas.csv'
df = pd.read_csv(dataz)
# START LOOPING HERE >>>>>
for index, row in df.iterrows():
    number = row['Number']
    id_pel = row['ID Pelanggan']
    nama = row['Nama']
    alamat = row['Alamat']
    tarif = row['Tarif/Daya']
    rekening = row['Rekening']
    tagihan = row['Tagihan']
    message = f'''*PT PLN (Persero) ULP KROYA*

    Yth. Bapak/Ibu Pelanggan PLN

    Dengan ini kami informasikan,
    IDPEL  : {str(id_pel)}
    Nama  : {str(nama)}
    Alamat  : {str(alamat)}
    Tarif/Daya : {str(tarif)}
    Rekening : {str(rekening)}
    Tagihan : Rp. {tagihan}
    (Belum termasuk Admin Bank & Meterai)

    Berdasarkan data kami, Tagihan Listrik anda *BELUM LUNAS & sudah melewati jatuh tempo* pembayaran, tanggal 20 setiap bulannya.
    Untuk menghindari *pemutusan.* listrik di tempat anda, mohon segera melakukan pembayaran.

    Demikian disampaikan
    Hormat kami
    PLN ULP KROYA

    - _Contact Center PLN : 123_
    - _Pembayaran dapat di lakukan di PPOB terdekat_
    - _Instal apk PLN Mobile untuk semua layanan PLN_
    - *_Mohon abaikan jika sudah LUNAS_*'''  # Replace with your message

    message = message.replace('\n', '\u000A')
    print(message)
    time.sleep(1)
    try:
        driver.get(f'https://api.whatsapp.com/send/?phone={number:.0f}')
        # skipping
        driver.implicitly_wait(10)
        driver.find_element(By.ID,'action-button').click()
        driver.implicitly_wait(10)
        driver.find_element(By.XPATH,'//*[@id="fallback_block"]/div/div/h4[2]/a').click()
        driver.implicitly_wait(10)
        msgs = driver.find_element(By.CSS_SELECTOR,'[data-testid="conversation-compose-box-input"]')
        msgs.click()
        pyperclip.copy(message)
        msgs.send_keys(Keys.CONTROL,'v')
        driver.implicitly_wait(10)
        driver.find_element(By.CSS_SELECTOR,'[data-testid="compose-btn-send"]').click()
        time.sleep(2)
        print('\n-- sended\n')
        counter += 1
    except NoSuchElementException():
        time.sleep(5)
        pass
