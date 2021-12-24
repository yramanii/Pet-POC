import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import unittest
from pet import app, db
from pet.models import User

class testing(unittest.TestCase):
    def setUp(self):

        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(parentdir, 'test.db')
        self.app = app.test_client()
        db.create_all()
        # db.session.add(User(name='yash', email='yash@gmail.com', password='yash', number='123456', category_name='buyer'))
        # db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def register(self, name, email, password, number, category_name):
        return self.app.post('/register',data=dict(name=name, email=email, password=password, number=number, category_name=category_name), follow_redirects=True)

    def login(self, email, password):
        return self.app.post('/login',data=dict(email=email, password=password),
        follow_redirects=True)

    def logout(self):
        return self.app.get('/logout',follow_redirects=True)
#-----------------------------------------------------------------------------------------------------------
    def test_home_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_valid_user_registration(self):
        response = self.register('yash', 'yash@gmail.com', 'yash', '123456', 'buyer')
        self.assertEqual(response.status_code, 200)
    
    def test_valid_user_login(self):
        response = self.login('yash@gmail.com', 'yash')
        self.assertEqual(response.status_code, 200)

    def test_user_logout(self):
        response = self.logout()
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
