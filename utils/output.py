import time


class Output:
    def __init__(self, tag, statement):
        self._time = time.strftime("%Y-%m-%d %H:%M:%S ",
                                   time.localtime())
        self._statement = statement
        self._tag = tag

        print("[MOLOGOV][" + self._tag + "] " + self._time + self._statement)


