import unittest
from flask import session, request
from app import app

class PruebaGestorTareas(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        app.config['MYSQL_DB'] = 'test_db'  # Cambiar a una base de datos de prueba

    def test_home(self):
        respuesta = self.app.get('/')
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn(b'<title>Gestor de Tareas</title>', respuesta.data)

    def test_login_con_credenciales_correctas(self):
        with app.app_context():
            with self.app as cliente:
                with cliente.session_transaction() as sesion:
                    sesion['email'] = 'ejemplo@gmail.com'

                respuesta = self.app.post('/login', data={'email': 'ejemplo@gmail.com', 'password': 'contraseña'})

                self.assertEqual(respuesta.status_code, 302)
                self.assertEqual(respuesta.location, 'http://localhost/tasks')

    def test_login_con_credenciales_incorrectas(self):
        with app.app_context():
            with self.app as cliente:
                with cliente.session_transaction() as sesion:
                    sesion['email'] = 'ejemplo@gmail.com'

                respuesta = self.app.post('/login', data={'email': 'ejemplo@gmail.com', 'password': 'contraseñaincorrecta'})

                self.assertEqual(respuesta.status_code, 200)
                self.assertIn(b'Las credenciales no son correctas', respuesta.data)

    def test_tasks_sin_sesion_iniciada(self):
        respuesta = self.app.get('/tasks')
        self.assertEqual(respuesta.status_code, 302)
        self.assertEqual(respuesta.location, 'http://localhost/')

    def test_tasks_con_sesion_iniciada(self):
        with app.app_context():
            with self.app as cliente:
                with cliente.session_transaction() as sesion:
                    sesion['email'] = 'ejemplo@gmail.com'

                respuesta = self.app.get('/tasks')
                self.assertEqual(respuesta.status_code, 200)
                self.assertIn(b'<title>Tareas</title>', respuesta.data)

    # Agregar más pruebas según sea necesario

if __name__ == '__main__':
    unittest.main()
