from simral.data.migration import Migration
from simral.sipd.SipdHelper import SipdConnection

import logging

logging.basicConfig(level=logging.INFO)



sc=SipdConnection(1)
sc.initConnection()
sc.authenticate(payload={
    '_token':sc.cookie['csrf-token'],
    'userName':'adm.keuangan_11_0',
    'password':'belanja',
    'tahunanggaran':2021,
    'idDaerah':11,
    'namaDaerah':'Kab. Bogor'
})


skpd=sc.getAllSkpd()

mig=Migration()
mig.createTableSkpd()
mig.createTableDpa()
mig.createTableDpaRinci()
mig.populateSkpdTable(skpd)
single=mig.findAllSkpd()
print(len(single))

dpa=sc.getRekapDpaBelanja()
mig.populateDpa(dpa)
dpa=mig.findAllDpa()
for d in dpa:
    rinci=sc.getDpaBelanja(d[2])
    mig.populateDpaRinci(rinci,d[2])
rinc=mig.findDpaRinci(1423)
print(rinc)
mig.close()