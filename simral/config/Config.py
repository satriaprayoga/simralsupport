#Konfigurasi
class Config:

    __defaultSimralAnggaranUsername="gilang_2021"
    __defaultSimralAnggaranPassword="1234567a"
    __defaultSimralDatabaseCfg="2021"
    __defaultSimralPeriode="PARSIAL 3 (2021-07-13 s/d 2021-09-30)"
    __defaultSimralJenisPerubahan="Perubahan Anggaran Sebelum APBD-P"

    __defaultSimralUsernama="lalapati"
    __defaultSimralPassword="lalapati123"

    

    def __init__(self):
        self.__simralPerubahan={
            "username":self.__defaultSimralAnggaranUsername,
            "password":self.__defaultSimralAnggaranPassword,
            "cfg":self.__defaultSimralDatabaseCfg,
            "periode":self.__defaultSimralPeriode,
            "jenis_perubahan":self.__defaultSimralJenisPerubahan
        }
        self.__simralKasda={
            "username":self.__defaultSimralUsernama,
            "password":self.__defaultSimralPassword,
            "cfg":self.__defaultSimralDatabaseCfg
        }
        self.__simralPendapatan={
            "username":self.__defaultSimralUsernama,
            "password":self.__defaultSimralPassword,
            "cfg":self.__defaultSimralDatabaseCfg
        }

    def get_simral_perubahan_config(self):
        return self.__simralPerubahan

    def get_simral_kasda_config(self):
        return self.__simralKasda
    
    def get_simral_pendapatan_config(self):
        return self.__simralPendapatan
    
    def set_simral_perubahan_config(self,username,password,cfg):
        self.__simralPerubahan["username"]=username
        self.__simralPerubahan["password"]=password
        self.__simralPerubahan["cfg"]=cfg
    
    def set_simral_pendapatan_config(self,username,password,cfg):
        self.__simralPendapatan["username"]=username
        self.__simralPendapatan["password"]=password
        self.__simralPendapatan["cfg"]=cfg
        

    def set_simral_kasda_config(self,username,password,cfg):
        self.__simralKasda["username"]=username
        self.__simralKasda["password"]=password
        self.__simralKasda["cfg"]=cfg
