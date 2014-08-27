## Usage
See `examples/`

## Examples

### mesos_ec2.py

```bash
mesos_ec2.py \
    --mesos-url http://mesos_master.local:5050 \
    --cpus 1,3 \
    --region us-west-2 \
    --asg mesos-MesosSlaveStack-1AB12345ABC-ServerGroup-789XYZ789 \
    --log-level info
```

```console
INFO:requests.packages.urllib3.connectionpool:Starting new HTTP connection (1): mesos_master.local
INFO:autoscale:State: {'mem_free': 6353, 'disk_free': 35703, 'cpus_free': 8.5}
INFO:autoscale:Thresholds: {'cpus': {'upper': 3, 'lower': 1}}
INFO:autoscale:Should scale by -1
Scaling mesos-MesosSlaveStack-1AB12345ABC-ServerGroup-789XYZ789 in us-west-2 by -1
INFO:autoscale:Current scale: 9
INFO:autoscale:Scaling to 8
```