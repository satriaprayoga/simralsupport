from SipdHelper import SipdConnection

import logging
import json
import time
import csv

logging.basicConfig(level=logging.INFO)

def downloadRkaSubGiat(sc,id_skpd,kode_skpd,nama_skpd):
    subgiatList=sc.getDpaBelanja(id_skpd)
    json_data=[]     
    for item in subgiatList:
        id_sub_giat=item['id_sub_giat']
        kode_bl=item['kode_bl'] if(item['kode_bl']) else ""
        logging.info("mengunduh: {} {} {} {} ".format(item['nama_sub_skpd'],item['nama_program'],item['nama_giat'],item['nama_sub_giat']))
        if id_sub_giat:
            logging.info("mengunduh rincian: {}.{}.{}".format(id_skpd,kode_bl,id_sub_giat))
            rekObjectList=sc.getRkaBelanjaKodeBl(id_skpd,item['kode_bl'],item['id_sub_giat']) if item['kode_bl'] else sc.getRkaBelanja(item['id_skpd'],item['id_sub_skpd'],item['id_bidang_urusan'],item['id_program'],item['id_giat'],item['id_sub_giat'])
            for obj in rekObjectList:
                
                json_data.append({
                "bulan_1":obj['bulan_1'],
                "bulan_2":obj['bulan_2'],
                "bulan_3":obj['bulan_3'],
                "bulan_4":obj['bulan_4'],
                "bulan_5":obj['bulan_5'],
                "bulan_6":obj['bulan_6'],
                "bulan_7":obj['bulan_7'],
                "bulan_8":obj['bulan_8'],
                "bulan_9":obj['bulan_9'],
                "bulan_10":obj['bulan_10'],
                "bulan_11":obj['bulan_11'],
                "bulan_12":obj['bulan_12'],
                "id_skpd":id_skpd,
                "kode_skpd":kode_skpd,
                "nama_skpd":nama_skpd,
                "kode_sub_skpd":item['kode_sub_skpd'] if(item['kode_sub_skpd']) else "",
                "nama_sub_skpd":item['nama_sub_skpd'].replace(item['kode_sub_skpd'],"").strip() if(item['nama_sub_skpd']) else "",
                "kode_bidang_urusan":item['kode_bidang_urusan'] if(item['kode_bidang_urusan']) else "",
                "nama_bidang_urusan":item['nama_bidang_urusan'].replace(item['kode_bidang_urusan'],"").strip(),
                "kode_program":item['kode_program'],
                "nama_program":item['nama_program'].replace(item['kode_program'],"").strip(),
                "kode_giat":item['kode_giat'],
                "nama_giat":item['nama_giat'].replace(item['kode_giat'],"").strip(),
                "kode_bl":kode_bl,
                "id_sub_giat":item['id_sub_giat'],
                "kode_sub_giat":item['kode_sub_giat'],
                "nama_sub_giat":item['nama_sub_giat'].replace(item['kode_sub_giat'],"").strip(),
                "rincian":item['rincian'],
                "rincian_murni":item['rincian_murni'],
                'kode_akun':obj['kode_akun'],
                'nama_akun':obj['nama_akun'].replace(obj['kode_akun'],"").strip(),
                'total_rincian':obj['total_rincian'],
                })
    
    json_obj=json.dumps(json_data)
    filename="angkas/{}.json".format(nama_skpd)
    f=open(filename,"w")
    f.write(json_obj)
    f.close()

def saveToCsv(filename,skpd):
    with open(filename) as json_file:
        jsondata = json.load(json_file)
    
    data_file = open(f'angkas/{skpd["nama_skpd"]}.csv', 'w', newline='')
    csv_writer = csv.writer(data_file)
    
    count = 0
    for data in jsondata:
        if count == 0:
            header = data.keys()
            csv_writer.writerow(header)
            count += 1
        csv_writer.writerow(data.values())
    
    data_file.close()

f=open(r'dpa.json','r')
skpd=json.load(f)
sc=SipdConnection(20)
sc.initConnection()
payload={
    '_token':sc.cookie['csrf-token'],
    'userName':'adm.keuangan_11_0',
    'password':'belanja',
    'tahunanggaran':2021,
    'idDaerah':11,
    'namaDaerah':'Kab. Bogor'
}
sc.authenticate(payload)
for s in skpd:
    start=time.perf_counter()
   
    logging.info("Downloading data:{} {} {}".format(s['nama_skpd'],s['kode_skpd'],s['id_skpd']))
    downloadRkaSubGiat(sc,s['id_skpd'],s['kode_skpd'],s['nama_skpd'])
    saveToCsv(f'angkas/{s["nama_skpd"]}.json',s)
    end=time.perf_counter()
    logging.info("Finished download data:{}".format(s['nama_skpd']))
    time.sleep(2)
    print(f"Execution Time : {end - start:0.6f} seconds" )
    time.sleep(3)
f.close()
sc.session.close()