#!/usr/bin/python2
# -*- coding: utf-8 -*-
import boto3
region = 'eu-west-1'
instances = ['i-1234567890ABCDEF0']

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name=region)
    ec2.start_instances(InstanceIds=instances)
    print 'stopped your instances: ' + str(instances)
