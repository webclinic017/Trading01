from PSQLCommand import PSQLCommand
from DecoratorTabls import *
from datetime import datetime, time, timedelta


class TDateTime(PSQLCommand):
    def __init__(self, *args, **kwargs):
        PSQLCommand.__init__(self, *args, **kwargs)
        self._dbname = "tdt"
        self._name_idx = f"{self._dbname}_idx"
        if not (self.is_tabl(self._dbname)):
            if self.find_index_count(self._dbname, self._name_idx) != 0:
                self.delete_index(self._name_idx)

            send = f"CREATE TABLE {self._dbname}" \
                   "(ID bigserial PRIMARY KEY," \
                   "DATETIME timestamp, " \
                   "DAY_OF_WEEK integer );"
            self.fcommand_execute(send)

        if self.find_index_count(self._dbname, self._name_idx) == 0:
            self.create_index(f"{self._dbname}  (datetime)", self._name_idx)
        else:
            pass

    def create_table(self, name):
        self.fcommand_execute(f"CREATE TABLE {name} (DATETIME timestamp, b boolean);")

    def insert(self, ls: list):
        print(" TDatetime - insert поиск и добавление новых значений datetime \n Поиск")
        _xdt = "xdt"
        _s = ", ".join(f"'{str(x)}'" for x in ls)

        if not (self.is_tabl("xdt")):
            self.create_table("xdt")
        else:
            self.clear_tadle("xdt")

        _sourse = {}
        for i, dx in enumerate(ls):
            _sourse[i] = dict(datetime=dx, b=True)

        self.insert_dan_new('xdt', _sourse)

        _send = "select datetime from xdt where datetime NOT IN " \
                "(select DISTINCT xdt.datetime from xdt, tdt where xdt.datetime IN (tdt.datetime))"
        _d = self.fcommand_fetchall(_send)
        if _d is None:
            self.clear_tadle("xdt")
            return

        print(" TDatetime - insert добавление новых значений datetime")
        _sourse = {}
        for i, dx in enumerate(_d):
            _sourse[i] = dict(datetime=dx[0], day_of_week=dx[0].weekday())
        self.insert_dan_new(self._dbname, _sourse)
        self.reindex(self._name_idx)
        self.clear_tadle("xdt")

    def get(self, ls: list):
        _s = ", ".join(f"'{str(x)}'" for x in ls)
        _send = f"select datetime, id from {self._dbname} where datetime IN ({_s})"
        return {it[0]: it[1] for it in self.fcommand_fetchall(_send)}

    def add_list(self, ls:list):
        new_key = list( set(ls)-set(self.get(ls).keys()))
        self.insert(new_key)

    def add_list_return(self, ls:list):
        new_key = list( set(ls)-set(self.get(ls).keys()))
        self.insert(new_key)
        return  self.get(ls)


'''

    def InicialWeek_number(self):

        startdt = datetime(2005, 1, 2)
        enddt = datetime(2030, 12, 31)

        self._dtBasaWeek, _sourse, i = [], dict(), 0
        while startdt < enddt:
            # if startdt.weekday() == 0:
            self._dtBasaWeek += [startdt]
            _sourse[i] = dict(datetime=startdt, day_of_week=6, session=100)
            i += 1

            startdt = startdt + timedelta(days=7)

        self.insert_dan_new(self._dbname, _sourse)

    def set_session(self, *args, **kwargs):
        if args.__len__()>0:
            return ""
        __sdate = f" and  {self._dbname}.datetime >='{self.dt_evening_session}' "
        sf = f" and {self._dbname}.session in (0, 1)"
        x = kwargs.get("session", sf)
        x1 = str(type(x))
        if 'list' in x1:
            _is_evening_session = (1 in x) and (x.__len__()==1)
            if x.__len__() == 0:
                return sf + __sdate if _is_evening_session else sf
            __z = f' and {self._dbname}.session in ({", ".join([str(z) for z in x])})'
            return  __z + __sdate if _is_evening_session else __z

        return x



        # send = "SELECT tdt.id, tdt.datetime, tdt.DAY_OF_WEEK from tdt"
        # dan = self.read_db_to_pandas(send, ["id", "datetime", "day_of_week"])
# !!!!!?????            self.reindex(self._name_idx)

    # @value_insert
    # def _value_one(self, _sourse):
    #     return [(_sourse["datetime"], _sourse["day_of_week"], _sourse["session"])]
    #
    # def insert_dan(self, _sourse: dict):
    #     self.finsert(
    #         f"{self._dbname} (datetime, day_of_week, session)",
    #         self._value_one(_sourse))
    #
    # @value_insert
    # def _value_one_dt(self, _sourse):
    #     return [(_sourse["datetime"], _sourse["b"])]
    #
    # def insert_dan_dt(self, nametb, _sourse: dict):
    #     self.finsert(
    #         f" {nametb} (datetime, b)",           # xdt
    #         self._value_one_dt(_sourse))

    # @value_insert
    # def _value_one_week(self, _sourse):
    #     return [(_sourse["datetime"], _sourse["b"])]
    #
    # def insert_dan_week(self, _sourse: dict):
    #     self.finsert(
    #         f"{self._db_week} (datetime)",
    #         self._value_one_week(_sourse))

  
'''
