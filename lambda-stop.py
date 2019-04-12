#!/usr/bin/python2
# -*- coding: utf-8 -*-
import boto3
region = 'eu-west-1'
instances = ['i-1234567890ABCDEF0']

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name=region)
    ec2.stop_instances(InstanceIds=instances)
    print 'started your instances: ' + str(instances)

