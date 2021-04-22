import time
import os

from prometheus_client import Gauge
from utils.output import Output


# listen logs
class Tail:
    def __init__(self,
                 file,
                 keywords,
                 label,
                 matric,
                 hostName):
        self._file = file
        self._keywords = keywords
        self._labelName = label
        self._hostName = hostName
        self._matric = matric
        self._maxTry = 0
        self._count = Gauge('keywords_count_' + self._matric, 'Count keywords from log', ['keyword', 'instance'])

    def start_tail(self):
        """Try tailing logs,
        move cursor after reading file
        """
        file = self._file

        while self._maxTry < 5:
            try:
                self.do_tail()
            except FileNotFoundError:
                self._maxTry += 1
                Output("ERROR", "File " + file + " not found")
                time.sleep(10)
        Output("INFO", "Stop monitoring " + file)

    def do_tail(self):
        """Do tailing logs"""

        with open(self._file) as log:
            self._maxTry = 0
            while True:
                # if log was cleaned, read from start
                if os.path.getsize(self._file) == 0:
                    log.seek(0, 0)
                    # off this loop
                where = log.tell()
                line = log.readline()
                if not line:
                    time.sleep(1)
                    # remain point last char
                    log.seek(where)
                else:
                    self._inc(line)

    def _inc(self, line):
        """Increase when keyword in line"""

        for keyword in self._keywords:
            if keyword in line:
                self._count.labels(keyword=self._labelName[self._keywords.index(keyword)],
                                   instance=self._hostName).inc()
