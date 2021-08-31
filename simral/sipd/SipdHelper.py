import json
import  requests
from bs4 import BeautifulSoup

SIPD_URL="https://sipd.kemendagri.go.id/siap/"

class SipdConnection:

    def __init__(self, timeout=0.05):
        self.timeout = timeout

    def initConnection(self):
        response = requests.get(
            SIPD_URL, timeout=self.timeout)
        headers = response.headers  # get headers part -> Dictionary
        setCookie = headers['Set-Cookie']  # get set-cookie header part -> String
        cookieDecons = setCookie.split(';')  # split to List
        self.cookie = {}
        for c in cookieDecons:
            if(c.find('=') != -1):
                key = c.split('=')[0]
                value = c.split('=')[1]
                self.cookie[key] = value
            else:
                self.cookie[key] = c
                self.cookie[value] = ''
        soup = BeautifulSoup(response.content, "html.parser")
        csrfTokenTag = soup.head.find('meta', attrs={'name': 'csrf-token'})
        self.cookie['csrf-token'] = csrfTokenTag.get('content')
        #return self.cookie

    
    def authenticate(self,payload):
       if not hasattr(self,'cookie'):
           print('connection has not been established')
           return False
       response=requests.post(SIPD_URL+'login',data=payload)
       #print(response.status_code)
       #print(response.headers)
       #print(response.cookies.get_dict())
       #print(self.cookie['siap_session'])
       # Update Cookie for siap_session
       self.cookie['siap_session']=response.cookies.get_dict()['siap_session']
       #print(self.cookie['siap_session'])
       return True

    def getAllSkpd(self,saveToFile=False,filename='skpd.json'):
        if not hasattr(self,'cookie'):
           print('connection has not been established')
           return
        response=requests.get(SIPD_URL+'data/skpd/all',cookies={'siap_session':self.cookie['siap_session']})
        if(saveToFile==True):
           json_obj=json.dumps(response.json(),indent=4,sort_keys='idSkpd')
           with open(filename,"w") as outfile:
               outfile.write(json_obj)
        return response.json()

    def getRekapDpaBelanja(self):
        if not hasattr(self,'cookie'):
           print('connection has not been established')
           return
        response=requests.get(SIPD_URL+'dpa-bl/tampil-unit/daerah/main/budget/2021/11/0',cookies={'siap_session':self.cookie['siap_session']})
        return response.json()['data']

    def getDpaBelanja(self,idSkpd,saveToFile=False,filename='dpa.json'):
        if not hasattr(self,'cookie'):
           print('connection has not been established')
           return
        response=requests.get(SIPD_URL+"dpa-bl-rinci/tampil-giat/daerah/main/budget/2021/11/{}".format(idSkpd),cookies={'siap_session':self.cookie['siap_session']})
        data=response.json()['data']
        if(saveToFile==True):
           json_obj=json.dumps(data,indent=4,sort_keys='data')
           with open(filename,"w") as outfile:
               outfile.write(json_obj)
        return data

    def getRkaBelanja(self,idSkpd,idSubSkpd,idBidangUrusan,idProgram,idGiat,idSubGiat):
        if not hasattr(self,'cookie'):
           print('connection has not been established')
           return
        params="{}.{}.{}.{}.{}.{}.{}".format(idSkpd,idSkpd,idSubSkpd,idBidangUrusan,idProgram,idGiat,idSubGiat)
        rkaUrl=SIPD_URL+'rak-belanja/tampil-rincian/daerah/main/budget/2021/11/{}'.format(idSkpd)
        response=requests.get(rkaUrl,cookies={'siap_session':self.cookie['siap_session']},params={'kodesbl': params})
        rdata=response.json()
        return rdata['data']

    def extractBidangUrusan(self,dpaJson):
        records=[]
        for item in dpaJson:
            records.append(
                (
                    {'id_bidang_urusan':item['id_bidang_urusan'],
                    'id_urusan':item['id_urusan'],
                    'kode_bidang_urusan':item['kode_bidang_urusan'],
                    'nama_bidang_urusan':item['nama_bidang_urusan']}
                ))
        return records
