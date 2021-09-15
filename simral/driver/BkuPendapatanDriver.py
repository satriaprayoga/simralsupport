import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
from simral.driver.SimralDriver import SimralDriver

class BkuPendapatanDriver(SimralDriver):

    def __init__(self):
        super().__init__()

    def pilih_skpd(self,periode=2021, bulan='September', tanggal="", skpd="[5.02.0.00.0.00.01.0000] BADAN PENGELOLAAN KEUANGAN DAN ASET DAERAH"):
        try:
            logging.info("BKU Pendapatan {} {}".format(bulan,skpd))
            self.switchFrame("content")
            self._driver.execute_script("""
        document.getElementById('apbd_apbd_id').style.display = "inline";

        """)
            Select(self._driver.find_element_by_id("apbd_apbd_id")).select_by_visible_text(str(periode))

            self._driver.execute_script("""
                document.getElementById('bulan').style.display = "inline";

                """)
            Select(self._driver.find_element_by_id("bulan")).select_by_visible_text(bulan)

            self._driver.execute_script("""
                document.getElementById('sikd_satker_id').style.display = "inline";

                """)
            Select(self._driver.find_element_by_id("sikd_satker_id")).select_by_visible_text(skpd)
            self._driver.find_element_by_id("tb-input").click()
            self.switchToDefault()
            self.switchFrame("content")
            self._driver.find_element_by_id("btn_input").click()
            self.switchToDefault()
        except Exception as err:
            logging.error(err)

    def input_bku_pendatan(self,data):
        try:
            logging.info("Input bku pendapatan untuk nomor bukti: {}".format(data['no_bukti']))
            self.switchFrame("content")
            self._driver.find_element_by_id("tgl_trx").clear()

            self._driver.find_element_by_id("tgl_trx").send_keys(data['tgl_transaksi'])

            self._driver.find_element_by_id("uraian_trx").send_keys(data['uraian'].strip())

            self._driver.find_element_by_id("no_bukti").send_keys(data['no_bukti'].strip())

            self._driver.execute_script("""
                document.getElementById('cara_pembayaran').style.display = "inline";

                """)
            Select(self._driver.find_element_by_id("cara_pembayaran")).select_by_visible_text(data['cara_pembayaran'].strip())


            self._driver.execute_script("""
                document.getElementById('pendapatan_thn_lalu').style.display = "inline";

                """)
            Select(self._driver.find_element_by_id("pendapatan_thn_lalu")).select_by_visible_text(data['status_pendapatan'].strip())

            self._driver.execute_script("""
                document.getElementById('sikd_skpkd_bank_account_id').style.display = "inline";

                """)
            Select(self._driver.find_element_by_id("sikd_skpkd_bank_account_id")).select_by_visible_text(data['rekening_setoran'])

            self._driver.execute_script("""
                document.getElementById('dpa_dpa_id').style.display = "inline";

                """)
            noDpa=""
            if data["nama_dpa"]=="Belum Tercatat di APBD":
                noDpa=data["nama_dpa"]
            else:
                noDpa=f'[{data["no_dpa"]}] {data["nama_dpa"]}'

            Select(self._driver.find_element_by_id("dpa_dpa_id")).select_by_visible_text(noDpa)

            self._driver.execute_script("""
                document.getElementById('sikd_rek_jenis_id').style.display = "inline";

                """)
            Select(self._driver.find_element_by_id("sikd_rek_jenis_id")).select_by_visible_text(f'[{data["rekening_jenis"]}] {data["nama_jenis"]}')
        
            rek_obj=self._driver.find_element_by_id('sikd_rek_obj_id')
            WebDriverWait(self._driver, 5).until(expected_conditions.staleness_of(rek_obj))
            rek_obj=WebDriverWait(self._driver, 5).until(expected_conditions.presence_of_element_located((By.ID,'sikd_rek_obj_id')))
            Select(rek_obj).select_by_visible_text(f'[{data["rekening_objek"]}] {data["nama_objek"]}')

            rek_rinc_obj=self._driver.find_element_by_id('sikd_rek_rincian_obj_id')
            WebDriverWait(self._driver, 5).until(expected_conditions.staleness_of(rek_rinc_obj))
            rek_rinc_obj=WebDriverWait(self._driver, 5).until(expected_conditions.presence_of_element_located((By.ID,'sikd_rek_rincian_obj_id')))
            Select(rek_rinc_obj).select_by_visible_text(f'[{data["rekening_rincian"]}] {data["nama_rincian"]}')

            jumlah=self._driver.find_element_by_id('jumlah_0')
            WebDriverWait(self._driver, 5).until(expected_conditions.staleness_of(jumlah))
            jumlah=WebDriverWait(self._driver, 5).until(expected_conditions.presence_of_element_located((By.ID,'jumlah_0')))
            
            jumlah.clear()

            jumlah.send_keys(str(data["jumlah"]))
            self._driver.implicitly_wait(1)

            self._driver.find_element_by_id('tb-simpan').click()
            self.switchToDefault()
        except Exception as err:
            logging.error(err)