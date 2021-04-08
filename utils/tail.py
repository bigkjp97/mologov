import time
from prometheus_client import Gauge, push_to_gateway, CollectorRegistry, start_http_server, instance_ip_grouping_key


class Tail():
    def __init__(self, file, job, keywords, label, pushHost, hostName):
        self.file = file
        self.job = job
        self.keywords = keywords
        self.labelName = label
        self.pushHost = pushHost
        self.hostName = hostName
        self.reg = CollectorRegistry()
        self.count = Gauge('keywords_count', 'Count keywords from log', ['keyword', 'instance'], registry=self.reg)

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
        instance_ip_grouping_key()
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
                            self.count.labels(keyword=arrLabel[arrKeywords.index(keyword)],
                                              instance=self.hostName).inc()
                            push_to_gateway(self.pushHost, job=jobName, registry=self.reg)
                            # print(self.count)
