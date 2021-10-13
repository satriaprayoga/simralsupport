import logging
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
from simral.driver.SimralDriver import SimralDriver

class NeracaAwalDriver(SimralDriver):

    def __init__(self):
        super().__init__()

    def load_neraca_awal(self,file_name):
        self.data_neraca=pd.read_excel(file_name)
        return self.data_neraca

    def pilih_skpd(self,kode_skpd,nama_skpd,sub_unit='UNIT INDUK',periode='2021'):
        try:
            self.switchFrame('content')
            self.__display_all_selects__()
            apbd_apbd_id=WebDriverWait(self._driver,1).until(expected_conditions.presence_of_element_located((By.ID,"apbd_apbd_id")))
            Select(apbd_apbd_id).select_by_visible_text(periode)
            self._driver.implicitly_wait(1)
            self.__display_all_selects__()
            sikd_satker_id=WebDriverWait(self._driver,1).until(expected_conditions.presence_of_element_located((By.ID,"sikd_satker_id")))
            #Select(sikd_satker_id).select_by_visible_text(f'[{kode_skpd}] {nama_skpd}')
            Select(sikd_satker_id).select_by_value(kode_skpd)
            self._driver.implicitly_wait(1)
            self.__display_all_selects__()
            sikd_sub_skpd_id=WebDriverWait(self._driver,1).until(expected_conditions.presence_of_element_located((By.ID,"sikd_sub_skpd_id")))
            Select(sikd_sub_skpd_id).select_by_visible_text(sub_unit)
            self._driver.implicitly_wait(1)
            self._driver.find_element_by_id('tb-input').click()
            self.switchToDefault()
        except Exception as err:
            logging.error(err)

    def input_neraca_awal(self,rek_kelompok,nama_kelompok,rek_jenis,nama_rek_jenis,rek_objek,nama_objek,rek_rincobjek,nama_rincobjek,rekening,uraian,debet,kredit):
        try:
            self.switchFrame('content')
            self.__display_all_selects__()
            sikd_rek_kelompok_id=WebDriverWait(self._driver,1).until(expected_conditions.presence_of_element_located((By.ID,"sikd_rek_kelompok_id")))
            Select(sikd_rek_kelompok_id).select_by_visible_text(f'[{rek_kelompok}] {nama_kelompok}')
            self._driver.implicitly_wait(0.5)
            self.__display_all_selects__()
            sikd_rek_jenis_id=WebDriverWait(self._driver,1).until(expected_conditions.presence_of_element_located((By.ID,"sikd_rek_jenis_id")))
            Select(sikd_rek_jenis_id).select_by_visible_text(f'[{rek_jenis}] {nama_rek_jenis}')
            self._driver.implicitly_wait(0.5)
            self.__display_all_selects__()
            sikd_rek_obj_id=WebDriverWait(self._driver,1).until(expected_conditions.presence_of_element_located((By.ID,"sikd_rek_obj_id")))
            Select(sikd_rek_obj_id).select_by_visible_text(f'[{rek_objek}] {nama_objek}')
            self._driver.implicitly_wait(1)

            self.__display_all_selects__()
            sikd_rek_rincian_obj_id=WebDriverWait(self._driver,1).until(expected_conditions.presence_of_element_located((By.ID,"sikd_rek_rincian_obj_id")))
            Select(sikd_rek_rincian_obj_id).select_by_visible_text(f'[{rek_rincobjek}] {nama_rincobjek}')
            self._driver.implicitly_wait(1)
            
            #self._driver.find_element_by_id('tb-input').click()
            search_field=WebDriverWait(self._driver,1).until(expected_conditions.presence_of_element_located((By.ID,"kt_kunci")))
            search_field.clear()
            search_field.send_keys(rekening)
            search_btn=self._driver.find_element_by_name("submitSearch")
            search_btn.click()
            self._driver.implicitly_wait(1)
            jml_debet_0=self._driver.find_element_by_id('jml_debet_0')
            #WebDriverWait(self._driver, 5).until(expected_conditions.staleness_of(jumlah))
            jml_debet_0=WebDriverWait(self._driver, 5).until(expected_conditions.presence_of_element_located((By.ID,'jml_debet_0')))
            
            jml_debet_0.clear()

            jml_debet_0.send_keys(str(debet))

            jml_kredit_0=self._driver.find_element_by_id('jml_kredit_0')
            #WebDriverWait(self._driver, 5).until(expected_conditions.staleness_of(jumlah))
            jml_kredit_0=WebDriverWait(self._driver, 5).until(expected_conditions.presence_of_element_located((By.ID,'jml_kredit_0')))
            
            jml_kredit_0.clear()

            jml_kredit_0.send_keys(str(kredit))
            self._driver.implicitly_wait(3)
            self._driver.find_element_by_id('tb-simpan').click()
            self.switchToDefault()
            self.switchToDefault()
        except Exception as err:
            logging.error(err)

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