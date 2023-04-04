# https://khashtamov.com/ru/postgresql-python-psycopg2/

import pandas as pd

import psycopg2
from contextlib import closing
from psycopg2.extras import DictCursor
from psycopg2 import sql
from DecoratorTabls import *


def command_fetchone(fn):
    def wrapper(self, *args, **kwargs):
        with closing(psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.host,
                                      port=self.port)) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                conn.autocommit = True
                cursor.execute(fn(self, *args, **kwargs))
                _count = cursor.fetchone()
                return None if _count is None else _count if len(_count) > 0 else None

    return wrapper


def command_fetchall(fn):
    def wrapper(self, *args, **kwargs):
        with closing(psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.host,
                                      port=self.port)) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(fn(self, *args, **kwargs))
                _count = cursor.fetchall()
                return None if _count is None else _count if len(_count) > 0 else None

    return wrapper


def command_execute(fn):
    def wrapper(self, *args, **kwargs):
        with closing(psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.host,
                                      port=self.port)) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                conn.autocommit = True
                cursor.execute(fn(self, *args, **kwargs))

    return wrapper


def command_sdlexecute(fn):
    def wrapper(self, *args, **kwargs):
        with closing(psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.host,
                                      port=self.port)) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                conn.autocommit = True
                sql_update_query, _sourse = fn(self, *args, **kwargs)
                cursor.executemany(sql_update_query, _sourse)

    #                cursor.executemany(fn(self, *args, **kwargs))

    return wrapper


class PSQLCommand:
    def __init__(self, *args, **kwargs):
        self.isSQL = True
        if len(args) > 0:
            _dx = args[0]
            self.dbname = _dx.get("dbname", "DbTrade")
            self.user = _dx.get("user", "postgres")
            self.password = _dx.get("password", "123")
            self.host = _dx.get("host", "127.0.0.1")
            self.port = _dx.get("port", 10000)

        else:
            self.dbname = "DbTrade"
            self.user = "postgres"
            self.password = "123"
            self.host = "127.0.0.1"
            self.port = 10000

    @command_execute
    def fcommand_execute(self, send):
        return send

    @command_fetchall
    def fcommand_fetchall(self, send):
        return send

    @command_fetchone
    def fcommand_fetchone(self, send):
        return send

    def _connect(self):
        try:
            return psycopg2.connect(dbname=self.dbname,
                                    user=self.user,
                                    password=self.password,
                                    host=self.host,
                                    port=self.port)
        except:
            return None

    @command_fetchall
    def tabl_count(self):
        return "SELECT table_name FROM information_schema.tables WHERE table_schema='public'"

    # @command_fetchone
    # def _is_rec_in_table(self, table, pole, value):
    #     return f"SELECT  count({pole})  FROM {table}  WHERE name='{value}';"

    #  ----  IS END  ---------------
    def is_tabl(self, name_tabl):
        return False if self.fcommand_fetchone(
            f"select tablename from pg_tables where tablename='{name_tabl}'") is None else True

    #  ----  DEL, CLEAR BEGIN  ---------------
    @command_execute
    def del_table(self, table1):
        # if 'list' in str(type(table1)):
        #     table = ', '.join(table1)
        # else:
        #     table = table1
        table = ', '.join(table1) if 'list' in str(type(table1)) else table1
        return f"DROP TABLE IF EXISTS  {table} CASCADE;"


    def del_tables(self, tables):
        for it in tables:
            if self.is_tabl(it):
                self.del_table(it)

    @command_execute
    def clear_table(self, table):
        return f"TRUNCATE {table} CASCADE"

    @command_execute
    def clear_tadle(self, name_table):
        return f"DELETE FROM {name_table};"

    #  ----  INSERT BEGIN  ---------------

    @command_execute
    def finsert(self, pole, values):
        return sql.SQL(f'INSERT INTO {pole}'
                       ' VALUES {};').format(sql.SQL(',').join(map(sql.Literal, values)))

    @command_execute
    def finsert_one(self, pole, values):
        return sql.SQL(f'INSERT INTO {pole}'
                       ' VALUES ({});').format(sql.SQL(',').join(map(sql.Literal, values)))

    @value_insert
    def _value_one_new(self, _sourse):
        return [tuple([_sourse[it] for it in list(_sourse.keys())])]

    def insert_dan_new(self, tname: str, _sourse: dict):
        self.finsert(f"{tname} ({', '.join(list(_sourse[0].keys()))})", self._value_one_new(_sourse))

    def read_db_to_pandas(self, *args, **kwargs):
        return pd.DataFrame(self.fcommand_fetchall(args[0]), columns=args[1])

    # -----  Удалить столбец  --------------------
    def db_colum(self, dbname, column_name):
        self.fcommand_execute(f"ALTER TABLE {dbname} DROP {column_name} description CASCADE; ")

    def calc_index(self, *args):
        ind = self._max_id(args[1], args[2])
        dval = args[0]
        _key = str(type([x for x in list(dval.keys())][0]))
        if "int" in _key:
            for key, val in dval.items():
                ind += 1
                val[args[2]] = ind
            return dval
        else:
            dval[args[2]] = ind + 1
        return dval

    def find_index(self, name_table):
        return self.fcommand_fetchall(f"SELECT indexname FROM pg_indexes WHERE tablename = '{name_table}';")

    def find_index_count(self, name_table, name_index):
        x1 = self.find_index(name_table)
        if x1 is None:
            return 0

        return [it[0] for it in x1 if it[0] == name_index].__len__()
        # return self.fcommand_fetchall(f"SELECT indexname FROM pg_indexes WHERE tablename = '{name_table}';")

    def create_index(self, name_table, name_index):
        return self.fcommand_execute(f"CREATE INDEX {name_index} ON {name_table}; ")
        #  CREATE INDEX test2_mm_idx ON test2 (major, minor);    name_table---> test2 (major, minor)

    def delete_index(self, name_index):
        return self.fcommand_fetchall(f"DROP INDEX {name_index} ;")

    def reindex(self, name_index):
        return self.fcommand_execute(f"REINDEX INDEX {name_index} ;")

    def column_name(self, name_table):
        _send = f"SELECT column_name " \
                f"FROM information_schema.columns " \
                f"WHERE table_name = '{name_table}' ORDER BY ordinal_position;"
        return self.fcommand_fetchall(_send)

    def is_test_field(self, td_name, field):
        _z = self.fcommand_fetchone(f"SELECT * FROM {td_name} "
                                    f"WHERE '{field}'  in "
                                            f"(SELECT column_name "
                                                f"FROM information_schema.columns "
                                                    f"WHERE table_name = '{td_name}') LIMIT 1;")
        return False if (_z is None) or (len(_z) == 0) else True


'''
    
    @command_execute
    def fupdate(self, tname, name0, id0, values):
        kk=1
        # for k in values.keys():
        #     s0 = sql.Identifier(str(k))
        #     s1 = sql.SQL(" = ")
        #     s2 =sql.Placeholder(str(k))
        #     fff=1

        # name=sql.SQL(', ').join(sql.Composed([sql.Identifier(str(k)), sql.SQL(" = "), sql.Placeholder(k)]) for k in values.keys()),
        # id1=sql.Placeholder('id')

        send = sql.SQL('UPDATE {} SET {}= {}  WHERE {}={}').format(tname, name0,id0,
            name=sql.SQL(', ').join(sql.Composed([sql.Identifier(str(k)), sql.SQL(" = "), sql.Placeholder(str(k))]) for k in values.keys()),
                id1=sql.Placeholder('id'))

        return send
                       #' VALUES {};').format(sql.SQL(',').join(map(sql.Literal, values)))


        # send = f"""Update  {tname} SET {name0}=%s WHERE {name1}=%s"""
        # return send, values)))

    sql_query = sql.SQL("UPDATE people SET {data} WHERE id = {id}").format(
        data=sql.SQL(', ').join(
            sql.Composed([sql.Identifier(k), sql.SQL(" = "), sql.Placeholder(k)]) for k in upd.keys()
        ),
        id=sql.Placeholder('id')
    )

    #
    # @command_execute
    # def fupdate_one(self, table_name, values):
    #     return sql.SQL(f'UPDATE {table_name}'
    #                    ' VALUES ({});').format(sql.SQL(',').join(map(sql.Literal, values)))
    #
    # @value_insert
    # def _update_one(self, _sourse):
    #     return [tuple([_sourse[it] for it in list(_sourse.keys())])]

    def update_dan(self, tname: str, _sourse: dict):
        self.fupdate(f"{tname} ({', '.join(list(_sourse[0].keys()))})", self._update_one(_sourse))
'''

'''

    # @command_execute
    # def delet_pole(self, table, pole):
    #     return f"DELETE FROM {table} WHERE {pole}"
    #
    # def delet_poles(self, table, pole):
    #     for item in pole:
    #         self.delet_pole(table, item)

    # @command_execute
    # def clear_tadle(self, name_table):
    #     return f"DELETE FROM {name_table};"

    #  ----  DEL END  ---------------

    # @command_fetchone
    # def _count_rec_table(self, nametable, pole="count(*)"):
    #     return f"SELECT {pole} FROM {nametable};"
    #
    # def _max_id(self, table, pole):
    #     xx = self._all_rec_table(table, pole)
    #     return -1 if None == xx else max(xx)[0]
    #
    # @command_fetchall
    # def _all_rec_table(self, nametable, value="*", _where=""):
    #     return f"SELECT {value} FROM {nametable} {_where};"



    @command_execute
    def insert_add(self, send):
        return send

    def add_pole(self, selftabl, name_pole, ls=[]):
        if len(ls) <= 0:
            return

        dval0 = selftabl.get()
        if dval0 is None:
            key = ls
        else:
            dval = [str(val).strip() for key, val in dval0.items()]
            key = list(set(ls) - set(dval))

        _ = {selftabl.insert_dan_inc({name_pole: val}) for i, val in enumerate(key, start=0)}

    @get_index_int
    def get_index_name_int(self, _send):
        return self.fcommand_fetchall(_send)

    def add_rec_instal(self, sourse, fun0, fun1):
        _ls = [val["name"] for key, val in sourse.items()]
        _x = fun0()

        if _x is None:
            fun1(sourse)
            return

        __ls = [str(val[0]).strip() for key, val in _x.items()]
        _sourse0 = {key: val for key, val in sourse.items() if (val["name"] not in __ls)}

        if len(_sourse0) > 0:
            fun1(_sourse0)



    def del_all_tables(self):
        tables = self.tabl_count()
        _ = [self.del_table(iten[0]) for iten in tables]

    # def del_all_table_not_(self, ls = ["addfileclfjson"]):
    #     _ = [self.del_table(iten) for iten in list(set([iten[0] for iten in self.tabl_count()])-set(ls))]



    #  ----  IS BEGIN  ---------------
#     @command_fetchone
#     def _is_tabl(self, name_tabl):
#         return f"select tablename from pg_tables where tablename='{name_tabl}'"
# #        return f"SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name='{mane_tabl}')"




import copy
import psycopg2
from contextlib import closing
from  psycopg2.extras import DictCursor


def command_fetchone(fn):
    def wrapper(self, *args, **kwargs):
        with closing(psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.host,
                                      port=self.port)) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(fn(self, *args, **kwargs))
                _count = cursor.fetchone()
                return None if _count is None else _count if len(_count) > 0 else None
    return wrapper


class PSQLCommand:

    def __init__(self, *args, **kwargs):
        self.dbname = kwargs.get("dbname", "BasaLogDan")
        self.user = kwargs.get("user", "postgres")
        self.password = kwargs.get("password", "123")
        self.host = kwargs.get("host", "127.0.0.1")
        self.port = kwargs.get("port", 9000)
        self.db_host = dict()
        self.db_host["dbname"] = self.dbname
        self.db_host["user"] = self.user
        self.db_host["password"] = self.password
        self.db_host["host"] = self.host
        self.db_host["port"] = self.port

    @command_fetchone
    def send_com(self, table):
        _send = f"SELECT count(*) FROM {table};"
        return _send




if __name__ == '__main__':
    _db_host_port = {"dbname": "TradeDb", "user": "postgres", "password": "123", "host": "127.0.0.1", "port": 9000}

    _com1 = MyPSQLCommand(_db_host_port)
#    xx = _com1.send_com("car")
#    print(xx)
    k = 1


'''
