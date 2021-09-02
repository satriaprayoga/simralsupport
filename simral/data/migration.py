import mysql.connector
from mysql.connector import cursor
from mysql.connector.errors import Error

import logging

CREATE_DB='CREATE DATABASE IF NOT EXISTS '
DEFAULT_DB_NAME='keuangan_db'

MYSQL_HOST='localhost'
MYSQL_USER='root'
MYSQL_PASSWORD='asdqwe123'

SKPD_CREATE_QUERY= """
    CREATE TABLE IF NOT EXISTS skpd(
        idSkpd INT NOT NULL PRIMARY KEY,
        namaSkpd VARCHAR(1000),
        kodeSkpd VARCHAR(100)
    )
"""
INSERT_SKPD_QUERY="""
    INSERT INTO skpd (idSkpd,namaSkpd,kodeSkpd)
    VALUES (%s,%s,%s)
"""
DPA_BELANJA_CREATE_QUERY="""
    CREATE TABLE IF NOT EXISTS dpa_belanja(
        id_dpa INT AUTO_INCREMENT,
        id_unit INT,
        id_skpd INT NOT NULL,
        kode_skpd VARCHAR(100),
        nama_skpd VARCHAR(1000),
        rincian_murni FLOAT,
        rincian FLOAT,
        FOREIGN KEY(id_skpd) REFERENCES skpd(idSkpd),
        PRIMARY KEY(id_dpa)

    )
"""
INSERT_DPA_SKPD_QUERY="""
    INSERT INTO dpa_belanja(id_unit,id_skpd,kode_skpd,nama_skpd,rincian_murni,rincian)
    VALUES(%s,%s,%s,%s,%s,%s)
"""

DPA_BELANJA_RINCI_CREATE_QUERY="""
    CREATE TABLE IF NOT EXISTS dpa_belanja_rinci(
        id_dpa_rinci INT AUTO_INCREMENT,
        id_dpa INT,
        id_unit INT,
        id_skpd INT NOT NULL,
        kode_skpd VARCHAR(100),
        nama_skpd VARCHAR(1000),
        id_sub_skpd INT,
        kode_sub_skpd VARCHAR(150),
        nama_sub_skpd VARCHAR(1000),
        id_urusan INT,
        id_bidang_urusan INT,
        kode_bidang_urusan VARCHAR(32),
        nama_bidang_urusan VARCHAR(1000),
        id_program INT,
        kode_program VARCHAR(50),
        nama_program VARCHAR(1000),
        id_giat INT,
        kode_giat VARCHAR(50),
        nama_giat VARCHAR(1000),
        id_sub_giat INT,
        kode_sub_giat VARCHAR(100),
        nama_sub_giat VARCHAR(1000),
        rincian FLOAT,
        rincian_murni FLOAT,
        PRIMARY KEY(id_dpa_rinci),
        FOREIGN KEY(id_dpa) REFERENCES dpa_belanja(id_dpa)
    )
"""

INSERT_DPA_BELANJA_RINCI_QUERY="""
    INSERT INTO dpa_belanja_rinci(
        id_dpa,
        id_unit,
        id_skpd,
        kode_skpd,
        nama_skpd,
        id_sub_skpd,
        kode_sub_skpd,
        nama_sub_skpd,
        id_urusan,
        id_bidang_urusan,
        kode_bidang_urusan,
        nama_bidang_urusan,
        id_program,
        kode_program,
        nama_program,
        id_giat,
        kode_giat,
        nama_giat,
        id_sub_giat,
        kode_sub_giat,
        nama_sub_giat,
        rincian,
        rincian_murni)
    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""

BIDANG_URUSAN_CREATE_QUERY="""
    CREATE TABLE IF NOT EXISTS bidang_urusan(
        id_bidang_urusan INT NOT NULL,
        nama_bidang_urusan VARCHAR(1000) NOT NULL,
        kode_bidang_urusan VARCHAR(32) NOT NULL,
        PRIMARY KEY(id_bidang_urusan)
    )
"""

CREATE_ANGKAS__QUERY="""
    CREATE TABLE IF NOT EXISTS rka_belanja(
        id_rka INT AUTO_INCREMENT,
        id_dpa_rinci INT,
        id_sub_giat INT,
        kode_sub_giat VARCHAR(100),
        nama_sub_giat VARCHAR(1000),
        kode_akun VARCHAR(100),
        nama_akun VARCHAR(100),
        kelompok_akun VARCHAR(10),
        jenis_akun VARCHAR(25),
        objek_akun VARCHAR(25),
        rinci_objek_akun VARCHAR(50),
        total_rincian FLOAT,
        PRIMARY KEY(id_rka),
        FOREIGN KEY(id_dpa_rinci) REFERENCES dpa_belanja_rinci(id_dpa_rinci)
    )
"""

AKUN_LRA_QUERY="""
     CREATE TABLE IF NOT EXISTS akun_lra(
        id_akun INT AUTO_INCREMENT PRIMARY KEY,
        kode_akun VARCHAR(1000),
        nama_akun VARCHAR(100)
    )
"""

INSERT_LRA_QUERY="""
    INSERT INTO akun_lra VALUES(%s,%s)
"""

class Migration:

    def __init__(self):
        try:
            logging.info("Memulai koneksi ke MySQL Server: {}@{}".format(MYSQL_USER,MYSQL_HOST))
            connection=mysql.connector.connect(
            host=MYSQL_HOST,
            username=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=DEFAULT_DB_NAME
        )
            logging.info("Tersambung dengan MySQL Server: {}@{}!".format(MYSQL_USER,MYSQL_HOST))
            self.connection=connection
        except mysql.connector.Error as err:
            logging.error(err)
            logging.info("Gagal Tersambung dengan MySQL Server @ {}".format(MYSQL_HOST))
            self.connection=None

    def close(self):
        if(self.connection.is_connected()):
            logging.info("Menutup koneksi MySQL")
            self.connection.close()

    def createTableSkpd(self):
        try:
            self.connection.autocommit=False
            cursor=self.connection.cursor()
            cursor.execute(SKPD_CREATE_QUERY)
            self.connection.commit()
        except Error as err:
            logging.error("Terjadi kesalahan: {}".format(err))
            self.connection.rollback()

    def findSingleSkpd(self,idSkpd):
        try:
            cursor=self.connection.cursor()
            cursor.execute("SELECT  FROM skpd where idSkpd=%s",(idSkpd,))
            return cursor.fetchone()
        except Error as err:
            logging.error("Terjadi kesalahan: {}".format(err))
            self.connection.rollback()

    def findDpaForSkpd(self,idSkpd):
        try:
            cursor=self.connection.cursor()
            cursor.execute("SELECT id_dpa,id_unit,id_skpd,kode_skpd,nama_skpd FROM dpa_belanja WHERE id_skpd=%s",(idSkpd,))
            
            return cursor.fetchone() # return None for empty result
        except Error as err:
            logging.error("Terjadi kesalahan: {}".format(err))
            self.connection.rollback()
    
    def populateSkpdTable(self,jsonData):
        try:
            self.connection.autocommit=False
            records=[]
            for item in jsonData:
                id=item['idSkpd']
                namaSkpd=item['namaSkpd']
                kode=item['kodeSkpd']
                if(item['kodeSkpd'].endswith('.00')):
                    kode=kode+'00'
                records.append((id,namaSkpd,kode))
            cursor=self.connection.cursor()
            cursor.executemany(INSERT_SKPD_QUERY,records)
            self.connection.commit()
        except Error as err:
            logging.error("Terjadi kesalahan: {}".format(err))
            self.connection.rollback()

    def createTableDpa(self):
        try:
            self.connection.autocommit=False
            cursor=self.connection.cursor()
            cursor.execute(DPA_BELANJA_CREATE_QUERY)
            self.connection.commit()
        except Error as err:
            logging.error("Terjadi kesalahan: {}".format(err))
            self.connection.rollback()

    def createTableDpaRinci(self):
         try:
            self.connection.autocommit=False
            cursor=self.connection.cursor()
            cursor.execute(DPA_BELANJA_RINCI_CREATE_QUERY)
            self.connection.commit()
         except Error as err:
            logging.error("Terjadi kesalahan: {}".format(err))
            self.connection.rollback()


    def createTableBidangUrusan(self):
         try:
            self.connection.autocommit=False
            cursor=self.connection.cursor()
            cursor.execute(BIDANG_URUSAN_CREATE_QUERY)
            self.connection.commit()
         except Error as err:
            logging.error("Terjadi kesalahan: {}".format(err))
            self.connection.rollback()

        

    def populateDpa(self,jsonData):
        try:
            self.connection.autocommit=False
            records=[]
            for item in jsonData:
                kode=item['kode_skpd']
                if(item['kode_skpd'].endswith('.00')):
                    kode=kode+'00'
                records.append((
                    item['id_unit'],
                    item['id_skpd'],
                    kode,
                    item['nama_skpd'].replace(item['kode_skpd'],"").strip(),
                    item['rincian_murni'],
                    item['rincian']
                ))             
            cursor=self.connection.cursor()
            cursor.executemany(INSERT_DPA_SKPD_QUERY,records)
            self.connection.commit()
        except Error as err:
            logging.error("Terjadi kesalahan: {}".format(err))
            self.connection.rollback()

    def populateDpaRinci(self,jsonData,idSkpd):
        try:
            self.connection.autocommit=False
            records=[]
            dpaSkpd=self.findDpaForSkpd(idSkpd) #SELECT id_dpa,id_unit,id_skpd,kode_skpd,nama_skpd FROM dpa_belanja WHERE id_skpd=%s
            for item in jsonData:
                records.append((
                    dpaSkpd[0],
                    dpaSkpd[1],
                    dpaSkpd[2],
                    dpaSkpd[3],
                    dpaSkpd[4],
                    item['id_sub_skpd'],
                    item['kode_sub_skpd'],
                    item['nama_sub_skpd'],
                    item['id_urusan'],
                    item['id_bidang_urusan'],
                    item['kode_bidang_urusan'],
                    item['nama_bidang_urusan'].replace(item['kode_bidang_urusan'],"").strip(),
                    item['id_program'],
                    item['kode_program'],
                    item['nama_program'].replace(item['kode_program'],"").strip(),
                    item['id_giat'],
                    item['kode_giat'],
                    item['nama_giat'].replace(item['kode_giat'],"").strip(),
                    item['id_sub_giat'],
                    item['kode_sub_giat'],
                    item['nama_sub_giat'].replace(item['kode_sub_giat'],"").strip(),
                    item['rincian'],
                    item['rincian_murni']
                ))
            cursor=self.connection.cursor()
            cursor.executemany(INSERT_DPA_BELANJA_RINCI_QUERY,records)
            self.connection.commit()
            return records
        except Error as err:
            logging.error("Terjadi kesalahan: {}".format(err))
            self.connection.rollback()

    def createAkunTable(self):
        try:
            self.connection.autocommit=False
            cursor=self.connection.cursor()
            cursor.execute(AKUN_LRA_QUERY)
            self.connection.commit()
        except Error as err:
            logging.error("Terjadi kesalahan: {}".format(err))
            self.connection.rollback()

    def findAkun(self,id_akun):
        try:
            cursor=self.connection.cursor()
            cursor.execute("SELECT id_akun, kode_akun, nama_akun, level FROM akun_lra where kode_akun=%s",(id_akun,))
            return cursor.fetchone()
        except Error as err:
            logging.error("Terjadi kesalahan: {}".format(err))
            self.connection.rollback()
    
    def createRkaTable(self):
        try:
            self.connection.autocommit=False
            cursor=self.connection.cursor()
            cursor.execute(CREATE_ANGKAS__QUERY)
            self.connection.commit()
        except Error as err:
            logging.error("Terjadi kesalahan: {}".format(err))
            self.connection.rollback()

    def findDpaRinci(self):
        try:
            cursor=self.connection.cursor()
            cursor.execute("SELECT id_skpd,id_sub_skpd,id_bidang_urusan,id_program,id_giat,id_sub_giat,kode_sub_giat,nama_sub_giat,id_dpa_rinci FROM keuangan_db.dpa_belanja_rinci ")
            return cursor.fetchone()
        except Error as err:
            logging.error("Terjadi kesalahan: {}".format(err))
            self.connection.rollback()
    
    def populateRka(self,id_skpd,id_sub_skpd,id_bidang_urusan,id_program,id_giat,id_sub_giat):
        pass