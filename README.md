# log-monit

The log-monit is made for monitoring logs in our servers, this tool can push metrics to [Pushgateway](https://github.com/prometheus/pushgateway), then we can collect them with prometheus.

First of all, you need to download [Pushgateway](https://github.com/prometheus/pushgateway) and [Prometheus](https://github.com/prometheus/prometheus), start with

```shell
tar xzvf log-monit-linux-amd64.tar.gz
# If init.yml is in the same directory
./log-monit
# or use this way to start process
./log-monit -f init.yml
```

### Function

This consist of easy code :) I just count the keywords which matched in logs, I will figure some new functions when needed...

## init.yml

Initialize a configuration

```yaml
remote_push:
  # make sure you have started a pushgateway process
  host: 'localhost:9091'
config:
  # job name 
  - job: 'test1'
    # file location
    file: 'test1.log'
    # keywords you want to count
    keywords: [ 'test','hello world' ]
    # name label for each keyword
    label: [ 'test','hello' ]
  # add job like this
  - job: 'test2'
    file: 'test2.log'
    keywords: [ 'warning','error connection' ]
    label: [ 'warn','error' ]

```



