import time
import os

from prometheus_client import Gauge


# listen logs
class Tail():
    def __init__(self, file, keywords, label, matric, hostName):
        self._file = file
        self._keywords = keywords
        self._labelName = label
        self._hostName = hostName
        self._matric = matric
        self._count = Gauge('keywords_count_' + self._matric, 'Count keywords from log', ['keyword', 'instance'])

    # listen when keyword appears in log
    def tail_keywords(self):
        # move cursor after reading file
        file = self._file
        # print(file)
        # keywords need collect
        arrKeywords = self._keywords
        # labels match keywords
        arrLabel = self._labelName
        maxTry = 0
        while maxTry < 5:
            try:
                with open(file) as log:
                    maxTry = 0
                    while True:
                        # if log was cleaned, read from start
                        if os.path.getsize(file) == 0:
                            log.seek(0, 0)
                            # off this loop
                            # continue
                        where = log.tell()
                        line = log.readline()
                        # print(line)
                        if not line:
                            time.sleep(1)
                            # remain point last char
                            log.seek(where)
                        else:
                            for keyword in arrKeywords:
                                if keyword in line:
                                    self._count.labels(keyword=arrLabel[arrKeywords.index(keyword)],
                                                       instance=self._hostName).inc()
            except FileNotFoundError:
                maxTry += 1
                print("[MOLOGOV][ERROR] " + time.strftime("%Y-%m-%d %H:%M:%S",
                                                          time.localtime()) + " File " + file + " not found")
                time.sleep(600)

        print("[MOLOGOV][INFO] " + time.strftime("%Y-%m-%d %H:%M:%S",
                                                 time.localtime()) + " Stop monitoring " + file)
