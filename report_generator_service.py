from logger import LOG
import multiprocessing
import time
import json
import numpy as np

REPORT_GENERATION_QUEUE = multiprocessing.Queue()
REPORT_SAMPLING_INTERVAL = 10

def shcedule_report_generation():
    while True:
        while REPORT_GENERATION_QUEUE.empty() == False:
            route_file_path = REPORT_GENERATION_QUEUE.get()
            route = {}
            with open(route_file_path, 'r') as route_file:
                route = json.load(route_file)
            speed = route['speed']
            statistics = {
                'min': float(np.min(speed)),
                'max': float(np.max(speed)),
                'avg': float(np.mean(speed)),
                'std': float(np.std(speed))
            }
            route['distance'] = round(np.trapz(route['speed'], dx=1.0/3600.0),4)
            route['statistics'] = statistics
            LOG.debug(route)
            with open(route_file_path, 'w') as output:
                output.write(json.dumps(route))
            LOG.info(f'{route_file}')
        LOG.debug(f'Report Queue is Empty')
        time.sleep(REPORT_SAMPLING_INTERVAL)