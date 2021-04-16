import threading

from prometheus_client import start_http_server

from utils import tail
import yaml
import argparse
import socket


def main():
    parser = argparse.ArgumentParser()
    # 设置传参方式
    parser.add_argument('-f', '--file', default='./init.yml')
    args = parser.parse_args()
    with open(args.file, 'r') as conf:
        config = yaml.load(conf, Loader=yaml.FullLoader)
    # print(config)
    pushHost = config['remote_push']['host']
    pushPort = int(config['remote_push']['port'])
    # 'config': [{'job': '', 'file': '', 'keyword': ['', ''], 'label': ['', '']}]
    cases = config['config']
    hostName = socket.gethostname()
    # threads = []
    start_http_server(pushPort, pushHost)
    for case in cases:
        file = case['file']
        keywords = case['keywords']
        label = case['label']
        # 开启多线程
        t = threading.Thread(target=tail.Tail(file, keywords, label, hostName).tail_keywords())
        t.start()
        # threads.append(t)


if __name__ == '__main__':
    main()
