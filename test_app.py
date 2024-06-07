import unittest
from xmlrunner import XMLTestRunner
from app import app, session, Data


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        session.query(Data).delete()
        session.commit()

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_store_data(self):
        response = self.app.post('/store_data', json={'name': 'test_name'})
        self.assertEqual(response.status_code, 200)
        data = session.query(Data).filter_by(name='test_name').first()
        self.assertIsNotNone(data)

    def test_read_data(self):
        self.app.post('/store_data', json={'name': 'test_name'})
        response = self.app.get('/read_data')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'test_name', response.data)


if __name__ == '__main__':
    with open('test-reports/results.xml', 'w') as output:
        unittest.main(testRunner=XMLTestRunner(output=output))
