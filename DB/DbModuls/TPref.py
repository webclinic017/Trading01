from PSQLCommand import PSQLCommand

class TPref(PSQLCommand):
  def __init__(self, *args, **kwargs):
    PSQLCommand.__init__(self, *args, **kwargs)
    self._pref = "pref"

    self.__setattr__('prefname', dict())

    if not (self.is_tabl(self._pref)):
      self.fcommand_execute(f"CREATE TABLE pref (id SERIAL PRIMARY KEY, name  TEXT UNIQUE);")
    else:
      self._getDb()

    _time = args[0].get('timeframe', None)
    if _time is None:
      self.__set_attr({'timeframeName': "", 'timeframeid': -1})
    else:
      self.__set_attr({'timeframeName': _time, 'timeframeid': self.get_index(_time)})

  def __set_attr(self, d0:dict):
    for key, val in d0.items():
      self.__setattr__(key, val)


  def _getDb(self):
    _z = self.fcommand_fetchall("SELECT name, id FROM pref;")
    if _z is None:
      self.__set_attr({'prefname': dict(), 'prefid': dict()})
      return
    self.__set_attr({'prefname': {x[0]: x[1] for x in _z}, 'prefid': {x[1]: x[0] for x in _z}})

  def _insert(self, name):
    self.fcommand_execute(f'INSERT INTO pref (name) VALUES(\'{name}\');')
    self._getDb()

  def get_index(self, name):
    try:
      return self.__getattribute__('prefname')[name]
    except:
      self._insert(name)
      id = self.__getattribute__('prefname')[name]
    return id

  def get_name(self, id: int):
    try:
      return self.__getattribute__('prefid')[id]
    except:
      pass
    return None

  def set_index(self, name):
    try:
      id = self.__getattribute__('prefname')[name]
      self.__set_attr({'timeframeName': name, 'timeframeid': id})
    except:
      id = self.get_index(name)
      self.__set_attr({'timeframeName': name, 'timeframeid': id})

