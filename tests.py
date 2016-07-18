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


    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'Soutěž' in rv.data

if __name__ == '__main__':
    unittest.main()
