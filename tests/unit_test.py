import json
import unittest
from unittest.mock import patch
from deploy_time import app
import datetime


class DeployTimeTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_invalid_method(self):
        r = self.app.get('/deploy/teste')
        self.assertEqual(r.status, '405 METHOD NOT ALLOWED')

    def test_invalid_post_data(self):
        r = self.app.post('/deploy/teste', data='{"aaaaa": 1}',
                          content_type='application/json')
        self.assertEqual(r.status, '422 UNPROCESSABLE ENTITY')

    def test_invalid_status(self):
        d = '{"version": "2.3.4", "user": "lalala", "status": "XXX"}'
        r = self.app.post('/deploy/teste', data=d,
                          content_type='application/json')
        self.assertEqual(r.status, '422 UNPROCESSABLE ENTITY')

    @patch("deploy_time.BASE_DIR", "/tmp/teste1")
    def test_ok(self):
        d = '{"version": "2.3.4", "user": "lalala", "status": "OK"}'
        r = self.app.post('/deploy/teste', data=d,
                          content_type='application/json')
        self.assertEqual(r.status, '200 OK')

    @patch("deploy_time.BASE_DIR", "/tmp/status_ok")
    def test_file_format(self):
        app_name = "teste"
        app_version = "2.2.2"
        user = "lalala"
        d = {"version": app_version, "user": user, "status": "OK"}
        r = self.app.post('/deploy/{}'.format(app_name), data=json.dumps(d),
                          content_type='application/json')
        date = datetime.datetime.now()
        y = str(date.year)
        m = str(date.month)
        d = str(date.day)
        abs_path = '/'.join(['/tmp/status_ok', 'teste', y, m, d, 'deploy.csv'])
        with open(abs_path) as f:
            t = f.readline().split(',')
        deploy_data = t[0].split('.')[0]
        application = t[1]
        version = t[2]
        username = t[3]
        status = t[4].replace('\n', '')

        try:
            datetime.datetime.strptime(deploy_data, '%Y-%m-%d %H:%M:%f')
            date_ok = True
        except ValueError:
            date_ok = False

        self.assertEqual(date_ok, True)
        self.assertEqual(application, app_name)
        self.assertEqual(version, app_version)
        self.assertEqual(username, user)
        self.assertEqual(status, 'OK')
        self.assertEqual(r.status, '200 OK')


if __name__ == '__main__':
    unittest.main()
