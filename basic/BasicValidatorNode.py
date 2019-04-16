
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
from pystemd.systemd1 import Unit
import time

# The unique hostname that &IoT; generated for 
# this device.
HOST_NAME = "yourhostname-ats.iot.us-east-1.amazonaws.com"

# The relative path to the correct root CA file for &IoT;, 
# which you have already saved onto this device.
ROOT_CA = "AmazonRootCA1.pem"

# The relative path to your private key file that 
# &IoT; generated for this device, which you 
# have already saved onto this device.
PRIVATE_KEY = "yourkeyid-private.pem.key"

# The relative path to your certificate file that 
# &IoT; generated for this device, which you 
# have already saved onto this device.
CERT_FILE = "yourkeyid-certificate.pem.crt.txt"

# A programmatic shadow handler name prefix.
SHADOW_HANDLER = "ValidatorNodeThing"

unit = Unit(b'polkadot-validator.service')
# Automatically called whenever the shadow is updated.
def myShadowUpdateCallback(payload, responseStatus, token):
  print()
  print('UPDATE: $aws/things/' + SHADOW_HANDLER + 
    '/shadow/update/#')
  print("payload = " + payload)
  print("responseStatus = " + responseStatus)
  print("token = " + token)

# Create, configure, and connect a shadow client.
shadowClient = AWSIoTMQTTShadowClient(SHADOW_HANDLER)
shadowClient.configureEndpoint(HOST_NAME, 8883)
shadowClient.configureCredentials(ROOT_CA, PRIVATE_KEY,
  CERT_FILE)
shadowClient.configureConnectDisconnectTimeout(10)
shadowClient.configureMQTTOperationTimeout(5)
shadowClient.connect()

# Create a programmatic representation of the shadow.
deviceShadow = shadowClient.createShadowHandlerWithName(SHADOW_HANDLER, True)

# Initialize
unit.load()
status = 'unknown'

# To stop running this script, press Ctrl+C.
while True:
  
  prevStatus = status
  status = unit.Unit.ActiveState.decode('utf-8')
  
  if prevStatus != status:
      msg = '{"state":{"reported":{"status":"%(data)s"}}}' % { 'data' : status}
  else:
      msg = '{"state":{"desired":{"status":"%(data)s"}}}' % { 'data' : prevStatus}

  deviceShadow.shadowUpdate(msg, myShadowUpdateCallback, 5)
  
  # Wait for this test value to be added.
  time.sleep(2)