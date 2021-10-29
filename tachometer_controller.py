# HTTP request fogadásáért felel, illetve feldolgozásáért, felparseolásáért, service hivásáért

from logger import LOG
from flask import Blueprint, request, Response
import tachometer_service as service
import json

tachometer_api = Blueprint('tachometer', __name__, url_prefix='/tachometer')


@tachometer_api.route('/', methods=['POST'])  # POST -ra hallgat
def create_route_record():
    # Parse Input
    LOG.debug(f'{__name__} Request Received: {request.get_json()}')
    data = request.get_json()  # elkérjük a bodyt, megkapjuk a datat
    # Validate Input #kötelező valid
    if 'driver' not in data or 'vehicle' not in data or 'start' not in data or 'speed' not in data:
        LOG.error(f'Bad Request: {data}')
        return Response('Problem', status=400)

    # Call Service
    result = service.record_route(data['driver'], data['vehicle'], data['start'], data['speed'])

    # Serialize Result
    return Response(result, status=200)


@tachometer_api.route('/drivers', methods=['GET'])  # GET -re hallgat
def read_drivers():
    return {
        'drivers': service.read_drivers()
    }


@tachometer_api.route('/drivers/<driver>', methods=['GET']) #driver : str driver> ugyanannak kell lennie
def read_vechiles_of_driver(driver: str):
    return {
        'vehicles': service.read_vehicles_of_driver(driver)
    }


@tachometer_api.route('/', methods=['GET'])
def report_route():
    LOG.debug(request.args)
    driver = request.args.get('driver')
    vehicle = request.args.get('vehicle')
    error = []  # üres tömb
    if not driver:
        error.append('driver')
    if not vehicle:
        error.append('vehicle')
    if len(error) != 0: # ha errornak a hossza nem 0, akkor
        return Response(json.dumps({
            'msg': 'Problem, Missing Parameter',
            'error': error
        }), status=400)
    return {
        'routes': service.read_routes_of_driver_on_vehicle(driver, vehicle)
    }
