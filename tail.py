import time
from prometheus_client import Gauge, push_to_gateway, CollectorRegistry
import sys


class Tail():
    def __init__(self):
        self.keyword = "warning"
        self.reg = CollectorRegistry()
        self.count = Gauge('words_count', 'Count keywords from log', ['keyword'], registry=self.reg)

    def tail(self):
        # register = CollectorRegistry()
        # count = Gauge('words_count', 'Count keywords from log', ['keyword'],
        #               registry=register)
        # 利用File的特性，读一个字节移动一个数据
        with open("./hello.log") as log:
            while True:
                # 返回文件当前位置，即文件指针当前位置
                # 与readline()配合，readline()则按一句一句读
                where = log.tell()
                line = log.readline()
                # print(line)
                # 如果不是句子，则seek
                if not line:
                    time.sleep(1)
                    # 保持指针移动到最后一个字节
                    log.seek(where)
                else:
                    if self.keyword in line:
                        self.count.labels('warning').inc()
                        push_to_gateway('192.168.1.1:9091', job='warn', registry=self.reg)
                        print(self.count)


if __name__ == '__main__':
    t = Tail()
    t.tail()