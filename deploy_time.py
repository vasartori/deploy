import datetime

import os

from flask import Flask, request, jsonify, send_file, render_template

app = Flask(__name__)

BASE_DIR = os.getenv("BASE_DIR", "/data")
BIND_ADDR = os.getenv("BIND_ADDR", "0.0.0.0")
PORT = os.getenv("PORT", "5000")


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


@app.route('/browse/', defaults={'rpath': ''})
@app.route('/browse/<path:rpath>')
def dir_listing(rpath):
    abs_path = os.path.join(BASE_DIR, rpath)
    x = os.walk(BASE_DIR)
    files = list()
    for i in x:
        if len(i[2]) > 0:
            files.append('/'.join([i[0], i[2][0]]).replace(BASE_DIR + '/', ''))
    if os.path.isfile(abs_path):
        return send_file(abs_path)
    return render_template('files.j2', files=files)


def store_data(deploy_data):
    try:
        path = create_directory_structure(component=deploy_data['component'])
    except BaseException as e:
        raise Exception("{}".format(e))

    with open('/'.join([path, 'deploy.csv']), 'a+') as csvfile:
        w = ','.join([deploy_data['date'],
                      deploy_data['component'],
                      deploy_data['version'],
                      deploy_data['user'],
                      deploy_data['status']])
        try:
            csvfile.write('\n'.join([w, '']))
            csvfile.flush()
        except BaseException as e:
            raise Exception("{}".format(e))


def create_directory_structure(component):
    date = datetime.datetime.now()
    path = '/'.join([BASE_DIR,
                     str(component),
                     str(date.year),
                     str(date.month),
                     str(date.day)])

    if not os.path.exists(path):
        try:
            os.makedirs(path, exist_ok=True)
        except BaseException as e:
            raise Exception("{}".format(e))
    return path


if __name__ == '__main__':
    app.run(host=BIND_ADDR, port=PORT)
