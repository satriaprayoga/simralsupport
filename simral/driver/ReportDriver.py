from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from simral.driver.SimralDriver import SimralDriver
from pathlib import Path

import logging
import time
import os

class ReportDriver(SimralDriver):

    def __init__(self):
        super().__init__()

    def download_report(self,skpd,subunit,jenisLaporan,tgl_mulai,bulan_mulai,tgl_selesai,bulan_selesai,format="Spreadsheet Stream"):
        try:
            self.switchFrame("content")
            logging.info("Pilih laporan: {} {} {}".format(skpd,subunit,jenisLaporan))
            self.__display_all_selects__()
            id_satker=WebDriverWait(self._driver,1).until(expected_conditions.presence_of_element_located((By.ID,"id_satker")))
            Select(id_satker).select_by_visible_text(f'[{skpd["kode_skpd"]}] {skpd["nama_skpd"]}')
            self._driver.implicitly_wait(3)
            self.__display_all_selects__()
            id_sub_unit=WebDriverWait(self._driver,1).until(expected_conditions.presence_of_element_located((By.ID,"id_sub_skpd")))
            Select(id_sub_unit).select_by_visible_text(subunit)
            self.__display_all_selects__()
            jns_lap=WebDriverWait(self._driver,0.5).until(expected_conditions.presence_of_element_located((By.ID,"jns_lap")))
            Select(jns_lap).select_by_visible_text(jenisLaporan)
            self.__display_all_selects__()
            bulan_s=WebDriverWait(self._driver,0.5).until(expected_conditions.presence_of_element_located((By.ID,"bulan_s")))
            Select(bulan_s).select_by_visible_text(bulan_mulai)
            self.__display_all_selects__()
            tgl_s=WebDriverWait(self._driver,0.5).until(expected_conditions.presence_of_element_located((By.ID,"tgl_s")))
            Select(tgl_s).select_by_visible_text(tgl_mulai)
            bulan_e=WebDriverWait(self._driver,0.5).until(expected_conditions.presence_of_element_located((By.ID,"bulan_e")))
            Select(bulan_e).select_by_visible_text(bulan_selesai)
            tgl_e=WebDriverWait(self._driver,0.5).until(expected_conditions.presence_of_element_located((By.ID,"tgl_e")))
            Select(tgl_e).select_by_visible_text(tgl_selesai)
            self.__display_all_selects__()
            frmt=WebDriverWait(self._driver,0.5).until(expected_conditions.presence_of_element_located((By.ID,"format")))
            Select(frmt).select_by_visible_text(format)

            button=WebDriverWait(self._driver,1).until(expected_conditions.element_to_be_clickable((By.PARTIAL_LINK_TEXT,'Tampilkan')))
            button.click()
            self.wait_for_downloads()
            
        except Exception as err:
            logging.error(err)
    
    def clean_report(self,dafaSource):
        pass

    def merge_data(self,dataSources=[]):
        pass

    def save_merged(self,filename,format='.xlsx'):
        pass

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

    def get_file_name(self,waitTime):
        self._driver.execute_script("window.open()")
        self._driver.switch_to.window(self._driver.window_handles[-1])
        self._driver.get('chrome://downloads')
        endTime=time.time()+waitTime
        while True:
                try:
                    # get downloaded percentage
                    downloadPercentage = self._driver.execute_script("return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('#progress').value")
                    # check if downloadPercentage is 100 (otherwise the script will keep waiting)
                    if downloadPercentage == 100:
                    # return the file name once the download is completed
                        return self._driver.execute_script("return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('div#content  #file-link').text")
                except Exception as err:
                    logging.error(err)
                    pass
                
                time.sleep(1)
                if time.time()>endTime:
                    break

    def wait_for_downloads(self):
        print("Waiting for downloads", end="")
        while any([filename.endswith(".crdownload") for filename in os.listdir(str(Path.home()/"Downloads"))]):
            time.sleep(2)
            print()
            print(".", end="")
        print("done!")
        
