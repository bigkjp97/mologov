import time
import os

from prometheus_client import Gauge


# 监听日志方案
class Tail():
    def __init__(self, file, keywords, label, hostName):
        self.file = file
        self.keywords = keywords
        self.labelName = label
        self.hostName = hostName
        self.count = Gauge('keywords_count', 'Count keywords from log', ['keyword', 'instance'])

    # 多线程去跑
    # 监听计数新出现的keywords
    def tail_keywords(self):
        # register = CollectorRegistry()
        # count = Gauge('words_count', 'Count keywords from log', ['keyword'],
        #               registry=register)
        # 利用File的特性，读一个字节移动一个数据
        file = self.file
        # print(file)
        # 该文件所需采集的关键词
        arrKeywords = self.keywords
        # 该关键词对应的标签名
        arrLabel = self.labelName
        with open(file) as log:
            while True:
                # 如果日志清空，则从头读起
                if os.path.getsize(file) == 0:
                    log.seek(0, 0)
                    # 跳出当前循环
                    # continue
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
                    for keyword in arrKeywords:
                        if keyword in line:
                            self.count.labels(keyword=arrLabel[arrKeywords.index(keyword)],
                                              instance=self.hostName).inc()

