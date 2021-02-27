from kubernetes import client, config
import os
import sys
import logging
config.load_incluster_config()
# target namespace
TARGET_NAMESPACE = ''
SOURCE_SECRET_NAME = ''
DEST_SECRET_LIST = ['', '']
SOURCE_NAMESPACE_LIST = ['', '']
v1 = client.CoreV1Api()
#######################################
### Logging Settings ##################
#######################################

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def CheckIfSecretExistInSource(SOURCE_SECRET_NAME, SOURCE_NAMESPACE):
    try:
        READ_SECRET_SOURCE = v1.read_namespaced_secret(SOURCE_SECRET_NAME, SOURCE_NAMESPACE)
        return True
    except:
        logger.warning('Secret not exist in source namespace, please verify')
        return False
def CheckIfSecretExistInDest(SOURCE_NAMESPACE, TARGET_NAMESPACE):
    try:
        READ_SECRET_DEST = v1.read_namespaced_secret(SOURCE_NAMESPACE.replace('service', 'db'), TARGET_NAMESPACE)
        return True
    except:
        logger.warning('Secret not exist in destination namespace, Creating now...')
        return False

for SOURCE_NAMESPACE in SOURCE_NAMESPACE_LIST:
    try:
        ##Checking Secret exist in Source namespace
        if CheckIfSecretExistInSource(SOURCE_SECRET_NAME, SOURCE_NAMESPACE):
            ## reading secret from source namespace
            READ_SECRET_SOURCE = v1.read_namespaced_secret(SOURCE_SECRET_NAME, SOURCE_NAMESPACE)
            body = client.V1Secret(kind=READ_SECRET_SOURCE.kind, metadata=dict(name=SOURCE_NAMESPACE.replace('service', 'db'), namespace=TARGET_NAMESPACE), api_version=READ_SECRET_SOURCE.api_version, data=READ_SECRET_SOURCE.data)
            ##Checking Secret exist in Destination namespace
            if CheckIfSecretExistInDest(SOURCE_NAMESPACE, TARGET_NAMESPACE):
                ## reading secret from destination namespace
                READ_SECRET_DEST = v1.read_namespaced_secret(SOURCE_NAMESPACE.replace('service', 'db'), TARGET_NAMESPACE)
                body = client.V1Secret(kind=READ_SECRET_SOURCE.kind, metadata=dict(name=SOURCE_NAMESPACE.replace('service', 'db'), namespace=TARGET_NAMESPACE), api_version=READ_SECRET_SOURCE.api_version, data=READ_SECRET_SOURCE.data)
                ## replacing existing Secret in Destination with updated Source Secret
                REPLACING_SECRET = v1.replace_namespaced_secret(READ_SECRET_DEST.metadata.name, TARGET_NAMESPACE, body)
            else:
                #creating secret in Target Namespace
                CREATE_SECRET = v1.create_namespaced_secret(TARGET_NAMESPACE, body)
        else:
            logger.error('Secret not exist in source namespace, please verify source namespace has database-secret')
    except:
        print('exception')
        continue