from PyInquirer.prompt import prompt
from simral.driver.JurnalPenyesuaian import JPDriver
from simral.config.Config import Config

def file_jurnal_prompt():
    file_propmpt={
        'type': 'input',
        'name': 'file',
        'message': 'File Jurnal Penyesuaian',
        'default': 'JURNAL_PENYESUAIAN_UTANGBARJAS.xlsx',
    }
    answer=prompt(file_propmpt)
    return answer['file']

def jurnal_penyesuaian_operation(filename):
    config=Config()
    driver=JPDriver()
    data=driver.load_jurnal_penyesuaian(filename)
    driver.connect(r'./chromedriver.exe',False)
    driver.get_captcha()
    kasda_config=config.get_simral_kasda_config()
    captcha_prompt={
    'type': 'input',
    'name': 'captcha',
    'message': 'Masukkan kode captcha?',
    'filter': lambda val: int(val)
    }
    answer=prompt(captcha_prompt)
    driver.login(kasda_config['username'],kasda_config['password'],kasda_config['cfg'],answer['captcha'])
   
    for index,row in data.iterrows():
        driver.select_modul("Akuntansi", "objTreeMenu_1_node_1_5_8")
        driver.pilih_skpd(row['Kode'],row['Satuan Kerja'],row['Sub Unit'])
        driver.input_jurnal_penyesuaian(row['Tgl Transaksi'],row['Uraian Transaksi'],row['No Bukti'],row['Kode Rekening Utang'],row['Uraian Utang'],row['Jumlah Debet Utang'],row['Kode Rekening Beban'],row['Uraian Beban'],row['Jumlah Kredit Beban'])