from typing import List
from logger import LOG
import os
import json
from report_generator_service import REPORT_GENERATION_QUEUE

DATA_DIR = os.path.join(os.getcwd(), 'data')


def get_save_directory(driver: str, vehicle: str) -> str:
    if not os.path.exists(DATA_DIR):
        LOG.info(f'Create Directory {DATA_DIR}')
        os.mkdir(DATA_DIR)
    driver_dir = os.path.join(DATA_DIR, driver.replace(' ','_'))
    if not os.path.exists(driver_dir):
        LOG.info(f'Create Directory {driver_dir}')
        os.mkdir(driver_dir)
    vehicle_dir = os.path.join(driver_dir, vehicle)
    if not os.path.exists(vehicle_dir):
        LOG.info(f'Create Directory {vehicle_dir}')
        os.mkdir(vehicle_dir)
    return vehicle_dir


def record_route(driver : str, vehicle: str, start: str, speed: List[int]):
    save_dir = get_save_directory(driver, vehicle)
    LOG.debug(f'Save Directory: {save_dir}')
    save_filename = start.replace(' ','_') + '.json'
    save_file_absolute_path = os.path.join(save_dir, save_filename)
    with open(save_file_absolute_path, 'w') as output:
        data = {
            'driver': driver,
            'vehicle': vehicle,
            'start': start,
            'speed': speed
        }
        output.write(json.dumps(data))
        REPORT_GENERATION_QUEUE.put(save_file_absolute_path)
    return f'Hello {driver}'

def read_drivers() -> List[str]:
   return os.listdir(DATA_DIR)

def read_vehicles_of_driver(driver: str) -> List[str]:
    return os.listdir(os.path.join(DATA_DIR, driver))

def read_routes_of_driver_on_vehicle(driver: str, vehicle: str):
    save_dir = get_save_directory(driver,vehicle)
    result = []
    for route_file in os.listdir(save_dir):
        with open(os.path.join(save_dir,route_file), 'r') as route:
            LOG.debug(route)
            content = json.load(route)
            LOG.debug(content)
            result.append(content)
    return result