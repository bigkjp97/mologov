import sys
import threading
from utils.too import Tail, Output
from prometheus_client import start_http_server

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
    pushPort = config['server']['port']
    # 'config': [{'job': '', 'file': '', 'keyword': ['', ''], 'label': ['', '']}]
    cases = config['config']
    hostName = socket.gethostname()
    Output("INFO", "Launch your little logs assistant :-)")
    try:
        start_http_server(int(pushPort), pushHost)
    except:
        Output("ERROR", "Bad server " + pushHost + ":" + pushPort)
        sys.exit(1)

    Output("INFO", "Start successfully with " + pushHost + ":" + pushPort)

    for case in cases:
        file = case['file']
        keywords = case['keywords']
        label = case['label']
        matric = case['matric']
        Output("INFO", "Monitoring " + file)
        # use multiple threads
        tail = Tail(file, keywords, label, matric, hostName)
        o = threading.Thread(target=tail.start_tail)
        o.start()


if __name__ == '__main__':
    main()
