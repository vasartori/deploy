import unittest
from deploy_time import app


class DeployTimeTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_invalid_method(self):
        r = self.app.get('/deploy/teste')
        self.assertEqual(r.status, '405 METHOD NOT ALLOWED')

    # def test_invalid_post_data(self):
    #     r = self.app.post('/deploy/teste', data='{"aaaaa": 1}')
    #     print(r)

if __name__ == '__main__':
    unittest.main()