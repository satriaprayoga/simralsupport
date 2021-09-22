import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
from urllib import parse

from simral.driver.SimralDriver import SimralDriver

class DppaSimralDriver(SimralDriver):

    def __init__(self,kode_skpd,nama_skpd):
        self.kode_skpd=kode_skpd
        self.nama_skpd=nama_skpd
        super().__init__()
       
    def set_skpd(self,kode_skpd,nama_skpd):
        self.kode_skpd=kode_skpd
        self.nama_skpd=nama_skpd

    def import_pilih_kegiatan(self,periode,kode_sub_skpd,sub_skpd):
        try:
            logging.info(f'Import kegiatan {self.nama_skpd} sub unit {sub_skpd}')
            self.switchFrame("content")
            self._driver.execute_script("""
                document.getElementById('id_periode_prbhn').style.display = "inline";

                """)
            Select(self._driver.find_element_by_id("id_periode_prbhn")).select_by_visible_text(periode)
            self._driver.execute_script("""
            document.getElementById('id_satker').style.display = "inline";

            """)
            Select(self._driver.find_element_by_id("id_satker")).select_by_visible_text(f'[{self.kode_skpd}] {self.nama_skpd}')
            self._driver.execute_script("""
            document.getElementById('id_sub_skpd').style.display = "inline";

            """)
            Select(self._driver.find_element_by_id("id_sub_skpd")).select_by_visible_text(f'[{kode_sub_skpd}] {sub_skpd}')
            self._driver.execute_script("""
            document.getElementById('jns_sumber_data').style.display = "inline";

            """)
            Select(self._driver.find_element_by_id("jns_sumber_data")).select_by_visible_text('DPA Sebelumnya')
            self._driver.find_element_by_id("tb-input").click()
            self.switchToDefault()
        except Exception as err:
             logging.error(err)

    def import_kegiatan(self,jnsPerubahan):
        try:
            logging.info("Memulai Import Kegiatan....")
            self.switchFrame("content")
            self._driver.execute_script("""
            var lists=document.getElementsByTagName('select');
            for(i=0;i<lists.length;i++){
                lists[i].style.display="inline"
            }

            """)
            selects=self._driver.find_elements_by_tag_name('select')
            if(len(selects)>0):
                logging.info("%s kegiatan akan diimport",len(selects))
                for i in selects:
                     Select(i).select_by_visible_text(jnsPerubahan)
                self._driver.find_element_by_name('import').submit()
            else:
                logging.info("tidak ada kegiatan/kegiatan sudah pernah diimport")
            self._driver.refresh()
            self.switchToDefault()
        except Exception as err:
            logging.error(err)

    def input_list_kegiatan(self,periode,sub_skpd,bidang_urusan,program):
        try:
            logging.info(f'input dppa [{self.kode_skpd}] {self.nama_skpd} {sub_skpd} {bidang_urusan} {program}')
            self._driver.implicitly_wait(1)
            self.switchFrame("content")
        
            self._driver.execute_script("""
            document.getElementById('apbd_pergeseran_id').style.display = "inline";

            """)
            Select(self._driver.find_element_by_id("apbd_pergeseran_id")).select_by_visible_text(periode)
            
            self._driver.execute_script("""
            document.getElementById('sikd_satker_id').style.display = "inline";

            """)
            Select(self._driver.find_element_by_id("sikd_satker_id")).select_by_visible_text(f'[{self.kode_skpd}] {self.nama_skpd}')
            self._driver.implicitly_wait(1)
            self._driver.execute_script("""
            document.getElementById('sikd_sub_skpd_id').style.display = "inline";

            """)
            Select(self._driver.find_element_by_id("sikd_sub_skpd_id")).select_by_visible_text(sub_skpd)
            self._driver.implicitly_wait(1)
            self._driver.execute_script("""
            document.getElementById('sikd_bidang_id').style.display = "inline";

            """)
            Select(self._driver.find_element_by_id("sikd_bidang_id")).select_by_visible_text(bidang_urusan)
            self._driver.implicitly_wait(1)
            self._driver.execute_script("""
            document.getElementById('sikd_program_id').style.display = "inline";

            """)
            Select(self._driver.find_element_by_id("sikd_program_id")).select_by_visible_text(program)
            self._driver.implicitly_wait(1)
            
            soup=BeautifulSoup(self._driver.page_source,"html.parser")
            table=soup.find('table', class_='table table-striped table-bordered table-condensed table-hover')
            links=table.find_all('a')

            if len(links)>0 and links!=None:
                link_sub_kegiatan=[]
                for l in links:
                    if(l.has_attr('id')) and l['id']=='link_subkegiatan':
                        href=l['href']
                        query_part=parse.urlsplit(href)
                        query_dict=dict(parse.parse_qsl(query_part.query))
                        query_dict["link"]=href
                        link_sub_kegiatan.append(query_dict)
                
                self.switchToDefault()
                return link_sub_kegiatan
            else:
                return None

        except Exception as err:
            logging.error(err)

    def input_pilih_kegiatan(self,kegiatan):
        try:
            logging.info(f'Memilih Kegiatan {kegiatan["nama_giat"]}')
            self.switchFrame("content")
            self._driver.implicitly_wait(1)
            self._driver.find_element_by_partial_link_text(f'{kegiatan["nama_giat"]}').click()
            #self._driver.find_element_by_xpath('//a[@href="'+link+'"]').click()
            self._driver.implicitly_wait(1)
            self.switchToDefault()
            self.switchFrame("content")
            self._driver.find_element_by_partial_link_text("Sub Kegiatan").click()
            self.switchToDefault()
        except Exception as err:
            logging.error(err)
        

    def input_list_sub_kegiatan(self,kegiatan):
        try:
            logging.info(f'daftar sub kegiatan {kegiatan["nama_giat"]}')
            self.switchFrame("content")
            soup=BeautifulSoup(self._driver.page_source,"html.parser")
            table=soup.find('table', class_='table table-striped table-bordered table-condensed table-hover')
            links=table.find_all('a')
            link_rincians=[]
            for l in links:
                if(l.has_attr('id')):
                    if l['id']=='link_anggaran':
                        href=l['href']
                        query_part=parse.urlsplit(href)
                        query_dict=dict(parse.parse_qsl(query_part.query))
                        query_dict["link"]=href
                        link_rincians.append(query_dict)
                    
            self.switchToDefault()
            return link_rincians
        except Exception as err:
            logging.error(err)

    def input_pilih_sub_kegiatan(self,sub_kegiatan):
        try:
            logging.info(f'memilih {sub_kegiatan["kode_sub_giat"]} {sub_kegiatan["nama_sub_giat"]}')
            self.switchFrame("content")
            self._driver.find_element_by_partial_link_text(f'{sub_kegiatan["kode_sub_giat"]}').click()
            #self._driver.find_element_by_xpath('//a[@href="'+link+'"]').click()
            self._driver.implicitly_wait(1)
            self.switchToDefault()
            self.switchFrame("content")
            self._driver.find_element_by_partial_link_text("Rincian Anggaran").click()
            self.switchToDefault()
        except Exception as err:
            logging.error(err)

    def input_list_rincian(self,sub_kegiatan):
        try:
            logging.info(f'list rincian rekening sub kegiatan: {sub_kegiatan["kode_sub_giat"]}')
            self.switchFrame("content")
            self._driver.implicitly_wait(1)
            soup=BeautifulSoup(self._driver.page_source,"html.parser")
            table=soup.find('table',class_="table table-striped table-bordered table-condensed table-hover")
            links=table.find_all('a')
            links_rekening=[]
            for l in links:
                if (l.has_attr('id') and l['id']=='kd_rekening' and l.text.strip()!=''):
                    href=l['href']
                    query_part=parse.urlsplit(href)
                    query_dict=dict(parse.parse_qsl(query_part.query))
                    query_dict["link"]=href
                    links_rekening.append(query_dict)
            self.switchToDefault()
            return links_rekening
        except Exception as err:
            logging.error(err)

    def input_edit_rincian(self,rincian,rincian_link):
        if(rincian==None and rincian_link!=None):
            self.input_hapus_rincian(rincian, rincian_link) #if rincian==None else self.input_tambah_rincian(rincian,rincian_link)
        elif(rincian!=None and rincian_link==None):
            self.input_tambah_rincian(rincian, rincian_link)
        else:                    
            if(rincian['kode_akun']==rincian_link['idRekSubRincObj']):
                self.input_copy_rincian(rincian,rincian_link)
            else:
                self.input_tambah_rincian(rincian,rincian_link)
                self.input_hapus_rincian(rincian,rincian_link)
        
    def input_copy_rincian(self,rincian,rincian_link):
        try:
            logging.info(f'Cek rincian {rincian["kode_akun"]} SIPD => {rincian_link["idRekSubRincObj"]} SIMRAL')
            self.switchFrame("content")
            self._driver.implicitly_wait(1)
            self._driver.find_element_by_xpath('//a[@href="'+rincian_link['link']+'"]').click()
            self._driver.implicitly_wait(1)
            jumlah_simral=self.get_jumlah_perubahan()
            jumlah_sipd=rincian["total_rincian"]
            logging.info(f'jumlah di simral : {jumlah_simral} jumlah di sipd {jumlah_sipd}')
            if jumlah_simral!=jumlah_sipd:
                logging.info("Selisih {}".format(jumlah_sipd-jumlah_simral))
                logging.info("Merubah rincian")
                self._driver.find_element_by_id('tb-edit').click()
                self.switchToDefault()
                self.switchFrame("content")
                volume=self._driver.find_element_by_id('volume_rinc_0')
                volume.clear()
                satuan=self._driver.find_element_by_id('satuan_rinc_0')
                satuan.clear()
                harga=self._driver.find_element_by_id('harga_rinc_0')
                harga.clear()

                volume.send_keys('1')
                satuan.send_keys('paket')
                harga.send_keys(str(rincian['total_rincian']))

                self._driver.implicitly_wait(1)
                        
                self._driver.find_element_by_id('tb-simpan').click()
                self.switchToDefault()
                self.switchFrame("content")
                self._driver.implicitly_wait(0.5)
            else:
                logging.info("Jumlah sama. Tidak ada perubahan")

            self._driver.find_element_by_id('tb-balik').click()
            self.switchToDefault()
        except Exception as err:
            logging.error(err)
    
    def input_tambah_rincian(self,rincian,rincian_link):
        try:
            self.switchFrame("content")
            self._driver.find_element_by_id('tb-input').click()
            self.switchToDefault()
            self.switchFrame("content")
            logging.info("Menambah rincian {} {} {}".format(rincian['kode_akun'], rincian['nama_akun'], rincian['total_rincian']))

            self._driver.execute_script('''

            ''')


        except Exception as err:
            logging.error(err)

    def input_hapus_rincian(self,rincian,rincian_link):
        try:
            logging.info(f'Menghapus {rincian_link["idRekSubRincObj"]} SIMRAL')
            self.switchFrame("content")
            self._driver.implicitly_wait(1)
            self._driver.find_element_by_xpath('//a[@href="'+rincian_link['link']+'"]').click()
            self._driver.implicitly_wait(1)
            self._driver.find_element_by_id('tb-edit').click()
            self.switchToDefault()
            self.switchFrame("content")
            volume=self._driver.find_element_by_id('volume_rinc_0')
            volume.clear()
            satuan=self._driver.find_element_by_id('satuan_rinc_0')
            satuan.clear()
            harga=self._driver.find_element_by_id('harga_rinc_0')
            harga.clear()

            volume.send_keys('1')
            satuan.send_keys('paket')
            harga.send_keys(str(0))

            self._driver.implicitly_wait(3)
                        
            self._driver.find_element_by_id('tb-simpan').click()
            self.switchToDefault()
            self.switchFrame("content")
            self._driver.implicitly_wait(0.5)

            self._driver.find_element_by_id('tb-balik').click()
            self.switchToDefault()
        except Exception as err:
            logging.error(err)

    def back(self):
        self.switchFrame("content")
        self._driver.implicitly_wait(0.5)

        self._driver.find_element_by_id('tb-balik').click()
        self.switchToDefault()

    def refresh(self):
        self.switchFrame("content")
        self._driver.implicitly_wait(0.5)

        self._driver.find_element_by_id('tb-muat-ulang').click()
        self.switchToDefault()

    def get_jumlah_perubahan(self):
        soup = BeautifulSoup(self._driver.page_source,"html.parser")
        jumlah_ssdh=soup.find('div',id="jml_pagu_ssdh")
        jumlah_pagu=jumlah_ssdh.string.strip().replace(".","").replace(",00","")
        return int(jumlah_pagu)

    def get_jenis_belanja(kode_akun):
        return kode_akun[0:6]

    def get_objek_belanja(kode_akun):
        return kode_akun[0:9]

    def get_rincian_objek(kode_akun):
        return kode_akun[0:12]