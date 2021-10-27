import sys
import logging

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(
    filename='tachometer.log',
    filemode='w',
    format=LOG_FORMAT,
    level=logging.DEBUG
)
LOG = logging.getLogger()
LOG.addHandler(logging.StreamHandler(stream=sys.stdout))