from SipdHelper import SipdConnection

import logging
import json
import time

logging.basicConfig(level=logging.INFO)

def downloadSkpd(sc):
    logging.info('download data skpd')
    skpdList=sc.getAllSkpd()
    json_data=[]
    for item in skpdList:
        id=item['idSkpd']
        namaSkpd=item['namaSkpd'].replace(item['kodeSkpd'],"").strip()
        kode=item['kodeSkpd']
        if(item['kodeSkpd'].endswith('.00')):
            kode=kode+'00'
        data={"idSkpd":id,"namaSkpd":namaSkpd,'kodeSkpd':kode}
        json_data.append(data)

    json_obj=json.dumps(json_data,indent=4,sort_keys='idSkpd')
    f=open("skpd.json","w")
    f.write(json_obj)
    f.close()

def downloadRekapDpa(sc):
    logging.info('download rekap dpa skpd')
    skpdList=sc.getRekapDpaBelanja()
    json_data=[]
    for item in skpdList:
        id=item['id_skpd']
        namaSkpd=item['nama_skpd'].replace(item['kode_skpd'],"").strip()
        kode=item['kode_skpd']
        rincian_murni=item['rincian_murni']
        rincian=item['rincian']
        if(item['kode_skpd'].endswith('.00')):
            kode=kode+'00'
        data={"id_skpd":id,"nama_skpd":namaSkpd,'kode_skpd':kode,'rincian_murni':rincian_murni,'rincian':rincian}
        json_data.append(data)

    json_obj=json.dumps(json_data,indent=4,sort_keys='id_skpd')
    f=open("referensi/dpa.json","w")
    f.write(json_obj)
    f.close()

def downloadDpaSubGiat(sc,id_skpd,kode_skpd,nama_skpd):
    subgiatList=sc.getDpaBelanja(id_skpd)
    json_data=[]     
    for item in subgiatList:
        id_sub_giat=item['id_sub_giat']
        kode_bl=item['kode_bl'] if(item['kode_bl']) else ""
        logging.info("mengunduh: {} {} {} {} ".format(item['nama_sub_skpd'],item['nama_program'],item['nama_giat'],item['nama_sub_giat']))
        if id_sub_giat:
            logging.info("mengunduh rincian: {}.{}.{}".format(id_skpd,kode_bl,id_sub_giat))
            rekObjectList=sc.getRkaBelanjaKodeBl(id_skpd,item['kode_bl'],item['id_sub_giat']) if item['kode_bl'] else sc.getRkaBelanja(item['id_skpd'],item['id_sub_skpd'],item['id_bidang_urusan'],item['id_program'],item['id_giat'],item['id_sub_giat'])
            rincian_objek=[]
            for obj in rekObjectList:
                rincian_objek.append({
                    'kode_akun':obj['kode_akun'],
                    'nama_akun':obj['nama_akun'].replace(obj['kode_akun'],"").strip(),
                    'total_rincian':obj['total_rincian']})

        
        json_data.append({
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
        'rincian_objek':rincian_objek
        })
    
    json_obj=json.dumps(json_data,indent=2,sort_keys='id_skpd')
    filename="referensi/{}.json".format(nama_skpd)
    f=open(filename,"w")
    f.write(json_obj)
    f.close()

f=open('referensi/dpa_test.json','r')
skpd=json.load(f)

#sc=SipdConnection(20)
#sc.initConnection()

#sc.authenticate(payload)
sc=SipdConnection(30)
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
    downloadDpaSubGiat(sc,s['id_skpd'],s['kode_skpd'],s['nama_skpd'])
    end=time.perf_counter()
    logging.info("Finished download data:{}".format(s['nama_skpd']))
    time.sleep(2)
    print(f"Execution Time : {end - start:0.6f} seconds" )
f.close()