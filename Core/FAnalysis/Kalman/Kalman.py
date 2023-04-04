import numpy as np

# from ElementPostgres import ElementPostgres


#class Kalman(ElementPostgres):
class Kalman():
    def __init__(self, *args, **kwargs):
 #       ElementPostgres.__init__(self, *args, 'trend', 'json', **kwargs)
        self._nfft = args[0].get('npoint', 32)  # для расчета периода STD
        self.read_db_ohlcv()

    def install(self):
        # self._dt_begin
        # self._dt_end
        self._count = len(self.dtcandels['id'])
        self._pref = 'kalman'+str(self._nfft)
        self.xx_old = 0.0
        self.P_old = 0.0

        # self.xx = np.zeros(self._count)
        # self.P = np.zeros(self._count)
        # self.DP = np.zeros(self._count)
        # self.DM = np.zeros(self._count)

        self.Ndisp = self._nfft
#        self.disper = np.zeros(self.Ndisp).tolist()
        self.enx = np.zeros(self.Ndisp).tolist()
        self.xx_old = self.dtcandels[self._candel][0]
        self.P_old = 1
        self.r = 1  # 0.999
        self.en = 0.1
        self.r2 = self.r * self.r
        self.en2 = self.en * self.en
        self._ind = 0
        params = {'pref':'kalman'+str(self._nfft)}
        self.repeat_dan_new(self.calc_all_xxx, params=params, dt0 = self._dt0, dt1 = self._dt1)

    def outer_function(self, _m):
        if self._ind == 0:
            self.xx_old = _m[self._nfft-1]
            self.P_old = 1
            delta = self.en * 0.7
            self._ind = self._ind + 1
            return {'d': self.xx_old, 'dp': self.xx_old + delta, 'dm':self.xx_old - delta}

        dNoise = np.std(_m)
        self.enx.pop(0)
        self.enx.append(self.xx_old)
        f0 = lambda x, y: x - y
        lsx = list(map(f0, _m, self.enx))
        en = np.std(lsx)

        z =_m[self._nfft-1]
        Pe = self.P_old + en * en
        P = (Pe * dNoise) / (Pe + dNoise)
        xx = self.xx_old + P / dNoise * (z -  self.xx_old)
        self.P_old = P
        self._ind = self._ind + 1
        self.xx_old = xx
        delta = self.en * 0.7
        return {'d': xx,  'dp': self.xx_old + delta, 'dm':self.xx_old - delta}


    def get_key_dict(self, **kwargs):
        keys = kwargs.get('keys', ['kalman120ohl'])
        _ls_keys = self.get_key_dict_field1(**kwargs)
        if len(keys)==0:
            return None
        _ls = [item for item in keys if item in _ls_keys]
        dan = self.get_field(**kwargs)
        _trend = dan['trend']
        _dtrend = {key: {} for key in _ls}
        _dtrend['datetime'] = [ val for key, val in  dan['datetime'].items()]
        _trend_count = len(_trend) 
        for itrm_key in _ls:
            _dtrend[itrm_key] = [_trend[i][itrm_key] for i in range(len(_trend))]
            _keys = list(_dtrend[itrm_key][0].keys())
            _dan_key = {key:[] for key in _keys}
            for item_key in _keys:
                _dan_key[item_key]=[_dtrend[itrm_key][i][item_key] for i in range(len(_dtrend[itrm_key]))]
                kkkk=1
            _dtrend[itrm_key] = _dan_key
        return _dtrend

#


'''
    _count = len(z)
    xx=np.zeros(_count)
    P = np.zeros(_count)
    Ndisp=60*2
    disper = np.zeros(Ndisp).tolist()
    enx =  np.zeros(Ndisp).tolist()
    xx[0]=z[0]
    P[0]=1
    r=1 #0.999
    en=0.1
#    dNoise=12
    r2=r*r
    en2=en*en
    DP=np.zeros(_count)
    DM=np.zeros(_count)
    print(' Расчет  !!!')
    for i in range(1, _count):
        disper.pop(0)
        disper.append(z[i-1])
#        dNoise = np.var(disper)
        dNoise = np.std(disper)
        enx.pop(0)
        enx.append(xx[i-1])
        f0 = lambda x, y: x-y
        lsx = list(map(f0,disper, enx))
        en=np.std(lsx)

        # en=np.var(enx)

        Pe=r2*P[i-1]+en*en
        P[i] = (Pe*dNoise)/(Pe+dNoise)
        xx[i]=r*xx[i-1]+P[i]/dNoise*(z[i]-r*xx[i-1])
        DP[i]=xx[i]+en*0.7
        DM[i]=xx[i]-en*0.7


        # Pe=r2*P[i-1]+en2
        # P[i] = (Pe*dNoise)/(Pe+dNoise)
        # xx[i]=r*xx[i-1]+P[i]/dNoise*(z[i]-r*xx[i-1])



'''
