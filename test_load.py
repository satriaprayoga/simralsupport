from SipdHelper import SipdConnection
import  sqlite3
from SipdHelper import  SipdConnection

con=sqlite3.connect("data/sipd.sqlite")
con.execute("""
CREATE TABLE IF NOT EXISTS skpd(
        idSkpd INT NOT NULL PRIMARY KEY,
        namaSkpd VARCHAR(1000),
        kodeSkpd VARCHAR(100)
    )
""")
print("create table successfully")


con.close()