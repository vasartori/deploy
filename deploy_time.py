import datetime

import os
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/deploy/<component>', methods=['POST'])
def register_deploy(component):
    c = request.json
    c['date'] = str(datetime.datetime.now())
    c['component'] = component
    if "version" in c and "user" in c and "status" in c:
        if c['status'] == "OK" or c['status'] == "NOK":
            try:
                store_data(c)
                return jsonify({"status": "OK"}), 200
            except BaseException as e:
                return jsonify({"status": "Fail", "message": "{}"
                               .format(e)}), 422
        else:
            return jsonify({"status": "Fail", "message": "Invalid Status"}), 422
    else:
        return jsonify({"status": "Fail", "message": "Missing Fields"}), 422


def store_data(deploy_data):
    try:
        path = create_directory_structure(component=deploy_data['component'])
    except BaseException as e:
        raise Exception("{}".format(e))

    with open('/'.join([path, 'deploy.csv']), 'a+') as csvfile:
        w = ','.join([deploy_data['date'], deploy_data['component'],
                      deploy_data['version'], deploy_data['user'],
                      deploy_data['status']])
        try:
            csvfile.write('\n'.join([w, '']))
            csvfile.flush()
        except BaseException as e:
            raise Exception("{}".format(e))


def create_directory_structure(component):
    date = datetime.datetime.now()
    deploy_dir = os.getenv("DEPLOY_DATA", "/tmp")
    path = '/'.join([deploy_dir, str(component), str(date.year),
                     str(date.month), str(date.day)])

    if not os.path.exists(path):
        try:
            os.makedirs(path, exist_ok=True)
        except BaseException as e:
            raise Exception("{}".format(e))
    return path


if __name__ == '__main__':
    app.run()
