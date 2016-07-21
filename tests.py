# -*- coding: utf-8 -*-
import os
import itf
import unittest
import tempfile


class ItfTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, itf.app.config['DATABASE'] = tempfile.mkstemp()
        itf.app.config['TESTING'] = True
        self.app = itf.app.test_client()
        with itf.app.app_context():
            itf.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(itf.app.config['DATABASE'])

    def test_home_data(self):
        rv = self.app.get('/')
        assert b'Soutěž' in rv.data

    def test_home_status_code(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            email=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('admin', 'admin')
        assert b'Byl jste úspěšně přihlášen' in rv.data
        rv = self.logout()
        assert b'Byli jste odhlášeni' in rv.data
        rv = self.login('adminx', 'default')
        assert 'Invalid username' in rv.data
        rv = self.login('admin', 'defaultx')
        assert 'Invalid password' in rv.data

if __name__ == '__main__':
    unittest.main()
