import logging

from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


import logging

NAV_ELEMENT="nav"
MODULE_MENU="SelectModul"
PENDAPATAN_MENU="Pendapatan"
PERUBAHAN_LINK="objTreeMenu_1_node_1_2"
PERUBAHAN_LAT_LINK="objTreeMenu_1_node_1_2"

def modul_pendapatan(driver):
    try:
        logging.info("Navigasi ke modul perubahan")
        driver.implicitly_wait(2)
        driver.switch_to.frame(driver.find_element_by_name(NAV_ELEMENT))
        moduleMenu=driver.find_element_by_id(MODULE_MENU)
        Select(moduleMenu).select_by_visible_text(PENDAPATAN_MENU)
        driver.execute_script("""
        document.getElementById('objTreeMenu_1_node_1_2').style.display = "inline"
        """)
        driver.find_element_by_xpath("//div[@id='objTreeMenu_1_node_1_2']//nobr//a").click()
        driver.switch_to.default_content()
        
    except  Exception as err:
        logging.error(err)

def choose_skpd(driver,periode=2021, bulan='September', tanggal="", skpd="[5.02.0.00.0.00.01.0000] BADAN PENGELOLAAN KEUANGAN DAN ASET DAERAH"):
    driver.switch_to.frame(driver.find_element_by_name("content"))
        
    driver.execute_script("""
        document.getElementById('apbd_apbd_id').style.display = "inline";

        """)
    Select(driver.find_element_by_id("apbd_apbd_id")).select_by_visible_text(str(periode))

    driver.execute_script("""
        document.getElementById('bulan').style.display = "inline";

        """)
    Select(driver.find_element_by_id("bulan")).select_by_visible_text(bulan)

    driver.execute_script("""
        document.getElementById('sikd_satker_id').style.display = "inline";

        """)
    Select(driver.find_element_by_id("sikd_satker_id")).select_by_visible_text(skpd)
    driver.find_element_by_id("tb-input").click()
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element_by_name("content"))
    driver.find_element_by_id("btn_input").click()
    driver.switch_to.default_content()

def input_bku_pendapatan(driver, data):
    driver.switch_to.frame(driver.find_element_by_name("content"))

    driver.find_element_by_id("tgl_trx").send_keys(data['tgl_transaksi'])

    driver.find_element_by_id("uraian_trx").send_keys(data['uraian'].strip())

    driver.execute_script("""
        document.getElementById('cara_pembayaran').style.display = "inline";

        """)
    Select(driver.find_element_by_id("cara_pembayaran")).select_by_visible_text(data['cara_pembayaran'].strip())

    driver.find_element_by_id("uraian_trx").send_keys(str(data['no_bukti']))

    driver.execute_script("""
        document.getElementById('pendapatan_thn_lalu').style.display = "inline";

        """)
    Select(driver.find_element_by_id("pendapatan_thn_lalu")).select_by_visible_text(data['status_pendapatan'].strip())

    driver.execute_script("""
        document.getElementById('sikd_skpkd_bank_account_id').style.display = "inline";

        """)
    Select(driver.find_element_by_id("sikd_skpkd_bank_account_id")).select_by_visible_text(data['rekening_setoran'])

    driver.execute_script("""
        document.getElementById('sikd_rek_jenis_id').style.display = "inline";

        """)
    Select(driver.find_element_by_id("sikd_rek_jenis_id")).select_by_visible_text(f'[{data["rekening_jenis"]}] {data["nama_jenis"]}')
  
    rek_obj=driver.find_element_by_id('sikd_rek_obj_id')
    WebDriverWait(driver, 5).until(expected_conditions.staleness_of(rek_obj))
    rek_obj=WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located((By.ID,'sikd_rek_obj_id')))
    Select(rek_obj).select_by_visible_text(f'[{data["rekening_objek"]}] {data["nama_objek"]}')

    rek_rinc_obj=driver.find_element_by_id('sikd_rek_rincian_obj_id')
    WebDriverWait(driver, 5).until(expected_conditions.staleness_of(rek_rinc_obj))
    rek_rinc_obj=WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located((By.ID,'sikd_rek_rincian_obj_id')))
    Select(rek_rinc_obj).select_by_visible_text(f'[{data["rekening_rincian"]}] {data["nama_rincian"]}')

    jumlah=driver.find_element_by_id('jumlah_0')
    WebDriverWait(driver, 5).until(expected_conditions.staleness_of(jumlah))
    jumlah=WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located((By.ID,'jumlah_0')))
    
    jumlah.clear()

    jumlah.send_keys(str(data["jumlah"]))
    driver.implicitly_wait(1)

    driver.find_element_by_id('tb-simpan').click()
    driver.switch_to.default_content()