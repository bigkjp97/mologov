import threading

from prometheus_client import start_http_server

from utils import tail
import yaml
import argparse
import socket


def main():
    parser = argparse.ArgumentParser()
    # system parameter
    parser.add_argument('-f', '--file', default='./init.yml')
    args = parser.parse_args()
    with open(args.file, 'r') as conf:
        config = yaml.load(conf, Loader=yaml.FullLoader)
    # print(config)
    pushHost = config['server']['host']
    pushPort = int(config['server']['port'])
    # 'config': [{'job': '', 'file': '', 'keyword': ['', ''], 'label': ['', '']}]
    cases = config['config']
    hostName = socket.gethostname()
    start_http_server(pushPort, pushHost)
    for case in cases:
        file = case['file']
        keywords = case['keywords']
        label = case['label']
        matric = case['matric']
        print(case)
        # use multiple threads
        t = threading.Thread(target=tail.Tail(file, keywords, label, matric, hostName).tail_keywords)
        t.start()


if __name__ == '__main__':
    main()
