import sys
import time
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
    pushPort = config['server']['port']
    # 'config': [{'job': '', 'file': '', 'keyword': ['', ''], 'label': ['', '']}]
    cases = config['config']
    hostName = socket.gethostname()
    print("[MOLOGOV][INFO] " + time.strftime("%Y-%m-%d %H:%M:%S",
                                       time.localtime()) + " Start - " + pushHost + ":" + pushPort)
    try:
        start_http_server(int(pushPort), pushHost)
    except:
        print("[MOLOGOV][ERROR] " + time.strftime("%Y-%m-%d %H:%M:%S",
                                                  time.localtime()) + " Bad server " + pushHost + ":" + pushPort)
        sys.exit(1)

    print("[MOLOGOV][INFO] " + time.strftime("%Y-%m-%d %H:%M:%S",
                                       time.localtime()) + " Start successfully " + pushHost + ":" + pushPort)

    for case in cases:
        file = case['file']
        keywords = case['keywords']
        label = case['label']
        matric = case['matric']
        print("[MOLOGOV][INFO] " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " Monitoring " + file)
        # use multiple threads
        t = threading.Thread(target=tail.Tail(file, keywords, label, matric, hostName).tail_keywords)
        t.start()


if __name__ == '__main__':
    main()
