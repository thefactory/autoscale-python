# autoscale

## Overview

`autoscale` is a Python library for composable autoscaling functionality.

Autoscaling is built up from three primitives:
* **Reporters** convey the state of the world. Cluster size, request latency, free resources, etc.
* **Deciders** hold business logic. They evaluate the state of a Reporter to make a scaling decision
* **Scalers** are the doers. They perform scale-up and scale-down actions on AWS, GCE, or your custom infrastructure

## Installation

Straight from the cheeseshop:
```python
pip install autoscale
```

## Usage

### Writing your own Reporter/Decider/Scaler
See [autoscale.py](https://github.com/thefactory/autoscale-python/blob/master/autoscale.py)

### Writing an autoscaling script
See [examples/](https://github.com/thefactory/autoscale-python/tree/master/examples)

## Examples

### mesos_ec2.py
```console
$ mesos_ec2.py --help
usage: mesos_ec2.py [-h] [-l LOG_LEVEL] -u MESOS_URL [-c CPUS] [-d DISK]
                    [-m MEM] -r REGION -a ASG

optional arguments:
  -h, --help            show this help message and exit
  -l LOG_LEVEL, --log-level LOG_LEVEL
                        Log level (debug, [default] info, warn, error)
  -u MESOS_URL, --mesos-url MESOS_URL
                        Mesos cluster URL
  -c CPUS, --cpus CPUS  Comma-delimited CPU thresholds (lower,upper)
  -d DISK, --disk DISK  Comma-delimited disk thresholds (lower,upper)
  -m MEM, --mem MEM     Comma-delimited memory thresholds (lower,upper)
  -r REGION, --region REGION
                        AWS region
  -a ASG, --asg ASG     AWS auto scaling group name

$ mesos_ec2.py \
    --mesos-url http://mesos_master.local:5050 \
    --cpus 1,3 \
    --region us-west-2 \
    --asg mesos-MesosSlaveStack-1AB12345ABC-ServerGroup-789XYZ789 \
    --log-level info
INFO:requests.packages.urllib3.connectionpool:Starting new HTTP connection (1): mesos_master.local
INFO:autoscale:State: {'mem_free': 6353, 'disk_free': 35703, 'cpus_free': 8.5}
INFO:autoscale:Thresholds: {'cpus': {'upper': 3, 'lower': 1}}
INFO:autoscale:Should scale by -1
Scaling mesos-MesosSlaveStack-1AB12345ABC-ServerGroup-789XYZ789 in us-west-2 by -1
INFO:autoscale:Current scale: 9
INFO:autoscale:Scaling to 8
```