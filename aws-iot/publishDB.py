SeSenimport os
import sys
import AWSIoTPythonSDK
sys.path.insert(0, os.path.dirname(AWSIoTPythonSDK.__file__))

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

import logging
import time
import getopt
import datetime
import random
#--------------------


# Usage
usageInfo = """Usage:
Use certificate based mutual authentication:
python basicPubSub.py -e <endpoint> -r <rootCAFilePath> -c <certFilePath> -k <privateKeyFilePath>
Use MQTT over WebSocket:
python basicPubSub.py -e <endpoint> -r <rootCAFilePath> -w
Type "python basicPubSub.py -h" for available options.
"""
# Help info
helpInfo = """-e, --endpoint
    Your AWS IoT custom endpoint
-r, --rootCA
    Root CA file path
-c, --cert
    Certificate file path
-k, --key
    Private key file path
-w, --websocket
    Use MQTT over WebSocket
-h, --help
    Help information
"""

def configure():
    # Read in command-line parameters
    useWebsocket = False
    host = ""
    rootCAPath = ""
    certificatePath = ""
    privateKeyPath = ""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hwe:k:c:r:", ["help", "endpoint=", "key=","cert=","rootCA=", "websocket"])
        if len(opts) == 0:
            raise getopt.GetoptError("No input parameters!")
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                print(helpInfo)
                exit(0)
            if opt in ("-e", "--endpoint"):
                host = arg
            if opt in ("-r", "--rootCA"):
                rootCAPath = arg
            if opt in ("-c", "--cert"):
                certificatePath = arg
            if opt in ("-k", "--key"):
                privateKeyPath = arg
            if opt in ("-w", "--websocket"):
                useWebsocket = True
    except getopt.GetoptError:
        print(usageInfo)
        exit(1)

    # Missing configuration notification
    missingConfiguration = False
    if not host:
        print("Missing '-e' or '--endpoint'")
        missingConfiguration = True
    if not rootCAPath:
        print("Missing '-r' or '--rootCA'")
        missingConfiguration = True
    if not useWebsocket:
        if not certificatePath:
            print("Missing '-c' or '--cert'")
            missingConfiguration = True
        if not privateKeyPath:
            print("Missing '-k' or '--key'")
            missingConfiguration = True
    if missingConfiguration:
        exit(2)

    # Configure logging
    logger = None
    if sys.version_info[0] == 3:
        logger = logging.getLogger("core")  # Python 3
    else:
        logger = logging.getLogger("AWSIoTPythonSDK.core")  # Python 2
    logger.setLevel(logging.DEBUG)
    streamHandler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)

    # Init AWSIoTMQTTClient
    myAWSIoTMQTTClient = None
    myAWSIoTMQTTClient = AWSIoTMQTTClient("SensorData")
    myAWSIoTMQTTClient.configureEndpoint(host, 8883)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

    # AWSIoTMQTTClient connection configuration
    myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
    myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
    myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
    myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

def publish(devId, data):
    # Connect and subscribe to AWS IoT
    myAWSIoTMQTTClient.connect()
    # Publish to the topic in a loop
    topic = "SensorData"
    delay_s = 60

    try:
       
        timestamp = datetime.datetime.now()
        msg = '"Device": "{}", "Time": "{}", "Sound": "{}", "Co2": "{}", "Temperature": "{}", "voc": "{}", "Humidity": "{}", "Ambient Light": "{}", "Pressure": "{}", "UV Index": "{}"'.format(devId, timestamp, data['sound'], data['co2'], data['temperature'], data['voc'], data['humidity'], data['ambientLight'], data['pressure'], data['uvIndex'])
        msg = '{'+msg+'}'
        myAWSIoTMQTTClient.publish(topic, msg, 1)
        #print('Sleeping...')
        #time.sleep(delay_s)
    except KeyboardInterrupt:
        pass
        
    #myAWSIoTMQTTClient.disconnect()
    