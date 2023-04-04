from datetime import datetime, time, timedelta
import pandas as pd
from DecoratorTabls import *
#from PSQLCommand import PSQLCommand, command_sdlexecute
from PSQLCommand import *

from Ticker import Ticker
import csv
import numpy as np
import re


class NormVSA(Ticker):
    def __init__(self, *args, **kwargs):
        Ticker.__init__(self, *args, **kwargs)
        self._id_nametime = None
        self._dtWeekId = None
        print("-- normVSA --")

        self._pref_kof0, self._pref_kof1, self._pref_norm = None, None, None

        ls_count_name = self.column_name(self.name_tick)
        _ls = [x[0] for x in ls_count_name]
        if not ('nork' in _ls):
            self.fcommand_execute(f"ALTER TABLE {self.name_tick} ADD COLUMN nork real[];")
        if not ('nor' in _ls):
            self.fcommand_execute(f"ALTER TABLE {self.name_tick} ADD COLUMN nor real[];")

        self._dtWeekId, self._dtWeekLs = self.get_week()  # self._tdt.get_week(', nork ')
        self._dtWeekLs = np.array(self._dtWeekLs)

    def find_dt(self, _dtx: datetime):
        return np.min(self._dtWeekLs[self._dtWeekLs > _dtx])

    def find_dt_min(self, _dtx: datetime):
        return np.max(self._dtWeekLs[self._dtWeekLs < _dtx])

    def finds_dt(self, lsdt):
        _dtls = []
        for it in lsdt:
            _dtls += [self.find_dt(it)]
        return _dtls

    # f"  and ({_dt_n}.datetime >= '{self._dt_begin}' and {_dt_n}.datetime < '{self._dt_end}')  " \

    def get_week(self, snork=""):
        _nt = self.name_tick
        _dt_n = self._tdt._dbname
        fun = lambda id_pref: f"select DISTINCT tdt.datetime, {_nt}.nork  from {_dt_n}, {_nt} " \
                              f"where {_nt}.Pref_Id={id_pref} " \
                              f" and {_nt}.tdt_id={_dt_n}.id " \
                              f" and {_dt_n}.session = 100  " \
                              f"ORDER BY {_dt_n}.datetime"

        if snork == "":
            _dan = {z[0]: z[1] for z in
                    self.fcommand_fetchall(f"select datetime, id  from {self._tdt._dbname} where session=100;")}
            return _dan, list(_dan.keys())

        return {z[0]: z[1] for z in self.fcommand_fetchall(fun(self._pref_id_kof0))}, \
               {z[0]: z[1] for z in self.fcommand_fetchall(fun(self._pref_id_kof1))}

    def _calc_coef(self, *args, **kwargs):
        k = 1
        nametime = kwargs.get('nametime', "5min")
        self.id_pref = self._tpref.get_index(nametime)
        session = kwargs.get('session', [0])
        _id_session = session[0] if session.__len__() > 0 else 0

        timeframe_end = kwargs.get('timeframe_end', "1W")
        dt0, dt1 = self.db_min_max(self.id_pref)

        _dan0 = self.read_db_pandas(dt0=dt0, dt1=dt1,  session=session)

        _d = re.match(r'\d*', nametime).group(0)
        _pref_kof = _d + nametime[len(_d)] + "Nk" + str(_id_session)

        pref_id_koef = self._tpref.insert(_pref_kof)

        _dan0.index = pd.to_datetime(_dan0.datetime)

        _dan0['oc'] = abs(_dan0['close'] - _dan0['open'])
        _dan0['hl'] = abs(_dan0['high'] - _dan0['low'])
        _dan0['th'] = _dan0.high - _dan0[["open", "close"]].max(axis=1)
        _dan0['tl'] = _dan0[["open", "close"]].min(axis=1) - _dan0.low
        _dan0['doc'] = _dan0['oc']
        _dan0['dhl'] = _dan0['hl']
        _dan0['dth'] = _dan0['th']
        _dan0['dtl'] = _dan0['tl']
        _dan0['dvol'] = _dan0['volume']

        _dan1 = _dan0.resample(timeframe_end).agg({
            'datetime': 'last',
            'oc': 'max', 'hl': 'max', 'th': 'max', 'tl': 'max', 'volume': 'max',
            'doc': 'std', 'dhl': 'std', 'dth': 'std', 'dtl': 'std', 'dvol': 'std'})  #


        _dtls = _dan1['datetime'].tolist()
        _dtls0 = self.finds_dt(_dtls)

        self._tdt.insert(_dtls0)
        _id_dt = self._tdt.get(_dtls0)

        _sourse = {}
        i = 0
        print("  формируем данные для записи")
        for i1, row in _dan1.iterrows():  # print(f"Index: {i}")  print(f"{row}\n")
            xx = row.to_dict()
            _sourse[i] = dict(pref_id=pref_id_koef,
                              tdt_id=_id_dt[_dtls0[i]],
                              nork=[xx['oc'], xx['hl'], xx['th'], xx['tl'], xx['volume'],
                                    xx['doc'], xx['dhl'], xx['dth'], xx['dtl'], xx['dvol']])
            i += 1
        print(f"  пишем в  {self.name_tick} запись")
#        self.insert_dan_norm_kof(_sourse)
        self.insert_dan_new(self.name_tick, _sourse)


    def Calc_koef(self, *args, **kwargs):
        kwargs['session'] = [0]
        self._calc_coef(**kwargs)
        kwargs['session'] = [1]
        self._calc_coef(**kwargs)
        kkkk=1

    def Calc_ohlcv(self, *args, **kwargs):
        nametime = kwargs.get('nametime', "5min")
        print(f"   Нормируем данные по времени {nametime} ")

        self._id_nametime = self._tpref.get_index(nametime)
        _d = re.match(r'\d*', nametime).group(0)
        self._pref_kof0 = _d + nametime[len(_d)] + "Nk" + str(0)
        self._pref_kof1 = _d + nametime[len(_d)] + "Nk" + str(1)
        self._pref_id_kof0 = self._tpref.insert(self._pref_kof0)
        self._pref_id_kof1 = self._tpref.insert(self._pref_kof1)
        self._pref_id_norm = self._tpref.insert(self._pref_norm)

        self.koef0, self.koef1 = self.get_week(' nork ')

        self.repeat_dan(nametime, self.SaveNormal)

    def SaveNormal(self):
        sid = f" {self._tdt._dbname}.id,"
        _dan = self.read_db_pandas(dt0 = self._dt_begin, dt1 = self._dt_end, id_pref = self._id_nametime, session=[])
        _ddan0 = _dan.to_dict()
        _dtls = list(_ddan0['datetime'].values())

        _dtstart = self.find_dt_min(_dtls[0])
        if not (_dtstart in self.koef0.keys()):
            _d0K0 = list(self.koef0.keys())[0]
            _dv0K0 = self.koef0[_d0K0]
            _d0K01 = _d0K0 - timedelta(days=7)
            self.koef0[_d0K01] = _dv0K0
            _dv0K1 = self.koef1[_d0K0]
            self.koef1[_d0K01] = _dv0K1

        _koefx = []

        _dan['oc'] = _dan['close'] - _dan['open']
        _dan['hl'] = _dan['high'] - _dan['low']
        _dan['th'] = _dan.high - _dan[["open", "close"]].max(axis=1)
        _dan['tl'] = _dan[["open", "close"]].min(axis=1) - _dan.low
#        _dan[_dan['hl'] == 0] = 0.01
        _dan['spr_p'] = (_dan['close'] - _dan['low']) / _dan['hl']
        _dan['spr_m'] = (_dan['close'] - _dan['high']) / _dan['hl']

        _dan['spr_p'] = round(_dan['spr_p'], 1)
        _dan['spr_m'] = round(_dan['spr_m'], 1)

        _dan = _dan.fillna(0.0)
        data_tek = datetime(2000, 1, 1).date()

        _sourse = []
        for row in _dan.itertuples():
            if data_tek != row.datetime.date():
                data_tek = row.datetime.date()
                dtKx = self.find_dt_min(row.datetime)
                _koefx = [self.koef0[dtKx], self.koef1[dtKx]]
                print(row)

            #                print(row.datetime , row.datetime.date(), row.datetime.time(),  row.open)

            k = 0 if row.datetime.hour < 19 else 1
            nor = []

            # spread - положительный/отрицательный
            if row.oc > 0:
                nor += [row.spr_p]
            else:
                nor += [row.spr_m]
            # нормируем oc
            nor += [round(min(row.oc / _koefx[k][0], 1), 1)]

            # нормируем hl
            nor += [round(min(row.hl / _koefx[k][1], 1), 1)]

            # нормируем th
            nor += [round(min(row.th / _koefx[k][2], 1), 1)]

            # нормируем tl
            nor += [round(min(row.tl / _koefx[k][3], 1), 1)]

            # нормируем volume
            nor += [round(min(row.volume / (_koefx[k][9]*5), 1), 1)]    # 4
#            nor += [round(min(row.volume / (_koefx[k][4]), 1), 1)]    # 4
            z = tuple([nor, row.id])
            # print(f"  row.id = {row.id}")
            _sourse+= [z ]

        print(" запускаем программу обновления записи")
        self.fupdate_nor(_sourse)

    @command_sdlexecute
    def fupdate_nor(self,  _sourse):
        sql_update_query = f"""Update {self.name_tick} set nor = %s where id = %s"""
        return sql_update_query, _sourse

'''
!!!!!!!!!!!    ОБРАТИТЬ ВНИМАНИЕ НА ПРИМЕРЫ  !!!!!!!!!!!!!!!!!!!!!!!!!!!


        # koef0 = self.fcommand_fetchall(fun(self._pref_id_kof0))
        # koef1 = self.fcommand_fetchall(fun(self._pref_id_kof1))
        # koef0 = {z[0]:z[1] for z in koef0}
        # koef1 = {z[0]:z[1] for z in koef1}
        # return koef0, koef1


        # db_min = kwargs.get('dt0', db_min)
        # db_max = kwargs.get('dt1', db_max)
        # self.id_pref = kwargs.get('id_pref', '1')


        # добаввить строку вначало таблицы
        # x1 = _dan1.iloc[[0]]  
        # _dt_start = (x1.datetime)[0]   
        # _dt_start = self.find_dt_min(_dt_start)
        # x1.datetime = _dt_start # datetime(2000, 1, 1, 0, 0)   
        # _dan1 = pd.concat([x1, _dan1])



        # _dan01 = _dan0.resample("1W").agg({
        #     'datetime': 'first', 'open1': 'close-open', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'})
        #        _dan01 = _dan0.resample("1W").agg({'date': 'last'})




        k = 1
        # _dtls = koef0['datetime'].tolist()
        # _dtls += [_dtls[-1] + timedelta(days=7)]
        # _dkoef0 = koef0.to_dict()
        # _dt0 = _dkoef0['datetime']
        # _nor0 = _dkoef0['nork']
        # for key, val in _dkoef0.items():
        #     _key0 = key
        #     _key1 = key.split
        #     _val = val

        for i in range(_dtls.__len__() - 1):
            print(f"{_dtls[i]}     {_dtls[i + 1]}  ")
        k = 1
   
        
#
#         _dan01.index = pd.to_datetime(_dan01.datetime)
#
#
#         for row in _dan0.itertuples(name='oc'):
# #            print(row)
#             dt0 = row.datetime
#             print(dt0)
#             _z0 = _dan01.groupby(dt0<= _dan01.datetime).max() #.min()
# #            print(_z0["datetime"])
#             _dt01 = _z0['datetime']
#             _dt02 = _dt01.iloc[0]
#             print(f" -----  {_dt02}")
#             if dt0 >= datetime(2021, 2, 5):
#                 jjj=1
#
# #            if dt0 > datetime(_dt02.year, _dt02.month, _dt02.day, _dt02.hour, _dt02.minute):
#             if dt0 > _dt02:
#                 jj=1
#             kk=1
#
#         for row in _dan01.itertuples(index=False, name='People'):
#             print(row)
#
#
#         for row in _dan01.itertuples():
#             print(row)
#             print(row.datetime , row.oc)
#             k=1
#
#         for i, row in _dan01.iterrows():
#             print(f"Index: {i}")
#             print(f"{row}\n")
#             print(f"{row['oc']}\n")
#             k=1
#
#         print(_dan01.head(20))
#         _count = len(_dan01)
#         for _item, _d in _dan01.items():
#             xx0 = _item
#             xx1 = _d
#             print(xx1[0], xx1[1])
#             kk=1
#         print('------------------------------------------------------------------------')
#
# #        print(_dan01.tail(20))
#
#         k=1

        kkk = 1

    # @value_insert
    # def _value_one_norm_kof(self, _sourse):
    #     return [(_sourse["pref_id"], _sourse["tdt_id"], _sourse["nork"])]
    #
    # def insert_dan_norm_kof(self, _sourse: dict):
    #     self.finsert(
    #         f"{self.name_tick} (pref_id, tdt_id, nork)",
    #         self._value_one_norm_kof(_sourse))
 
 

    #                f"{_nt}.nork[1], {_nt}.nork[2], {_nt}.nork[3], {_nt}.nork[4], {_nt}.nork[5] from tdt, {_nt} " \
    #
    # def read_koef(self, id_pref):
    #     _nt = self.name_tick
    #     _send = f"select DISTINCT tdt.datetime, {_nt}.nork  from tdt, {_nt} " \
    #             f"where {_nt}.Pref_Id={id_pref} " \
    #             f"  and (tdt.datetime >= '{self._dt_begin}' and tdt.datetime < '{self._dt_end}')  " \
    #             f" and {_nt}.tdt_id={self._tdt._dbname}.id " \
    #             f" and {self._tdt._dbname}.session = 100  " \
    #             f"ORDER BY tdt.datetime"
    #     _dt_ohlcv = self.fcommand_fetchall(_send)
    #     #        _dan = pd.DataFrame(_dt_ohlcv, columns=['datetime', 'oc', 'hl', 'th', 'tl', 'volume'])
    #     _dan = pd.DataFrame(_dt_ohlcv, columns=['datetime', 'nork'])
    #     return _dan
 
'''
