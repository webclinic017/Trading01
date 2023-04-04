from PSQLCommand import *
from Ticker import Ticker
import numpy as np
import re, json


# from abc import ABC, abstractmethod

class ElementPostgres(Ticker):
    def __init__(self, *args, **kwargs):
        Ticker.__init__(self, *args, **kwargs)

        if args.__len__() < 3:
            return

        self._dt0 = args[0].get('dt0', self._dt_begin)
        self._dt1 = args[0].get('dt1', self._dt_end)
        self._candels = args[0].get('candels', ['close'])
        self._candel = self._candels[0]
        self._candel = args[0].get('candel', self._candel)

        self._nfft = 32
        self.__mbasa = None
        self.__candel = None

        self.field = args[1]
        self.type_field = args[2]
        print(f"-- ElementPostgres  ->> поле {self.field} тип ->> {self.type_field}  --")

        if not (self.is_test_field(self.name_tick, self.field)):
            self.fcommand_execute(f"ALTER TABLE {self.name_tick} ADD COLUMN {self.field} {self.type_field};")

    def read_db_ohlcv(self):
        self.dtcandels = self.get_ohlcv(self._candels)

    def get_field(self, **kwargs):
        db_min = kwargs.get('dt0', self._dt_begin)
        db_max = kwargs.get('dt1', self._dt_end)
        _limit = kwargs.get('limit', "")
#         LIMIT 1000;

        _session = self._tdt.set_session(session=[])
        _nt = self.name_tick
        _ntdt = self._tdt._dbname

        print(f" Запрос занных из db  {self.nametime}  по полю {_nt}.{self.field} дата: {db_min} - {db_max}")

        _send = f"select  {_nt}.id, {_ntdt}.datetime, {_nt}.{self.field} " \
                f"from {_ntdt}, {_nt} " \
                f"where {_nt}.Pref_Id={self.id_pref} " \
                f" {_session}  and ({_ntdt}.datetime >= '{db_min}' and {_ntdt}.datetime < '{db_max}')  " \
                f"and {_nt}.tdt_id=tdt.id ORDER BY tdt.datetime {_limit}"

        return self.read_db_to_pandas(_send, ['id', 'datetime', f'{self.field}']).to_dict()

    def get_key_dict_field1(self, **kwargs):
        kwargs['limit'] = 'limit 1'
        dan = self.get_field(**kwargs)
        if dan is None:
            return None
        # z = dan[self.field]
        # zkey = list(z[0].keys())
        # for key in zkey:
        #     print(key)
        #     lll=1
        return list(dan[self.field][0].keys())

    @command_sdlexecute
    def fupdate_nor(self, _sourse):
        sql_update_query = f"""Update {self.name_tick} set {self.field} = %s where id = %s"""
        return sql_update_query, _sourse

    def outer_function(self, dmas):
        return None

    def __calc_m_basa(self):
        _m = np.zeros(self._nfft).tolist()
        _datetime = self.dtcandels['datetime']
        _dt_start = [(key, val) for key, val in _datetime.items() if val < self._dt0]
        self._id_start = len(_dt_start)
        if self._id_start == 0:
            pass
        elif self._id_start >= self._nfft:
            _m = [val for key, val in self.dtcandels[self.__candel].items()
                  if key in [key[0] for key in _dt_start[-self._nfft:]]]
        else:
            _count = len(_dt_start)
            _m[-_count:] = [val for key, val in self.dtcandels[self.__candel].items()
                            if key in [key[0] for key in _dt_start[-self._nfft:]]]
        self.__mbasa = _m
        return _m

    def calc_all_xxx(self, params):
        _m = None
        # _d = re.match(r'\d*', self.nametime).group(0)
        # self._pref = _d + self.nametime[len(_d)] +  str(self._nfft)
        self._pref = str(self._nfft)
        self._pref= params.get('pref', self._pref)

        _sourse0 = self.get_field(dt0=self._dt0, dt1=self._dt1)
        _sourse = {_sourse0['id'][i]: _sourse0[f'{self.field}'][i] for i in range(len(_sourse0['id']))}

        for _candel in self._candels:
            print(f" Обработка  -> {_candel} ")
            self.__candel = _candel
            _pref = self._pref + _candel
            _m = self.__calc_m_basa()

            _datetime = self.dtcandels['datetime']
            _id_dt_end1 = [(key, val) for key, val in _datetime.items() if val >= self._dt1]
            if len(_id_dt_end1) == 0:
                self._id_dt_end = len(self.dtcandels['datetime'])
            else:
                self._id_dt_end = _id_dt_end1[0][0]

            for i in range(self._id_start, self._id_dt_end + 1):
                try:
                    print(
                        f"  {self.nametime}   {self._nfft}  {_candel} - {i}  = {self._id_dt_end}   дата   {_datetime[i]} ")
                except:
                    break

                _m.pop(0)
                _m.append(self.dtcandels[_candel][i])
                __d = self.outer_function(_m)
                try:
                    _xd = _sourse[self.dtcandels['id'][i]]
                    _xd[_pref] = __d
                    _sourse[self.dtcandels['id'][i]] = _xd
                except:
                    _sourse[self.dtcandels['id'][i]] = {_pref: __d}

        print('подготовка данных для записи в базу')
        _sourse_conv = [tuple([json.dumps(val), key]) for key, val in _sourse.items()]
        print('  запись в базу .....')
        self.fupdate_nor(_sourse_conv)
        print('  записали в базу!!!!!')

    # def get_field(self, *args, **kwargs):
    #     # db_min = kwargs.get('dt0', self._dt_begin)
    #     # db_max = kwargs.get('dt1', self._dt_end)
    #
    #     self.nametime = kwargs.get("nametime", self.nametime)
    #     self.id_pref = self._tpref.insert(self.nametime)
    #
    #     _session = self._tdt.set_session(session = [])
    #     _nt = self.name_tick   # f" {self._tdt._dbname}.id,"
    #     _ntdt = self._tdt._dbname                                    # DISTINCT
    #     _send = f"select  {_nt}.id, {_ntdt}.datetime, {_nt}.{self.field} " \
    #             f"from {_ntdt}, {_nt} " \
    #             f"where {_nt}.Pref_Id={self.id_pref} " \
    #             f" {_session}  and ({_ntdt}.datetime >= '{db_min}' and {_ntdt}.datetime < '{db_max}')  " \
    #             f"and {_nt}.tdt_id=tdt.id ORDER BY tdt.datetime"
    #
    #     return self.read_db_to_pandas(_send, ['id', 'datetime', f'{self.field}']).to_dict()
    #

    def calc(self):
        k = 1
        return 0
