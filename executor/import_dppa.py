from PyInquirer.prompt import prompt
from simral.driver.DppaSimralDriver import DppaSimralDriver
from simral.config.Config import Config
from simral.sipd.Backup import findAllSkpd, findSubSkpd

import sqlite3

conn = sqlite3.connect("sipd_backup.db")

def skpd_prompt():
   skpd=findAllSkpd(conn)
   choices=[f'{d["kode_skpd"]} {d["nama_skpd"]}' for d in skpd]
   choices.append("Back")
   skpd_prompt={
      'type':'list',
      'name':'skpd',
      'message':'Pilih SKPD yang akan diimpor: ',
      'choices':choices
   }
   answer=prompt(skpd_prompt)
   return answer['skpd']

def dppa_operation_prompt(skpdChoice):
   if skpdChoice == 'Back':
      return skpd_prompt()
   operation_form={
      'type':'list',
      'name':'operation',
      'message':'Pilih Operasi pada SKPD: {}'.format(skpdChoice),
      'choices':['Import DPPA','Input DPPA','Back']
   }
   answer=prompt(operation_form)
   if answer['operation']=='Back':
      skpd_prompt()
   elif answer['operation']=='Import DPPA':
      targetSkpd=skpdChoice.strip().split(" ",1)
      import_dppa_operation(targetSkpd[0],targetSkpd[1])
   else:
      skpd_prompt()
   
def import_dppa_operation(kode_skpd,nama_skpd):
   subunits=findSubSkpd(conn,kode_skpd,nama_skpd)
   if len(subunits)>=0:
      dppa=DppaSimralDriver(kode_skpd,nama_skpd)
      conf=Config()
      anggaran_config=conf.get_simral_perubahan_config()
      dppa.connect(r'./chromedriver.exe')
      dppa.get_captcha()
      captcha_prompt={
        'type': 'input',
        'name': 'captcha',
        'message': 'Masukkan kode captcha?',
        'filter': lambda val: int(val)
      }
      answer=prompt(captcha_prompt)
      dppa.login(anggaran_config['username'],anggaran_config['password'],anggaran_config['cfg'],answer['captcha'])
      for s in subunits:
         if s['nama_sub_skpd']!=s['nama_skpd']:
            dppa.select_modul("Perubahan","objTreeMenu_1_node_2_2")
            dppa.import_pilih_kegiatan(anggaran_config['periode'],s['kode_sub_skpd'],s['nama_sub_skpd'])
            dppa.import_kegiatan(anggaran_config['jenis_perubahan'])
      dppa.quit_driver()
   conn.close()

   