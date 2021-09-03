import logging

from selenium.webdriver.support.select import Select

NAV_ELEMENT="nav"
MODULE_MENU="SelectModul"
PERUBAHAN_MENU="Perubahan"
PERUBAHAN_LINK="objTreeMenu_1_node_2_2"
PERUBAHAN_LAT_LINK="objTreeMenu_1_node_1_2"

"""
Navigasi browser ke modul Perubahan
"""
def modul_perubahan(driver):
    try:
        logging.info("Navigasi ke modul perubahan")
        driver.implicitly_wait(2)
        driver.switch_to.frame(driver.find_element_by_name(NAV_ELEMENT))
        moduleMenu=driver.find_element_by_id(MODULE_MENU)
        Select(moduleMenu).select_by_visible_text(PERUBAHAN_MENU)
        driver.execute_script("""
        document.getElementById('objTreeMenu_1_node_2_2').style.display = "inline"
        """)
        driver.find_element_by_xpath("//div[@id='objTreeMenu_1_node_2_2']//nobr//a").click()
        driver.switch_to.default_content()
    except Exception as err:
        logging.error(err)

def list_sub_skpd(driver):
    try:
        logging.info("Mengumpulkan data sub skdp")
        driver.implicitly_wait(3)
        driver.switch_to.frame(driver.find_element_by_name("content"))
        driver.execute_script("""
        document.getElementById('id_sub_skpd').style.display = "inline";

        """)
        select_sub_skpd=Select(driver.find_element_by_id("id_sub_skpd"))
        options=select_sub_skpd.options
        driver.switch_to.default_content()
        return options
    except Exception as err:
        logging.error(err)

"""
Pilih Kegiatan yang akan diimport
"""
def pilih_kegiatan(driver,periode,skpd,sub_skpd):
    try:
        logging.info("Import DPA ke DPA-P: Periode= %s, SKPD= %s, Sub-SKPD= %s ",periode,skpd,sub_skpd)
        driver.implicitly_wait(5)
        driver.switch_to.frame(driver.find_element_by_name("content"))
        driver.execute_script("""
        document.getElementById('id_periode_prbhn').style.display = "inline";

        """)
        Select(driver.find_element_by_id("id_periode_prbhn")).select_by_visible_text(periode)
        driver.execute_script("""
        document.getElementById('id_satker').style.display = "inline";

        """)
        Select(driver.find_element_by_id("id_satker")).select_by_visible_text(skpd)
        driver.execute_script("""
        document.getElementById('id_sub_skpd').style.display = "inline";

        """)
        Select(driver.find_element_by_id("id_sub_skpd")).select_by_visible_text(sub_skpd)
        driver.execute_script("""
        document.getElementById('jns_sumber_data').style.display = "inline";

        """)
       
        Select(driver.find_element_by_id("jns_sumber_data")).select_by_visible_text('DPA Sebelumnya')
        driver.find_element_by_id("tb-input").click()
        driver.switch_to.default_content()
    except Exception as err:
        logging.error(err)

"""
Import Kegiatan
"""
def import_kegiatan(driver,jnsPerubahan):
    try:
        logging.info("Memulai Import Kegiatan....")
        driver.implicitly_wait(3)
        driver.switch_to.frame(driver.find_element_by_name("content"))
        driver.execute_script("""
        var lists=document.getElementsByTagName('select');
        for(i=0;i<lists.length;i++){
            lists[i].style.display="inline"
        }

        """)
        selects=driver.find_elements_by_tag_name('select')
        logging.info("%s kegiatan akan diimport",len(selects))
        for i in selects:
            Select(i).select_by_visible_text(jnsPerubahan)
        driver.find_element_by_name('import').submit()
        driver.refresh()
        driver.switch_to.default_content()
    except Exception as err:
        logging.error(err)
    