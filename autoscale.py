#!/usr/bin/env python
import logging
import sys

import boto.ec2.autoscale
import requests


logger = logging.getLogger(__name__)


class MesosReporter():
    def __init__(self, mesos_url):
        self.mesos_url = mesos_url.rstrip('/')
        stats_url = '/'.join([self.mesos_url, '/stats.json'])
        self.state = requests.get(stats_url).json()

    @property
    def state(self):
        return self.state


class MesosDecider():
    def __init__(self, thresholds):
        self.thresholds = thresholds

    def should_scale(self, cluster):
        increment = 1
        decrement = -1

        cpus_free = cluster.state['cpus_total'] - cluster.state['cpus_used']
        disk_free = cluster.state['disk_total'] - cluster.state['disk_used']
        mem_free = cluster.state['mem_total'] - cluster.state['mem_used']
        logger.info('State: %s', dict(cpus_free=cpus_free, disk_free=disk_free, mem_free=mem_free))
        logger.info('Thresholds: %s', self.thresholds)

        if   (('cpus' in self.thresholds and cpus_free < self.thresholds['cpus']['lower']) or
              ('disk' in self.thresholds and disk_free < self.thresholds['disk']['lower']) or
              ('mem' in self.thresholds and mem_free < self.thresholds['mem']['lower'])):
            scale_by = increment
        elif (('cpus' in self.thresholds and cpus_free > self.thresholds['cpus']['upper']) or
              ('disk' in self.thresholds and disk_free > self.thresholds['disk']['upper']) or
              ('mem' in self.thresholds and mem_free > self.thresholds['mem']['upper'])):
            scale_by = decrement
        else:
            scale_by = 0

        logger.info('Should scale by %s', scale_by)
        return scale_by


class AwsAsgScaler():
    def __init__(self, region, asg_name, min_instances=1, max_instances=None, 
                 aws_access_key_id=None, aws_secret_access_key=None):
        self.region = region
        self.asg_name = asg_name
        self.min_instances = min_instances
        self.max_instances = max_instances
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key

    def _get_connection(self):
        if self.aws_access_key_id and self.aws_secret_access_key:
            return boto.ec2.autoscale.connect_to_region(
                self.region, 
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key)
        else:
            return boto.ec2.autoscale.connect_to_region(self.region)

    def scale(self, delta):
        c = self._get_connection()
        current_count = c.get_all_groups(names=[self.asg_name])[0].desired_capacity
        logger.info("Current scale: %s", current_count)
        new_count = current_count + delta
        
        if self.min_instances and new_count < self.min_instances:
            new_count = self.min_instances
        elif self.max_instances and new_count > self.max_instances:
            new_count = self.max_instances

        if new_count != current_count:
            logger.info("Scaling to %s", new_count)
            c.set_desired_capacity(self.asg_name, new_count)
