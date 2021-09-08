import logging

from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup

from urllib import parse

NAV_ELEMENT="nav"
MODULE_MENU="SelectModul"
PERUBAHAN_MENU="Perubahan"
PERUBAHAN_LINK="objTreeMenu_1_node_2_4_3"
PERUBAHAN_LAT_LINK="objTreeMenu_1_node_1_2"

def modul_belanja_dppa(driver):
    try:
        logging.info("Navigasi ke modul perubahan")
        driver.implicitly_wait(2)
        driver.switch_to.frame(driver.find_element_by_name(NAV_ELEMENT))
        moduleMenu=driver.find_element_by_id(MODULE_MENU)
        Select(moduleMenu).select_by_visible_text(PERUBAHAN_MENU)
        driver.execute_script("""
        document.getElementById('objTreeMenu_1_node_2_4_3').style.display = "inline"
        """)
        driver.find_element_by_xpath("//div[@id='objTreeMenu_1_node_2_4_3']//nobr//a").click()
        driver.switch_to.default_content()
    except Exception as err:
        logging.error(err)

def list_kegiatan(driver,periode,skpd,sub_skpd,bidang_urusan,program):
    try:
        logging.info(f'List kegiatan pada {skpd} {sub_skpd} {bidang_urusan} {program}')
        driver.implicitly_wait(1)
        driver.switch_to.frame(driver.find_element_by_name("content"))
        
        driver.execute_script("""
        document.getElementById('apbd_pergeseran_id').style.display = "inline";

        """)
        Select(driver.find_element_by_id("apbd_pergeseran_id")).select_by_visible_text(periode)
        
        driver.execute_script("""
        document.getElementById('sikd_satker_id').style.display = "inline";

        """)
        Select(driver.find_element_by_id("sikd_satker_id")).select_by_visible_text(skpd)
        driver.implicitly_wait(1)
        driver.execute_script("""
        document.getElementById('sikd_sub_skpd_id').style.display = "inline";

        """)
        Select(driver.find_element_by_id("sikd_sub_skpd_id")).select_by_visible_text(sub_skpd)
        driver.implicitly_wait(1)
        driver.execute_script("""
        document.getElementById('sikd_bidang_id').style.display = "inline";

        """)
        Select(driver.find_element_by_id("sikd_bidang_id")).select_by_visible_text(bidang_urusan)
        driver.implicitly_wait(1)
        driver.execute_script("""
        document.getElementById('sikd_program_id').style.display = "inline";

        """)
        Select(driver.find_element_by_id("sikd_program_id")).select_by_visible_text(program)
        driver.implicitly_wait(1)
        
        soup=BeautifulSoup(driver.page_source,"html.parser")
        table=soup.find('table', class_='table table-striped table-bordered table-condensed table-hover')
        links=table.find_all('a')
        link_sub_kegiatan=[]

        if(links):
            for l in links:
                if(l.has_attr('id')) and l['id']=='link_subkegiatan':
                    href=l['href']
                    query_part=parse.urlsplit(href)
                    query_dict=dict(parse.parse_qsl(query_part.query))
                    query_dict["link"]=href
                    link_sub_kegiatan.append(query_dict)
        
        driver.switch_to.default_content()
        return link_sub_kegiatan

    except Exception as err:
        logging.error(err)

def choose_kegiatan(driver, kegiatan, kegiatan_link, lookOnly=True):
    try:
        logging.info(f'Mememilih kegiatan {kegiatan["nama_giat"]}')
        driver.switch_to.frame(driver.find_element_by_name("content"))
        driver.implicitly_wait(1)
        driver.find_element_by_xpath('//a[@href="'+kegiatan_link+'"]').click()
        driver.implicitly_wait(1)
        if lookOnly:
            driver.find_element_by_id('tb-balik').click()
            driver.implicitly_wait(1)
        driver.switch_to.default_content()
    except Exception as err:
        logging.error(err)


def list_sub_kegiatan(driver,lookOnly=True):
    try:
        logging.info("Mememilih sub kegiatan")
        driver.switch_to.frame(driver.find_element_by_name("content"))
        driver.implicitly_wait(1)
        soup=BeautifulSoup(driver.page_source,"html.parser")
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
                   
        if lookOnly:
               driver.find_element_by_id('tb-balik').click()
        driver.switch_to.default_content()
        return link_rincians

    except Exception as err:
        logging.error(err)

def choose_sub_giat(driver,sub,link_sub):
    try:
        driver.switch_to.frame(driver.find_element_by_name("content"))
        driver.implicitly_wait(1)
        logging.info(f'Memilih sub kegiatan: {sub["kode_sub_giat"]} {sub["nama_sub_giat"]}')
       
        driver.find_element_by_xpath('//a[@href="'+link_sub+'"]').click()
        driver.implicitly_wait(1)
      
        driver.switch_to.default_content()
    except Exception as err:
        logging.error(err)

def list_akun(driver,sub_giat,lookOnly=True):
    try:
        logging.info(f'daftar rekening belanja pada kegiatan: {sub_giat["kode_sub_giat"]} {sub_giat["nama_sub_giat"]}')
        driver.switch_to.frame(driver.find_element_by_name("content"))
        driver.implicitly_wait(1)
        soup=BeautifulSoup(driver.page_source,"html.parser")
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
        if lookOnly:
            driver.find_element_by_id('tb-balik').click()
        driver.switch_to.default_content()
        return links_rekening
    except Exception as err:
        logging.error(err)



def edit_rincian_anggaran(driver,rekening_link):
    try:
        logging.info("memilih rincian")
        driver.switch_to.frame(driver.find_element_by_name("content"))
        driver.implicitly_wait(1)
        driver.find_element_by_xpath('//a[@href="'+rekening_link+'"]').click()
      
        driver.implicitly_wait(1)
    
        driver.find_element_by_id('tb-edit').click()
        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element_by_name("content"))
        driver.implicitly_wait(0.5)

        volume=driver.find_element_by_id('volume_rinc_0')
        volume.clear()
        satuan=driver.find_element_by_id('satuan_rinc_0')
        satuan.clear()
        harga=driver.find_element_by_id('harga_rinc_0')
        harga.clear()

        volume.send_keys('1')
        satuan.send_keys('paket')
        harga.send_keys('1150000')

        driver.implicitly_wait(1)

        driver.find_element_by_id('tb-simpan').click()
        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element_by_name("content"))
        driver.implicitly_wait(0.5)

        driver.find_element_by_id('tb-balik').click()
        driver.switch_to.default_content()
       
    except Exception as err:
        logging.error(err)