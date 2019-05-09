#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##################################################
## A serverless failover solution for Web3 validator nodes
##################################################
## Author: Ricardo Rius
## Copyright: Copyright 2019, Ricardo Rius
## License: Apache-2.0
## Version: 0.1.3
##################################################

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
from pystemd.systemd1 import Unit
from PyInquirer import prompt
import time, sys

def getConfigParameters():
  questions = [
      {
          'type': 'input',
          'name': 'host_name',
          'message': 'The unique HOSTNAME that AWS IoT; generated for this device: ',
      },
      {
          'type': 'input',
          'name': 'root_ca',
          'message': 'Path to the correct ROOT CA file for AWS IoT:',
      },
      {
          'type': 'input',
          'name': 'private_key',
          'message': 'Path to your PRIVATE KEY file:',
      },
      {
          'type': 'input',
          'name': 'cert_file',
          'message': 'Path to your CERTIFICATE FILE:',
      },
      {
          'type': 'input',
          'name': 'name',
          'message': 'The name of the AWS IOT Thing:',
          'default': 'ValidatorNode',
      },
  ]
  return prompt(questions)

def setClient(answers):
  try:
    shadowClient = AWSIoTMQTTShadowClient(answers['name']+"Thing")
    shadowClient.configureCredentials(answers['root_ca'], answers['private_key'], answers['cert_file'])
  except FileNotFoundError as fnf_error:
    print('File not found.',fnf_error)
  else: 
    try:
      shadowClient.configureEndpoint(answers['host_name'], 8883)
      shadowClient.configureConnectDisconnectTimeout(10)
      shadowClient.configureMQTTOperationTimeout(5)
      shadowClient.connect()
      # Create a programmatic representation of the shadow.
      return shadowClient.createShadowHandlerWithName(answers['name']+"Thing", True)
    except AssertionError as error:
      print(error)

def myShadowUpdateCallback(payload, responseStatus, token):
  print()
  print('UPDATE: $aws/things/' + 'myThing' +'/shadow/update/#')
  print("payload = " + payload)
  print("responseStatus = " + responseStatus)
  print("token = " + token)


def main():

  # Initialize, 3 attempts
  for i in range(3):
    try:
      answers = getConfigParameters()
      deviceShadow = setClient(answers)
    except OSError as os_error:
      print(os_error)
    else:
      break
    
  unit = Unit(b'polkadot-validator.service')
  unit.load()
  status = 'unknown'

  # To stop running this script, press Ctrl+C.
  while True:
    prev_status = status
    status = unit.Unit.ActiveState.decode('utf-8')
    
    try:
      if prev_status != status:
        msg = '{"state":{"reported":{"status":"%(data)s"}}}' % { 'data' : status}
        deviceShadow.shadowUpdate(msg, myShadowUpdateCallback, 5)
      else:
        msg = '{"state":{"desired":{"status":"%(data)s"}}}' % { 'data' : prev_status}
        # Uncomment next line if you want to send AWS IOT desired status to enable deltas.
        #deviceShadow.shadowUpdate(msg, myShadowUpdateCallback, 5) 
    except:
      break

    # Polling wait time [sec]
    time.sleep(.5)

if __name__ == '__main__':
  main()