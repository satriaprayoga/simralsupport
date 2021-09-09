import logging

from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from bs4 import BeautifulSoup

NAV_ELEMENT="nav"
MODULE_MENU="SelectModul"
KASDA_MENU="Kas Daerah"
PERUBAHAN_LINK="objTreeMenu_1_node_2_4"
PERUBAHAN_LAT_LINK="objTreeMenu_1_node_1_2"

def modul_kasda(driver):
    try:
        logging.info("Navigasi ke modul {}".format(KASDA_MENU))
        driver.implicitly_wait(2)
        driver.switch_to.frame(driver.find_element_by_name(NAV_ELEMENT))
        moduleMenu=driver.find_element_by_id(MODULE_MENU)
        Select(moduleMenu).select_by_visible_text(KASDA_MENU)
        driver.execute_script("""
        document.getElementById('objTreeMenu_1_node_2_4').style.display = "inline"
        """)
        driver.find_element_by_xpath("//div[@id='objTreeMenu_1_node_2_4']//nobr//a").click()
        driver.switch_to.default_content()
    except Exception as err:
        logging.error(err)

def find_spd2d(driver, noSp2d, refBjb):
    try:
        logging.info("Mencari SP2D dengan nomor: {}".format(noSp2d))
        driver.implicitly_wait(2)
        driver.switch_to.frame(driver.find_element_by_name("content"))
        search_field=WebDriverWait(driver,1).until(expected_conditions.presence_of_element_located((By.ID,"kt_kunci")))
        search_field.clear()
        search_field.send_keys(noSp2d)

        search_btn=driver.find_element_by_name("submitSearch")
        search_btn.click()
        driver.implicitly_wait(1)
        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element_by_name("content"))
        soup=BeautifulSoup(driver.page_source,"html.parser")
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
                driver.find_element_by_xpath('//a[@href="'+href['href']+'"]').click()
                driver.switch_to.default_content()
                return data
            else:
                return None
        else:
            return None
    except Exception as err:
        logging.error(err)

def validasi_sp2d(driver, data, tanggal_cair):
    try:
        logging.info(f'Memvalidasi {data["noSp2d"]}')
        driver.switch_to.frame(driver.find_element_by_name("content"))
        driver.find_element_by_id('tb-edit').click()
        driver.implicitly_wait(1)

        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element_by_name("content"))
        driver.execute_script("""
        document.getElementById('status').style.display = "inline";

        """)
        Select(driver.find_element_by_id('status')).select_by_visible_text("Sudah Dicairkan")

        driver.find_element_by_id("tgl_pencairan").clear()

        driver.find_element_by_id("tgl_pencairan").send_keys(tanggal_cair)

        driver.find_element_by_id('tb-simpan').click()
        driver.implicitly_wait(1)
        driver.switch_to.default_content()
    except Exception as err:
        logging.error(err)