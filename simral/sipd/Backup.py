import sqlite3
import json
import  os


            

conn = sqlite3.connect("sipd_backup.db")


def init_data():
        
    c=conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS skpd
        (id_skpd INTEGER PRIMARY KEY, kode_skpd VARCHAR(50), nama_skpd VARCHAR(250) )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS subkegiatan
        (kode_program VARCHAR(50),nama_program VARCHAR(200), id_skpd INTEGER,
        kode_skpd VARCHAR(50), nama_skpd VARCHAR(250),
        kode_sub_skpd VARCHAR(50), nama_sub_skpd VARCHAR(200),
        kode_bidang_urusan VARCHAR(10), nama_bidang_urusan VARCHAR(200),
        kode_giat VARCHAR(100), nama_giat VARCHAR(250),
        kode_sub_giat VARCHAR(100), nama_sub_giat VARCHAR(250)
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS rincian
        (kode_akun VARCHAR(50), nama_akun VARCHAR(100), 
        kode_sub_giat VARCHAR(100), nama_sub_giat VARCHAR(250),
        kode_program VARCHAR(50),nama_program VARCHAR(200), id_skpd INTEGER,
        kode_skpd VARCHAR(50), nama_skpd VARCHAR(250),
        kode_sub_skpd VARCHAR(50), nama_sub_skpd VARCHAR(200),
        kode_bidang_urusan VARCHAR(10), nama_bidang_urusan VARCHAR(200),
        kode_giat VARCHAR(100), nama_giat VARCHAR(250),
        total_rincian FLOAT)
    """)

    conn.commit()

def writeSkpdFromFile(filename):
    f=open(filename,"r")
    json_data=json.load(f)
    c=conn.cursor()
    for data in json_data:
        c.execute(" INSERT INTO skpd(id_skpd,kode_skpd,nama_skpd) VALUES(?,?,?)",(data['id_skpd'],data['kode_skpd'],data['nama_skpd']))
        conn.commit()
    f.close()

def writeProgramFromFile(filename):
    f=open(filename,"r")
    json_data=json.load(f)
    c=conn.cursor()
    for data in json_data:
        c.execute("INSERT INTO subkegiatan(kode_program, nama_program, id_skpd, kode_skpd, nama_skpd, kode_sub_skpd, nama_sub_skpd, kode_bidang_urusan, nama_bidang_urusan,kode_giat, nama_giat, kode_sub_giat, nama_sub_giat)VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",(data['kode_program'],data['nama_program'],data['id_skpd'],data['kode_skpd'],data['nama_skpd'], 
        data['kode_sub_skpd'],data['nama_sub_skpd'],data['kode_bidang_urusan'], data['nama_bidang_urusan'],data['kode_giat'],data['nama_giat'],data['kode_sub_giat'],data['nama_giat']))
        conn.commit()
    f.close()

def writeRincianFromFile(filename):
    f=open(filename,"r")
    json_data=json.load(f)
    c=conn.cursor()
    for data in json_data:
        rincian_objek=data['rincian_objek']
        rincian=[]
        for rek in rincian_objek:
            
            c.execute("""
                INSERT INTO rincian(kode_akun, nama_akun, 
                kode_sub_giat, nama_sub_giat,
                kode_program,nama_program ,id_skpd,
                kode_skpd, nama_skpd,
                kode_sub_skpd,nama_sub_skpd,
                kode_bidang_urusan, nama_bidang_urusan,
                kode_giat, nama_giat,
                total_rincian) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,(rek['kode_akun'],rek['nama_akun'],data['kode_sub_giat'],data['nama_sub_giat'],
                data['kode_program'],data['nama_program'],data['id_skpd'],
                data['kode_skpd'],data['nama_skpd'],
                data['kode_sub_skpd'],data['nama_sub_skpd'],
                data['nama_bidang_urusan'],data['kode_bidang_urusan'],   
                data['kode_giat'], data['nama_giat'],rek['total_rincian']))
        conn.commit()
    f.close()

# init_data()
# writeSkpdFromFile(r'dpa.json')

# for files in os.walk('referensi'):
#     for file_name in files:
#         if(file_name and file_name!='referensi'):
#            for f in file_name:
#                 writeProgramFromFile(f'referensi/{f}')
#                 writeRincianFromFile(f'referensi/{f}')
c=conn.cursor()
# writeProgramFromFile(r'referensi/BADAN PENGELOLAAN KEUANGAN DAN ASET DAERAH.json')
# writeRincianFromFile(r'referensi/BADAN PENGELOLAAN KEUANGAN DAN ASET DAERAH.json')
# c=conn.cursor()
id_skpd=96


def findAllSkpd(conn):
    c=conn.cursor()
    c.execute("SELECT * FROM skpd")
    result=c.fetchall()
    data=[]
    if result:
        for col in result:
            data.append({"id_skpd":col[0], "kode_skpd":col[1],"nama_skpd":col[2]})
        return data
    else:
        return

def findSkpdById(conn,id_skpd):
    c=conn.cursor()
    c.execute("SELECT id_skpd,kode_skpd,nama_skpd FROM skpd WHERE id_skpd=:id_skpd",{"id_skpd":id_skpd})
    result=c.fetchone()
    if result:
        return ({"id_skpd":result[0],"kode_skpd":result[1],"nama_skpd":result[2]})
    else:
        return None

def findKegiatanByProgram(conn,id_skpd, nama_progam):
    c=conn.cursor()
    c.execute("SELECT DISTINCT kode_program, nama_program,nama_skpd,nama_bidang_urusan,nama_sub_skpd,kode_giat, nama_giat FROM subkegiatan WHERE id_skpd=:id_skpd AND nama_program=:nama_program",{'id_skpd':id_skpd,"nama_program":nama_progam})
    result=c.fetchall()
    data=[]
    for col in result:
        data.append({"kode_program":col[0],"nama_program":col[1],"nama_skpd":col[2],"nama_bidang_urusan":col[3],"nama_sub_skpd":col[4],"kode_giat":col[5],"nama_giat":col[6]})
    return data;

def findProgramFromIdSkpd(conn,id_skpd):
    c=conn.cursor()
    c.execute("SELECT DISTINCT kode_program, nama_program, kode_skpd, nama_skpd, kode_bidang_urusan, nama_bidang_urusan, kode_sub_skpd, nama_sub_skpd FROM subkegiatan WHERE id_skpd=:id_skpd",{'id_skpd':id_skpd})
    result=c.fetchall()
    data=[]
    for col in result:
        if col[3]!=col[7]:
            data.append({"kode_program":col[0],"nama_program":col[1], "kode_skpd":col[2], "nama_skpd":col[3], "kode_bidang_urusan":col[4], "nama_bidang_urusan":col[5], "kode_sub_skpd":col[6],"nama_sub_skpd":col[7]})
    return data

def findKegiatan(conn, kode_skpd, kode_sub_skpd, kode_bidang_urusan, kode_program):
    c=conn.cursor()
    c.execute("SELECT DISTINCT kode_giat, nama_giat, kode_program, nama_program, kode_bidang_urusan, nama_bidang_urusan, kode_skpd, nama_skpd, kode_sub_skpd, nama_sub_skpd from subkegiatan WHERE kode_skpd=:kode_skpd AND kode_sub_skpd=:kode_sub_skpd AND kode_bidang_urusan=:kode_bidang_urusan AND kode_program=:kode_program",{
        "kode_skpd":kode_skpd,
        "kode_sub_skpd":kode_sub_skpd,
        "kode_bidang_urusan":kode_bidang_urusan,
        "kode_program":kode_program,
    })
    result=c.fetchall()
    if result:
        data=[]
        for col in result:
            data.append({"kode_giat":col[0],"nama_giat":col[1],"kode_program":col[2],"nama_program":col[3],"kode_bidang_urusan":col[4],"nama_bidang_urusan":col[5], "kode_skpd":col[6],"nama_skpd":col[7],"kode_sub_skpd":col[8], "nama_sub_skpd:":col[9]})
        return data
    else:
        return None

def findSubkegiatan(conn, kode_skpd, kode_sub_skpd, kode_bidang_urusan, kode_program, kode_giat):
    c=conn.cursor()
    c.execute("SELECT DISTINCT kode_sub_giat, nama_sub_giat, kode_giat, nama_giat, kode_program, nama_program, kode_bidang_urusan, nama_bidang_urusan, kode_sub_skpd, nama_sub_skpd, kode_skpd, nama_skpd FROM subkegiatan WHERE kode_skpd=:kode_skpd AND kode_sub_skpd=:kode_sub_skpd AND kode_bidang_urusan=:kode_bidang_urusan AND kode_program=:kode_program AND kode_giat=:kode_giat",{
        "kode_skpd":kode_skpd,
        "kode_sub_skpd":kode_sub_skpd,
        "kode_bidang_urusan":kode_bidang_urusan,
        "kode_program":kode_program,
        "kode_giat":kode_giat
    })
    result=c.fetchall()
    data=[]
    for col in result:
        data.append({"kode_sub_giat":col[0],"nama_sub_giat":col[1],"kode_giat":col[2],"nama_giat":col[3], "kode_program":col[4], "nama_program":col[5],"kode_bidang_urusan":col[6],"nama_bidang_urusan":col[7],"kode_sub_skpd":col[8],"nama_sub_skpd":col[9],"kode_skpd":col[10],"nama_skpd":col[11]})
    return data

def findRekeningAkun(conn,kode_skpd,kode_sub_skpd, kode_bidang_urusan, kode_program, kode_giat, kode_sub_giat):
    c=conn.cursor()
    c.execute("SELECT kode_akun, nama_akun, kode_sub_giat, nama_sub_giat, kode_giat, nama_giat, kode_program, nama_program, kode_bidang_urusan, nama_bidang_urusan, kode_skpd, nama_skpd, total_rincian FROM rincian WHERE kode_skpd=:kode_skpd AND kode_sub_skpd=:kode_sub_skpd AND nama_bidang_urusan=:nama_bidang_urusan AND kode_program=:kode_program AND kode_giat=:kode_giat AND kode_sub_giat=:kode_sub_giat",{
        "kode_skpd":kode_skpd,
        "kode_sub_skpd":kode_sub_skpd,
        "nama_bidang_urusan":kode_bidang_urusan,
        "kode_program":kode_program,
        "kode_giat":kode_giat,
        "kode_sub_giat":kode_sub_giat
    })
    result=c.fetchall()
    data=[]
    for col in result:
        
        data.append({"kode_akun":col[0],"nama_akun":col[1], "kode_sub_giat":col[2],"nama_sub_giat":col[3],"kode_giat":col[4],"nama_giat":col[5], "kode_program":col[6], "nama_program":col[7],"kode_bidang_urusan":col[8],"nama_bidang_urusan":col[9],"kode_skpd":col[10],"nama_skpd":col[11],"total_rincian":col[12]})
    return data

def findSingleRekeningAkun(conn,kode_skpd,kode_sub_skpd, kode_bidang_urusan, kode_program, kode_giat, kode_sub_giat,kode_akun):
    c=conn.cursor()
    c.execute("SELECT kode_akun, nama_akun, kode_sub_giat, nama_sub_giat, kode_giat, nama_giat, kode_program, nama_program, kode_bidang_urusan, nama_bidang_urusan, kode_skpd, nama_skpd, total_rincian FROM rincian WHERE kode_skpd=:kode_skpd AND kode_sub_skpd=:kode_sub_skpd AND nama_bidang_urusan=:nama_bidang_urusan AND kode_program=:kode_program AND kode_giat=:kode_giat AND kode_sub_giat=:kode_sub_giat AND kode_akun=:kode_akun",{
        "kode_skpd":kode_skpd,
        "kode_sub_skpd":kode_sub_skpd,
        "nama_bidang_urusan":kode_bidang_urusan,
        "kode_program":kode_program,
        "kode_giat":kode_giat,
        "kode_sub_giat":kode_sub_giat,
        "kode_akun":kode_akun
    })
    col=c.fetchone()
    if col:
        return {"kode_akun":col[0],"nama_akun":col[1], "kode_sub_giat":col[2],"nama_sub_giat":col[3],"kode_giat":col[4],"nama_giat":col[5], "kode_program":col[6], "nama_program":col[7],"kode_bidang_urusan":col[8],"nama_bidang_urusan":col[9],"kode_skpd":col[10],"nama_skpd":col[11],"total_rincian":col[12]}
    return None


kegiatan=findKegiatan(conn,"5.02.0.00.0.00.01.0000","5.02.0.00.0.00.01.0004","5.02","5.02.02")

result=findRekeningAkun(conn,"5.02.0.00.0.00.01.0000","5.02.0.00.0.00.01.0004","5.02","5.02.02","5.02.02.2.05","5.02.02.2.05.02")
single=findSingleRekeningAkun(conn,"5.02.0.00.0.00.01.0000","5.02.0.00.0.00.01.0004","5.02","5.02.02","5.02.02.2.05","5.02.02.2.05.02","5.1.02.02.02.0005")
print(kegiatan)
print(single)

c.close()
conn.close()