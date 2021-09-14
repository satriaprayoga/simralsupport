import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
from urllib import parse

from simral.driver.SimralDriver import SimralDriver

class ValidasiDriver(SimralDriver):

    def __init__(self):
        self.invalid=[]
        super().__init__()

    def find_sp2d(self,noSp2d):
        try:
            logging.info("Mencari SP2D dengan nomor: {}".format(noSp2d))
            self._driver.implicitly_wait(1)
            self.switchFrame("content")

            search_field=WebDriverWait(self._driver,1).until(EC.presence_of_element_located((By.ID,"kt_kunci")))
            search_field.clear()
            search_field.send_keys(f'02.03/{noSp2d}')

            search_btn=self._driver.find_element_by_name("submitSearch")
            search_btn.click()
            self._driver.implicitly_wait(1)
            self.switchToDefault()
            self.switchFrame("content")
            soup=BeautifulSoup(self._driver.page_source,"html.parser")
            table=soup.find('table', class_='table table-striped table-bordered table-condensed table-hover')
            if table:
                tr=table.find_all('tr')
                target_row=tr[2]
                td=target_row.find_all('td')
                link_column=td[1]
                href=link_column.find('a')
                #print(href['href'])
                if href:
                    sp2d=link_column.text
                    logging.info(f'SP2D dengan nomor {sp2d} ditemukan')
                    status_column=td[4].text.strip()
                    jumlah_column=td[5].text.strip()
                    logging.info(f'Status SP2D {status_column}')
                    logging.info(f'Jumlah SP2D {jumlah_column.replace(".","").replace(",00","")}')
                    data={
                            "link":href['href'],
                            "noSp2d":sp2d.strip(),
                            "status":status_column.strip(),
                            "jumlah":int(jumlah_column.strip().replace(".","").replace(",00",""))
                    }
                    self._driver.find_element_by_xpath('//a[@href="'+href['href']+'"]').click()
                    self.switchToDefault()
                    return data
                else:
                    self.switchToDefault()
                    return None
            else:
                self.switchToDefault()
                return None
        except Exception as err:
            logging.error(err)

    def validasi_sp2d(self,data,refTable,tanggal_cair):
        try:
            if data == None:
                logging.info(f'SP2D {refTable["no_sp2d"]} tidak ditemukan')
                lostData={"noSp2d":refTable["no_sp2d"],"jumlah":refTable["jumlah"]}
                self.add_invalid_data(lostData,"SP2D tidak ada")
                self._driver.switch_to.default_content()
            else:
                logging.info(f'Memvalidasi {data["noSp2d"]}')
                if data['status']=="Sudah Dicairkan":
                    logging.info(f'SP2D {data["noSp2d"]} sudah dicairkan')
                    lostData={"noSp2d":refTable["no_sp2d"],"jumlah":refTable["jumlah"]}
                    self.add_invalid_data(lostData,"Sudah dicairkan")
                    self._driver.switch_to.default_content()
                elif data['status']=='Proses Bank':
                    if data['jumlah']!=int(refTable['jumlah']):
                        logging.info(f'SP2D {data["noSp2d"]} jumlah tidak sama')
                        lostData={"noSp2d":refTable["no_sp2d"],"jumlah":refTable["jumlah"]}
                        self.add_invalid_data(lostData,"Jumlah tidak sama")
                        self._driver.switch_to.default_content()
                    else:

                        self.switchFrame('content')
                        self._driver.find_element_by_id('tb-edit').click()
                        self._driver.implicitly_wait(1)

                        self._driver.switch_to.default_content()
                        self._driver.switch_to.frame(self._driver.find_element_by_name("content"))
                        self._driver.execute_script("""
                        document.getElementById('status').style.display = "inline";

                        """)
                        Select(self._driver.find_element_by_id('status')).select_by_visible_text("Sudah Dicairkan")

                        self._driver.find_element_by_id("tgl_pencairan").clear()

                        self._driver.find_element_by_id("tgl_pencairan").send_keys(tanggal_cair)

                        self._driver.find_element_by_id('tb-simpan').click()
                        self._driver.implicitly_wait(1)
                        self._driver.switch_to.default_content()
                else:
                    logging.info(f'SP2D {data["noSp2d"]} ditolak')
                    lostData={"noSp2d":refTable["no_sp2d"],"jumlah":refTable["jumlah"]}
                    self.add_invalid_data(lostData,"Ditolak")
                    self._driver.switch_to.default_content()
        except Exception as err:
            logging.error(err)


    def add_invalid_data(self,data,reason):
        data["keterangan"]=reason.strip()
        self.invalid.append(data) 