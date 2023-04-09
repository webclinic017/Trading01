import json
import os
import socket


class ConfigDbSing:
    __instance = None
    connect_db = None
    path_json = r'Trade\config_db.json'

    def __init__(self):
        print("!!!!!!!!!!  ConfigDbSing ")
        name_comp = (socket.gethostname()).lower()
        if name_comp == 'p1':
            pref_comp = "E:\\"
        else:
            pref_comp = "E:\MLserver\\"

        ConfigDbSing.path_json = pref_comp + ConfigDbSing.path_json

        if ConfigDbSing.connect_db is None:
            print("--------------  ConfigDbSing ")
            if not os.path.exists(ConfigDbSing.path_json):
                ConfigDbSing.set_config(self)

            with open(ConfigDbSing.path_json, 'r') as j:
                print(" Читаем данные из файла")
                ConfigDbSing.connect_db = json.load(j)
#                print(ConfigDbSing.connect_db)
                if ConfigDbSing.connect_db is None:
                    ConfigDbSing.connect_db = {"user": "postgres", "password": "123", "host": "127.0.0.1", "port": 10000, "dbname": "DbTrade"}
                    ConfigDbSing.set_config(ConfigDbSing)

            # Name DB -----------------------------------------------
            ConfigDbSing.connect_db.update(dbname="DbTrade")
            # Comp -Name --------------------------------------------
            ConfigDbSing.connect_db.update(comp_pref = pref_comp)
            print(ConfigDbSing.connect_db)
            ConfigDbSing.set_config(self)

        _dir_data = pref_comp+ "Trade\\Data"
        if not(os.path.isdir(_dir_data)):
            os.mkdir(_dir_data)
        ConfigDbSing.connect_db['Data']=_dir_data


    @classmethod
    def getInstance(cls):
        if not cls.__instance:
            cls.__instance = ConfigDbSing()
        return cls.__instance

    def get_config(cls):
        return ConfigDbSing.connect_db

    def set_config(cls):
        with open(cls.path_json, 'w') as file:
            json.dump(ConfigDbSing.connect_db, file)
        # cls.connect_db = {"user": "postgres", "password": "123", "host": "127.0.0.1", "port": 10000, "dbname": "DbTrade"}

    def path_dan(self):
        return ConfigDbSing.connect_db['Data']

    def path_files(self, s):
        return  ConfigDbSing.connect_db['comp_pref']+s