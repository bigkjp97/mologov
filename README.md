# mologov🚀

The mologov(`log-monit`) is made for monitoring logs in our servers.

First of all, you need to download [Pushgateway](https://github.com/prometheus/pushgateway) `not necessary after v1.3`and [Prometheus](https://github.com/prometheus/prometheus), start with

```shell
tar xzvf log-monit-linux-amd64.tar.gz
# If init.yml is in the same directory
./mologov
# or use this way to start process
./mologov -f init.yml
```

### Function

This consist of easy code :), thanks to `prometheus-client` I just count the keywords which matched in logs, I will figure some new functions when needed...

## init.yml

Initialize a configuration

```yaml
server:
  # make sure you have started a pushgateway process
  host: 'localhost'
  port: '9092'
config:
    # file location
  - file: './test.log'
    # keyword_count_test
    matric: 'test'
    # keywords you want to count
    keywords: [ 'error1','error2' ]
    # name label for each keyword
    label: [ 'err1','err2' ]
    # add more

  - file: './hello.log'
    matric: 'hello'
    keywords: [ 'error3','error4' ]
    label: [ 'err3','err4' ]
```



