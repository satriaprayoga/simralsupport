import logging

from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup

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

def pilih_skpd(driver, periode, skpd, sub_skpd):
    try:
        logging.info("Memilih kegiatan: Periode= %s, SKPD= %s, Sub-SKPD= %s ",periode,skpd,sub_skpd)
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
        driver.execute_script("""
        document.getElementById('sikd_sub_skpd_id').style.display = "inline";

        """)
        Select(driver.find_element_by_id("sikd_sub_skpd_id")).select_by_visible_text(sub_skpd)
        
        soup=BeautifulSoup(driver.page_source,"html.parser")
        table=soup.find('table', class_='table table-striped table-bordered table-condensed table-hover')
        print(table.prettify())
        links=table.find_all('a')
        link_sub_kegiatans=[]
        for l in links:
            if(l.has_attr('id')):
                if l['id']=='link_subkegiatan':
                    link_sub_kegiatans.append(l['href'])
        driver.switch_to.default_content()
        return link_sub_kegiatans
    except Exception as err:
        logging.error(err)

def pilih_sub_kegiatan(driver,kegiatan_link):
    try:
        logging.info("Mememilih sub kegiatan")
        driver.switch_to.frame(driver.find_element_by_name("content"))
        driver.implicitly_wait(1)
        driver.find_element_by_xpath('//a[@href="'+kegiatan_link+'"]').click()
       
        soup=BeautifulSoup(driver.page_source,"html.parser")
        table=soup.find('table', class_='table table-striped table-bordered table-condensed table-hover')
        links=table.find_all('a')
        link_rincians=[]
        for l in links:
            if(l.has_attr('id')):
                if l['id']=='link_anggaran':
                    link_rincians.append(l['href'])
        driver.switch_to.default_content()
        return link_rincians

    except Exception as err:
        logging.error(err)

def pilih_rincian_anggaran(driver,rincian_link):
    try:
        logging.info("memilih rincian")
        driver.switch_to.frame(driver.find_element_by_name("content"))
        driver.implicitly_wait(1)
        driver.find_element_by_xpath('//a[@href="'+rincian_link+'"]').click()

        soup=BeautifulSoup(driver.page_source,"html.parser")
        table=soup.find('table',class_="table table-striped table-bordered table-condensed table-hover")
        links=table.find_all('a')
        links_rekening=[]
        for l in links:
            if (l.has_attr('id') and l['id']=='kd_rekening' and l.text.strip()!=''):
                links_rekening.append({"link":l['href'],"rekening":l.text})
            
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