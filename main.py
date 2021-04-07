import threading
import tail
import yaml
import argparse


def main():
    parser = argparse.ArgumentParser()
    # 设置传参方式
    parser.add_argument('-f', '--file', default='./init.yml')
    args = parser.parse_args()
    with open(args.file, 'r') as conf:
        config = yaml.load(conf, Loader=yaml.FullLoader)
    # print(config)
    pushHost = config['remote_push']['host']
    # 'config': [{'job': '', 'file': '', 'keyword': ['', ''], 'label': ['', '']}]
    cases = config['config']
    # threads = []

    for case in cases:
        file = case['file']
        job = case['job']
        keywords = case['keywords']
        label = case['label']
        # 开启多线程
        t = threading.Thread(target=tail.Tail(file, job, keywords, label, pushHost).tail)
        t.start()
        # threads.append(t)


if __name__ == '__main__':
    main()
