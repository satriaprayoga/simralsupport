import logging
from PyInquirer.prompt import prompt
from prompt_toolkit.interface import CommandLineInterface
from simral.driver.DppaSimralDriver import DppaSimralDriver
from simral.config.Config import Config
from simral.sipd.Backup import findAllSkpd, findKegiatan, findKegiatanByProgram, findProgramFromIdSkpd, findRekeningAkun, findSkpdByCode, findSubSkpd, findSubkegiatan

import sqlite3



def skpd_prompt():
   conn = sqlite3.connect("sipd_backup.db")
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
   conn.close()
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
   elif answer['operation']=='Input DPPA':
      targetSkpd=skpdChoice.strip().split(" ",1)
      input_dppa_operation(targetSkpd[0],targetSkpd[1])
   else:
      skpd_prompt()
   
def import_dppa_operation(kode_skpd,nama_skpd):
   conn = sqlite3.connect("sipd_backup.db")
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
            dppa.select_modul_by_name("Perubahan","Import DPA")
            #dppa.select_modul("Perubahan","objTreeMenu_1_node_2_2")
            dppa.import_pilih_kegiatan(anggaran_config['periode'],s['kode_sub_skpd'],s['nama_sub_skpd'])
            dppa.import_kegiatan(anggaran_config['jenis_perubahan'])
      dppa.quit_driver()
   conn.close()

def input_dppa_operation(kode_skpd,nama_skpd):
   conn = sqlite3.connect("sipd_backup.db")
   skpd=findSkpdByCode(conn,kode_skpd)
   
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
      
   
   programs=findProgramFromIdSkpd(conn,skpd['id_skpd'])
   for p in programs:
      dppa.select_modul("Perubahan","objTreeMenu_1_node_2_4_3")
      kgtns=findKegiatan(conn,p['kode_skpd'],p['kode_sub_skpd'],p['kode_bidang_urusan'],p['kode_program'])
      kgtns_links=dppa.input_list_kegiatan(periode=anggaran_config['periode'],\
                  sub_skpd=f'[{p["kode_sub_skpd"]}] {p["nama_sub_skpd"]}',\
                  bidang_urusan=f'[{p["kode_bidang_urusan"]}] {p["nama_bidang_urusan"]}',\
                  program=f'[{p["kode_program"]}] {p["nama_program"]}' )
      
      if kgtns_links!=None:
         kegiatan_fix=filter_kgtn(kgtns,kgtns_links)
         for k in kegiatan_fix:
               dppa.input_pilih_kegiatan(k)
               subgiats=findSubkegiatan(conn,k['kode_skpd'],k['kode_sub_skpd'],k['kode_bidang_urusan'],k['kode_program'],k['kode_giat'])
               subgiats_links=dppa.input_list_sub_kegiatan(k)
               for s,sl in zip(subgiats,subgiats_links):
                  dppa.input_pilih_sub_kegiatan(s)
                  rincians=findRekeningAkun(conn,s['kode_skpd'],s['kode_sub_skpd'],s['kode_bidang_urusan'],s['kode_program'],s['kode_giat'],s['kode_sub_giat'])
                  rincians_links=dppa.input_list_rincian(s)
                  links=len(rincians)
                  count=1
                  for r,rl in zip(rincians,rincians_links):
                     dppa.input_edit_rincian(r,rl)
                     if(count==links):
                        dppa.back()
                        dppa.switchToDefault()
                     count+=1
          
      else:
         dppa.switchToDefault()
         
   dppa.quit_driver()
   conn.close()

def filter_kgtn(kgtns,kgtn_links):
   links={kl['idKgtn'] for kl in kgtn_links}
   kgtns_fix=[k for k in kgtns if k['kode_giat'] in links]
   return kgtns_fix

def filter_sub_kgtn(sub,sub_links):
   pass
