import logging
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
from simral.driver.SimralDriver import SimralDriver

class JPDriver(SimralDriver):

    def __init__(self):
        super().__init__()

    def load_jurnal_penyesuaian(self,file_name):
        self.data_jurnal=pd.read_excel(file_name)
        return self.data_jurnal

    def pilih_skpd(self,kode_skpd,nama_skpd,sub_unit='UNIT INDUK',periode='2021'):
        try:
            self.switchFrame('content')
            self.__display_all_selects__()
            apbd_apbd_id=WebDriverWait(self._driver,1).until(EC.presence_of_element_located((By.ID,"apbd_apbd_id")))
            Select(apbd_apbd_id).select_by_visible_text(periode)
            self._driver.implicitly_wait(1)
            self.__display_all_selects__()
            sikd_satker_id=WebDriverWait(self._driver,1).until(EC.presence_of_element_located((By.ID,"sikd_satker_id")))
            Select(sikd_satker_id).select_by_visible_text(f'[{kode_skpd}] {nama_skpd}')
            self._driver.implicitly_wait(1)
            self.__display_all_selects__()
            sikd_sub_skpd_id=WebDriverWait(self._driver,1).until(EC.presence_of_element_located((By.ID,"sikd_sub_skpd_id")))
            Select(sikd_sub_skpd_id).select_by_visible_text(sub_unit)
            self._driver.implicitly_wait(1)
            logging.info("Memilih Jurnal Penyesuaian pada {},{}".format(nama_skpd,sub_unit))
            self._driver.find_element_by_id('tb-input').click()
            self.switchToDefault()
        except Exception as err:
            logging.error(err)

    def input_jurnal_penyesuaian(self,tgl_trx,uraian_trx,no_bukti,kode_rekening_utang,nama_rek_utang,jml_debet_utang,kode_rekening_beban,nama_rek_beban,jml_kredit_beban):
        try:
            self.switchFrame("content")
            self._driver.find_element_by_id("tgl_trx").clear()
            self._driver.find_element_by_id("tgl_trx").send_keys(tgl_trx)

            self._driver.find_element_by_id("uraian_trx").send_keys(uraian_trx)
            self._driver.find_element_by_id("no_bukti").send_keys(no_bukti)

            kd_rek_utang=self._driver.find_element_by_id("kd_rekening_0_0_0")
            kd_rek_utang.send_keys(kode_rekening_utang)
            kd_rek_utang.send_keys(Keys.ARROW_DOWN)
            
            utang_first_opt=WebDriverWait(self._driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//li[@class='ui-menu-item'][contains(@id, 'ui-id-')][text()='[{}] {}']".format(kode_rekening_utang,nama_rek_utang))))
            utang_first_opt.click()

            jumlah_debet_utang=self._driver.find_element_by_id('jml_debet_0_0_0')
            jumlah_debet_utang.send_keys(jml_debet_utang)

            kd_rek_beban=self._driver.find_element_by_id("kd_rekening_0_1_0")
            kd_rek_beban.send_keys(kode_rekening_beban)
            kd_rek_beban.send_keys(Keys.ARROW_DOWN)
            self._driver.implicitly_wait(2)
            beban_first_opt=WebDriverWait(self._driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//li[@class='ui-menu-item'][contains(@id, 'ui-id-')][text()='[{}] {}']".format(kode_rekening_beban,nama_rek_beban))))
            beban_first_opt.click()
            
            jumlah_kredit_beban=self._driver.find_element_by_id('jml_kredit_0_1_0')
            jumlah_kredit_beban.send_keys(jml_kredit_beban)

            self._driver.implicitly_wait(2)
            self._driver.find_element_by_id('tb-simpan').click()
            self.switchToDefault()
        except Exception as err:
            logging(err)

    def __display_all_selects__(self):
        try:
            self._driver.execute_script('''
                var selects=document.getElementsByTagName("select");
                for(var i=0;i<selects.length;i++){
                    selects[i].style.display="inline"
                }
            ''')
        except Exception as err:
            logging.error(err)