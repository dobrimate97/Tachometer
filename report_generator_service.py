
# Üzleti logikát valósitja meg

from logger import LOG
import multiprocessing
import time
import json
import numpy as np

REPORT_GENERATION_QUEUE = multiprocessing.Queue()
REPORT_SAMPLING_INTERVAL = 10


def shcedule_report_generation():
    while True: # Végtelen ciklus
        while REPORT_GENERATION_QUEUE.empty() == False: # queue nem üres
            route_file_path = REPORT_GENERATION_QUEUE.get() # kiveszünk valamit a queue -ból
            route = {}
            with open(route_file_path, 'r') as route_file:
                route = json.load(route_file)
            speed = route['speed'] # kivesszük a speed -et
            statistics = {
                'min': float(np.min(speed)),
                'max': float(np.max(speed)),
                'avg': float(np.mean(speed)),
                'std': float(np.std(speed))
            }
            route['distance'] = round(np.trapz(route['speed'], dx=1.0 / 3600.0), 4) # megtett utat számoljuk ki
            route['statistics'] = statistics
            LOG.debug(route)
            with open(route_file_path, 'w') as output:
                output.write(json.dumps(route)) # visszairjuk a route -ot a fájlba
            LOG.info(f'{route_file}')
        LOG.debug(f'Report Queue is Empty') # ha véget ért a ciklus, üres a queue akkor szólunk hogy az üres
        time.sleep(REPORT_SAMPLING_INTERVAL)
