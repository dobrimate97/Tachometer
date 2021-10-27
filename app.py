import os
from flask import Flask
import report_generator_service

from tachometer_controller import tachometer_api

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    print('Hello')

    REPORT_GENERATOR_PID = os.fork()
    if REPORT_GENERATOR_PID == 0:
        report_generator_service.shcedule_report_generation()
        exit(0)

    print(tachometer_api)
    app.register_blueprint(tachometer_api)

    app.run(host='0.0.0.0', port=5000, debug=True)