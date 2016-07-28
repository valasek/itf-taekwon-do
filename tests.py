# -*- coding: utf-8 -*-
import os, datetime
import itf
import unittest
import tempfile


class ItfTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, itf.app.config['DATABASE'] = tempfile.mkstemp()
        itf.app.config['TESTING'] = True
        itf.app.config['WTF_CSRF_ENABLED'] = False
        self.app = itf.app.test_client()
        with itf.app.app_context():
            itf.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(itf.app.config['DATABASE'])

    def test_home_data(self):
        rv = self.app.get('/')
        assert b'Taekwondo' in rv.data

    def test_home_status_code(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def login(self, email, password):
        return self.app.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def register(self, team, first_name, last_name, email, password, confirm):
        return self.app.post('/register', data=dict(
            team=team,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            confirm=confirm
        ), follow_redirects=True)

    def test_register(self):
        rv = self.register('Test tým', 'Jméno', 'Příjmení', 'email@email.com', 'password', 'password')
        assert u'Registrace proběhla úspěšně.' in rv.data

    def new_member(self, itf_id, team_id, first_name, last_name, sex, birthdate, weight, level):
        return self.app.post('/member/new', data=dict(
            itf_id=itf_id,
            team_id=team_id,
            first_name=first_name,
            last_name=last_name,
            sex=sex,
            birthdate=birthdate,
            weight=weight,
            level=level
        ), follow_redirects=True)

    def test_new_member(self):
        self.login('admin', 'admin')
        rv = self.new_member(1234, 1, u'Stano', u'Valasek', 1, datetime.date(2013, 3, 25), 80, 1)
        assert u'Nový soutěžící úspěšně přidán' in rv.data

    def test_login_logout(self):
        rv = self.login('admin', 'admin')
        assert u'Byl jste úspěšně přihlášen' in rv.data
        rv = self.logout()
        assert u'Byli jste odhlášeni' in rv.data
        rv = self.login('adminx', 'default')
        assert u'Nesprávny email' in rv.data
        rv = self.login('admin', 'defaultx')
        assert u'Nesprávne heslo' in rv.data

    def test_new_member_status_code(self):
        self.login('admin', 'admin')
        result = self.app.get('/member/new')
        self.assertEqual(result.status_code, 200)


    def test_members_status_code(self):
        self.login('admin', 'admin')
        result = self.app.get('/members')
        self.assertEqual(result.status_code, 200)

    def test_administration_status_code(self):
        self.login('admin', 'admin')
        result = self.app.get('/administration')
        self.assertEqual(result.status_code, 200)

    def test_competitions_status_code(self):
        self.login('admin', 'admin')
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_competition_members_status_code(self):
        self.login('admin', 'admin')
        result = self.app.get('/competition-members')
        self.assertEqual(result.status_code, 200)

if __name__ == '__main__':
    unittest.main()
