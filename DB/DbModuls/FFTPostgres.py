
from Ticker import Ticker

class FFTPostgres(Ticker):
    def __init__(self, *args, **kwargs):
        Ticker.__init__(self, *args, **kwargs)
        print("-- FFTPostgres --")

        ls_count_name = self.column_name(self.name_tick)
        _ls = [x[0] for x in ls_count_name]
        if not ('fft' in _ls):
            self.fcommand_execute(f"ALTER TABLE {self.name_tick} ADD COLUMN fft json;")



    def calc(self, *args, **kwargs):
        _dan = self.get_ohlcv(*args, **kwargs)
        k=1


    def set_fft(self):
        pass

    def get_fft(self, *args, **kwargs):
        db_min = kwargs.get('dt0', self._dt_begin)
        db_max = kwargs.get('dt1', self._dt_end)
        self.nametime = kwargs.get("nametime", self.nametime)
        self.id_pref = self._tpref.insert(self.nametime)

        _session = self._tdt.set_session(session = kwargs.get('session', []))
        _nt = self.name_tick   # f" {self._tdt._dbname}.id,"
        _ntdt = self._tdt._dbname                                    # DISTINCT
        _send = f"select  {_nt}.id, {_ntdt}.datetime, {_nt}.fft " \
                f"from {_ntdt}, {_nt} " \
                f"where {_nt}.Pref_Id={self.id_pref} " \
                f" {_session}  and (tdt.datetime >= '{db_min}' and tdt.datetime < '{db_max}')  " \
                f"and {_nt}.tdt_id=tdt.id ORDER BY tdt.datetime"

        return self.read_db_to_pandas(_send, ['id', 'datetime', 'fft']).to_dict()


    def __setitem__(self, name, value):
        self.__dict__[name]=value
#        self.name =value


    def __getitem__(self, key):
        return self.__dict__[key]
#        return self.key

