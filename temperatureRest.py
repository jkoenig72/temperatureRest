from flask import Flask

import glob
import time

app = Flask(__name__)

path = "/sys/bus/w1/devices/"
sensor_path = glob.glob(path + "28*")[0]
sensor_data_path = sensor_path + "/w1_slave"

def read_temperature():
    file = open(sensor_data_path, "r")
    rows = file.readlines()
    file.close()
    return rows

def get_temperature_in_degree():
    rows = read_temperature()
    while rows[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        rows = read_temperature()
    equals_pos = rows[1].find('t=')
    if equals_pos != -1:
        temp_string = rows[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

@app.route('/temperature', methods=['GET'])
def get_temperature():
    return {'temperature': get_temperature_in_degree()}

if __name__ == '__main__':
    app.run()
