# mologov🚀

Mologov(`log-monit`) is made to monitor logs.

#### unzip and start

```shell
tar xzvf log-monit-linux-amd64.tar.gz
# If init.yml is in the same directory
./mologov
# or use this way to start process
./mologov -f init.yml
```

#### start with shell script `monit.sh`

```shell
chmod +x monit.sh
# start
./monit.sh start
```

### Function

Tail and count the keywords which matched in logs, some new functions will be updated when need👶...

### Configure

#### *init.yml*

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



