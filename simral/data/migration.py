import sqlite3
from sqlite3 import Error

import logging


CREATE_DB='CREATE DATABASE IF NOT EXISTS '
DEFAULT_DB_NAME='sipd_ref.db'


SKPD_CREATE_QUERY= """
    CREATE TABLE IF NOT EXISTS skpd(
        idSkpd INT NOT NULL PRIMARY KEY,
        namaSkpd VARCHAR(1000),
        kodeSkpd VARCHAR(100)
    )
"""
INSERT_SKPD_QUERY="""
    INSERT INTO skpd VALUES (?,?,?)
"""
DPA_BELANJA_CREATE_QUERY="""
    CREATE TABLE IF NOT EXISTS dpa_belanja(
        id_dpa INTEGER PRIMARY KEY,
        id_unit INTEGER,
        id_skpd INTEGER,
        kode_skpd VARCHAR(100),
        nama_skpd VARCHAR(1000),
        rincian_murni FLOAT,
        rincian FLOAT

    )
"""
INSERT_DPA_SKPD_QUERY="""
    INSERT INTO dpa_belanja VALUES(NULL,?,?,?,?,?,?)
"""

DPA_BELANJA_RINCI_CREATE_QUERY="""
    CREATE TABLE IF NOT EXISTS dpa_belanja_rinci(
        id_dpa_rinci INT PRIMARY KEY,
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
        rincian_murni FLOAT
    )
"""

INSERT_DPA_BELANJA_RINCI_QUERY="""
    INSERT INTO dpa_belanja_rinci VALUES(NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
"""

BIDANG_URUSAN_CREATE_QUERY="""
    CREATE TABLE IF NOT EXISTS bidang_urusan(
        id_bidang_urusan INT NOT NULL,
        nama_bidang_urusan VARCHAR(1000) NOT NULL,
        kode_bidang_urusan VARCHAR(32) NOT NULL,
        PRIMARY KEY(id_bidang_urusan)
    )
"""

class Migration:

    def __init__(self):
        try:
            logging.info("Memulai koneksi ke SQLite Database: {}".format(DEFAULT_DB_NAME))
            connection=sqlite3.connect(DEFAULT_DB_NAME)
            logging.info("Tersambung dengan SQLite Database: {}!".format(DEFAULT_DB_NAME))
            self.connection=connection
        except Error as err:
            logging.error(err)
            self.connection=None

    def close(self):
        logging.info("Menutup koneksi SQLite")
        self.connection.close()
          

    def createTableSkpd(self):
        try:
            cursor=self.connection.cursor()
            cursor.execute(SKPD_CREATE_QUERY)
            self.connection.commit()
        except Error as err:
            logging.error(err)
            self.connection.rollback()

    def findAllSkpd(self):
        try:
            cursor=self.connection.cursor()
            cursor.execute("SELECT * FROM skpd")
            return cursor.fetchall()
        except Error as err:
            logging.error(err)
            self.connection.rollback()

    def findSingleSkpd(self,idSkpd):
        try:
            cursor=self.connection.cursor()
            cursor.execute("SELECT * FROM skpd where idSkpd=:idSkpd",{"idSkpd":idSkpd})
            return cursor.fetchone()
        except Error as err:
            logging.error(err)
            self.connection.rollback()

    def findDpaForSkpd(self,idSkpd):
        try:
            cursor=self.connection.cursor()
            cursor.execute("SELECT id_dpa,id_unit,id_skpd,kode_skpd,nama_skpd FROM dpa_belanja WHERE id_skpd=:id_skpd",{"id_skpd":idSkpd})
            
            return cursor.fetchone() # return None for empty result
        except Error as err:
            logging.error(err)
            self.connection.rollback()

    def findAllDpa(self):
        try:
            cursor=self.connection.cursor()
            cursor.execute("SELECT * FROM dpa_belanja")
            
            return cursor.fetchall() # return None for empty result
        except Error as err:
            logging.error(err)
            self.connection.rollback()
    
    def populateSkpdTable(self,jsonData):
        try:
            records=[]
            for item in jsonData:
                id=item['idSkpd']
                namaSkpd=item['namaSkpd']
                kode=item['kodeSkpd']
                if(item['kodeSkpd'].endswith('.00')):
                    kode=kode+'00'
                records.append((id,namaSkpd,kode))
            print(records)
            cursor=self.connection.cursor()
            cursor.executemany(INSERT_SKPD_QUERY,records)
            self.connection.commit()
        except Error as err:
            logging.error(err)
            self.connection.rollback()

    def createTableDpa(self):
        try:
            cursor=self.connection.cursor()
            cursor.execute(DPA_BELANJA_CREATE_QUERY)
            self.connection.commit()
        except Error as err:
            logging.error(err)
            self.connection.rollback()

    def createTableDpaRinci(self):
         try:
            cursor=self.connection.cursor()
            cursor.execute(DPA_BELANJA_RINCI_CREATE_QUERY)
            self.connection.commit()
         except Error as err:
            logging.error(err)
            self.connection.rollback()


    def createTableBidangUrusan(self):
         try:
            cursor=self.connection.cursor()
            cursor.execute(BIDANG_URUSAN_CREATE_QUERY)
            self.connection.commit()
         except Error as err:
            logging.error(err)
            self.connection.rollback()

        

    def populateDpa(self,jsonData):
        try:
            records=[]
            for item in jsonData:
                kode=item['kode_skpd']
                if(kode.endswith('.00')):
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
            logging.error(err)
            self.connection.rollback()

    def populateDpaRinci(self,jsonData,idSkpd):
        try:
            records=[]
            dpaSkpd=self.findDpaForSkpd(idSkpd) #SELECT id_dpa,id_unit,id_skpd,kode_skpd,nama_skpd FROM dpa_belanja WHERE id_skpd=?
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
            logging.error(err)
            self.connection.rollback()

    def findDpaRinci(self,idSkpd):
        try:
            cursor=self.connection.cursor()
            cursor.execute("SELECT * FROM dpa_belanja_rinci WHERE id_skpd=:id_skpd",{"id_skpd":idSkpd})
            return cursor.fetchall()
        except Error as err:
            logging.error(err)
            self.connection.rollback()
