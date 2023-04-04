from datetime import datetime, date

class TDateTimeNew:
    def __init__(self, *args, **kwargs):
        print('__ TDateTime __')
        self.timeframe = kwargs.get('timeframe', "x")
        self.id = kwargs.get('id', [])
        self.datetime = kwargs.get('datetime', [])
        self.dt0, self.dt1 = None, None
        if len(self.id)==0 or len(self.datetime)==0:
            return
        self.dt0, self.dt1 = self.datetime[0], self.datetime[len(self.datetime)-1]
        # self.args = args
        # self.kwargs = kwargs


    def __str__(self) -> str:  # Для наглядности print'а
        return "I am {}\nMy param1 is {}\nParam2 is {}\nargs is {}   kwargs-()".format(
            self.__class__,
            self.timeframe,
            self.id,
            self.datetime,
            # self.args,
            # self.kwargs
        )
    #
    # def __getstate__(self) -> dict:  # Как мы будем "сохранять" класс
    #     kk=1
    #     state = {}
    # #     state["timeframe"] = self.timeframe
    # #     state["id"] = self.id
    # #     state["datetime"] = self.datetime
    # #     # state["args"] = self.args
    # #     # state["kwargs"] = self.kwargs
    #     return state
    # #
    # def __setstate__(self, state: dict):  # Как мы будем восстанавливать класс из байтов
    #     k=1
    # #     # self.timeframe = state["timeframe"]
    # #     # self.id = state["id"]
    # #     # self.datetime = state["datetime"]
    # #
    # #     # self.args = state["args"]
    # #     # self.kwargs = state["kwargs"]
