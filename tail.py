import time
from prometheus_client import Gauge, push_to_gateway, CollectorRegistry


class Tail():
    def __init__(self, file, job, keywords, label, pushHost):
        self.file = file
        self.job = job
        self.keywords = keywords
        self.labelTag = 'keyword'
        self.labelName = label
        self.matrixName = 'keywords_count'
        self.description = 'Count keywords from log'
        self.pushHost = pushHost
        self.reg = CollectorRegistry()
        self.count = Gauge(self.matrixName, self.description, [self.labelTag], registry=self.reg)

    # 多线程去跑
    def tail(self):
        # register = CollectorRegistry()
        # count = Gauge('words_count', 'Count keywords from log', ['keyword'],
        #               registry=register)
        # 利用File的特性，读一个字节移动一个数据
        file = self.file
        # print(file)
        # 文件地址所在数组的下标
        arrIndex = self.file.index(file)
        # 不同日志的采集当对应不同的job名
        jobName = self.job
        # 该文件所需采集的关键词
        arrKeywords = self.keywords
        # 该关键词对应的标签名
        arrLabel = self.labelName
        with open(file) as log:
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
                    for keyword in arrKeywords:
                        if keyword in line:
                            self.count.labels(arrLabel[arrKeywords.index(keyword)]).inc()
                            push_to_gateway(self.pushHost, job=jobName, registry=self.reg)
                            # print(self.count)
