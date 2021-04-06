import time
from prometheus_client import Gauge, push_to_gateway, CollectorRegistry
import sys


class Tail():
    def __init__(self):
        self.keyword = 'warning'
        self.job = 'warn'
        self.labelTag = 'keyword'
        self.labelName = ['warning']
        self.matrixName = 'keywords_count'
        self.description = 'Count keywords from log'
        self.pushHost = '192.168.1.1:9091'
        self.reg = CollectorRegistry()
        self.count = Gauge(self.matrixName, self.description, [self.labelTag], registry=self.reg)

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
                        self.count.labels(self.labelName[0]).inc()
                        push_to_gateway(self.pushHost, job=self.job, registry=self.reg)
                        print(self.count)


if __name__ == '__main__':
    t = Tail()
    t.tail()
