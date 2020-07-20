import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import app
from models import setup_db


PRODUCER_JWT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkhYbmhDdUwyYllNSkJfcnZjRHAzSSJ9.eyJpc3MiOiJodHRwczovL21hZG1lZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYxNWY2ZjNkZTNiNTkwMDE5MjUwODJhIiwiYXVkIjoidWRhY2l0eSIsImlhdCI6MTU5NTI3OTA4NiwiZXhwIjoxNTk1MzY1NDg2LCJhenAiOiJpbTY0VE9LenFsTkRpZXFaWlBKNFBCQmdUeW9VbnJ3YyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmFjdG9ycyIsImNyZWF0ZTptb3ZpZXMiLCJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsInJlYWQ6YWN0b3JzIiwicmVhZDptb3ZpZXMiLCJ1cGRhdGU6YWN0b3JzIiwidXBkYXRlOm1vdmllcyJdfQ.G_70ZK1VtlAYMQTSCW5Y4Wjzm22DO718DXreyZtvYEOq8VIBkYGqnuy3-nkocvJPdZgRKdCLon7bNYHsVJzNGtJoQLy6qnO1oI83n9ITIe5Deecvil63SG0KPGEVuXYE48lPaF8bMTK3HRMfGZPomcOgmbsKTmLg347JQ5EAy8GcgGpwQ9uJ6-MTEUV6VIopocSATgBMs_wJ295j7_VvfZRoJSf513wdGKsiWQACjgEmeQU7WZfXw_1JEYNn_m6slQ85ITlvscuTttH2bnTw1Pis3ugAUZbkEiUUY6XpMSd84-aHFqAQ8RK_4Cs1U7Bv3n5qLuXz160hmNgVCUBrTA'
ASSISTANT_JWT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkhYbmhDdUwyYllNSkJfcnZjRHAzSSJ9.eyJpc3MiOiJodHRwczovL21hZG1lZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYxNWY2OWFkYmY2ZmYwMDEzNWM5MmIyIiwiYXVkIjoidWRhY2l0eSIsImlhdCI6MTU5NTI3OTE3MiwiZXhwIjoxNTk1MzY1NTcyLCJhenAiOiJpbTY0VE9LenFsTkRpZXFaWlBKNFBCQmdUeW9VbnJ3YyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsicmVhZDphY3RvcnMiLCJyZWFkOm1vdmllcyJdfQ.iFuxHGbO_vxkMrL1c7qB1y2d2X8V9w3IaQXYmFVhmB5BexIkLFzCtpgJ5Ke40zhRy1dtBjbURzXSQJK_zaGiE_hAP3RrYSop_3Y6orWnSetdH7UDcDGfqtnQh9UpdwdPHjFeWvSahIw4jxQqtf1HdJAqXP25tQenk2zjDbcOMcCelMpRRCtKG17Gfi9C3cFGHIPRBt-kpC04AVR6oNI96eSGg1mIlegJ-xlulNiXVoJUVX_E-6qvyc4GzA-ti7AHKn4J3ay1gUBcb6FczsFAQMpOCR4oqWeKite_-M7fN5p5lxNhhYy87CgHhbrbtMMPGztskM7ZTGgt6urEbhgusQ'
DIRECTOR_JWT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkhYbmhDdUwyYllNSkJfcnZjRHAzSSJ9.eyJpc3MiOiJodHRwczovL21hZG1lZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYxNWY2Y2I5NjViOGMwMDE5ZmU2N2JjIiwiYXVkIjoidWRhY2l0eSIsImlhdCI6MTU5NTI3OTIyMywiZXhwIjoxNTk1MzY1NjIzLCJhenAiOiJpbTY0VE9LenFsTkRpZXFaWlBKNFBCQmdUeW9VbnJ3YyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmFjdG9ycyIsImRlbGV0ZTphY3RvcnMiLCJyZWFkOmFjdG9ycyIsInJlYWQ6bW92aWVzIiwidXBkYXRlOmFjdG9ycyIsInVwZGF0ZTptb3ZpZXMiXX0.bNGfbE1d-HjqUbwjQosbdlx3RkxiQMvW8-5-GS-PHi9IU1n6Ow2s84-Opvjht4XcKAxalF-FbePycpgxAW6CKBsAa5QFUxtTUMmRLqlPJdnQ_3oAQN3jPkog3JkxtGYaCmx4cMc1CGyQ0AuMRsSgB8aObPrTrIlXxChPazlc7Ocd5plIkmfzJs48VnzmphYTyV2iLJMpKpXoeCB4qkQzPLe71rDess7ffRuwDZ1k6_tDa-mGpkyTMIxjlIVOUpvxTXjZvTw9AfK5XU3wmePIBD-YtyGCwExwHWPP-mkbPqur1oHrHZMbZwCoCOCxuQfC0uYC3ifkWWdUyLFO_1emuQ'


class ProducerCastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case for a Producer"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        setup_db(self.app)

        self.new_movie = {
            'title': 'Titanic',
            'release_year': 1999,
        }

        self.new_actor = {
            'name': 'Leo Di Cap',
            'age': 40,
            'gender': 'male',
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_movies_creation(self):
        """Test API can create a movie (POST request)"""
        res = self.client().post('/movies',
                                 json=self.new_movie,
                                 headers=dict(
                                     Authorization='Bearer ' + PRODUCER_JWT
                                 ))
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['title'], 'Titanic')
        self.assertEqual(data['release_year'], 1999)

    def test_api_can_get_all_movies(self):
        """Test API can get all movies (GET request)."""
        res = self.client().post('/movies',
                                 json=self.new_movie,
                                 headers=dict(
                                     Authorization='Bearer ' + PRODUCER_JWT
                                 ))
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        id = data['id']

        res1 = self.client().get('/movies',
                                 headers=dict(
                                     Authorization='Bearer ' + PRODUCER_JWT
                                 ))
        self.assertEqual(res1.status_code, 200)
        data1 = json.loads(res1.data)
        self.assertTrue(any(movie['id'] == id for movie in data1))

    def test_api_can_get_movie_by_id(self):
        """Test API can get a single movie by using it's id."""
        res = self.client().post('/movies',
                                 json=self.new_movie,
                                 headers=dict(
                                     Authorization='Bearer ' + PRODUCER_JWT
                                 ))
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)

        res1 = self.client().get('/movies/{}'.format(data['id']),
                                 headers=dict(
                                     Authorization='Bearer ' + PRODUCER_JWT
        ))
        self.assertEqual(res1.status_code, 200)
        data1 = json.loads(res1.data)
        self.assertEqual(data1['title'], 'Titanic')
        self.assertEqual(data1['release_year'], 1999)

    def test_movie_can_be_edited(self):
        """Test API can edit an existing movie. (PUT request)"""
        res = self.client().post('/movies',
                                 json=self.new_movie,
                                 headers=dict(
                                     Authorization='Bearer ' + PRODUCER_JWT
                                 ))
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)

        res1 = self.client().patch('/movies/{}'.format(data['id']),
                                   json={"title": "Titanic2"},
                                   headers=dict(
                                       Authorization='Bearer ' + PRODUCER_JWT
        ))
        self.assertEqual(res1.status_code, 200)
        data1 = json.loads(res1.data)
        self.assertEqual(data1['title'], 'Titanic2')
        self.assertEqual(data1['release_year'], 1999)

    def test_movie_deletion(self):
        """Test API can delete an existing movie. (DELETE request)."""
        res = self.client().post('/movies',
                                 json=self.new_movie,
                                 headers=dict(
                                     Authorization='Bearer ' + PRODUCER_JWT
                                 ))
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)

        res = self.client().delete('/movies/{}'.format(data['id']),
                                   headers=dict(
            Authorization='Bearer ' + PRODUCER_JWT
        ))
        self.assertEqual(res.status_code, 204)

        # Test to see if it exists, should return a 404
        result = self.client().get('/movies/{}'.format(data['id']),
                                   headers=dict(
            Authorization='Bearer ' + PRODUCER_JWT
        ))
        self.assertEqual(result.status_code, 404)

    def test_actors_creation(self):
        """Test API can create a actor (POST request)"""
        res = self.client().post('/actors',
                                 json=self.new_actor,
                                 headers=dict(
                                     Authorization='Bearer ' + PRODUCER_JWT
                                 ))
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['name'], 'Leo Di Cap')
        self.assertEqual(data['age'], 40)
        self.assertEqual(data['gender'], 'male')

    def test_api_can_get_all_actors(self):
        """Test API can get all actors (GET request)."""
        res = self.client().post('/actors',
                                 json=self.new_actor,
                                 headers=dict(
                                     Authorization='Bearer ' + PRODUCER_JWT
                                 ))
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        id = data['id']

        res1 = self.client().get('/actors',
                                 headers=dict(
                                     Authorization='Bearer ' + PRODUCER_JWT
                                 ))
        self.assertEqual(res1.status_code, 200)
        data1 = json.loads(res1.data)
        self.assertTrue(any(actor['id'] == id for actor in data1))

    def test_api_can_get_actor_by_id(self):
        """Test API can get a single actor by using it's id."""
        res = self.client().post('/actors',
                                 json=self.new_actor,
                                 headers=dict(
                                     Authorization='Bearer ' + PRODUCER_JWT
                                 ))
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)

        res1 = self.client().get('/actors/{}'.format(data['id']),
                                 headers=dict(
                                     Authorization='Bearer ' + PRODUCER_JWT
        ))
        self.assertEqual(res1.status_code, 200)
        data1 = json.loads(res1.data)
        self.assertEqual(data1['name'], 'Leo Di Cap')
        self.assertEqual(data1['age'], 40)
        self.assertEqual(data1['gender'], 'male')

    def test_actor_can_be_edited(self):
        """Test API can edit an existing actor. (PUT request)"""
        res = self.client().post('/actors',
                                 json=self.new_actor,
                                 headers=dict(
                                     Authorization='Bearer ' + PRODUCER_JWT
                                 ))
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)

        res1 = self.client().patch('/actors/{}'.format(data['id']),
                                   json={"name": "Brad"},
                                   headers=dict(
                                       Authorization='Bearer ' + PRODUCER_JWT
        ))
        self.assertEqual(res1.status_code, 200)
        data1 = json.loads(res1.data)
        self.assertEqual(data1['name'], 'Brad')
        self.assertEqual(data1['age'], 40)

    def test_actor_deletion(self):
        """Test API can delete an existing actor. (DELETE request)."""
        res = self.client().post('/actors',
                                 json=self.new_actor, headers=dict(
                                     Authorization='Bearer ' + PRODUCER_JWT
                                 ))
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)

        res = self.client().delete('/actors/{}'.format(data['id']),
                                   headers=dict(
                                       Authorization='Bearer ' + PRODUCER_JWT
        ))
        self.assertEqual(res.status_code, 204)

        # Test to see if it exists, should return a 404
        result = self.client().get('/actors/{}'.format(data['id']),
                                   headers=dict(
                                       Authorization='Bearer ' + PRODUCER_JWT
        ))
        self.assertEqual(result.status_code, 404)


class DirectorCastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case for a director"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        setup_db(self.app)

        self.new_movie = {
            'title': 'Titanic',
            'release_year': 1999,
        }

        self.new_actor = {
            'name': 'Leo Di Cap',
            'age': 40,
            'gender': 'male',
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_movies_creation_fails(self):
        """Test API can create a movie (POST request)"""
        res = self.client().post('/movies',
                                 json=self.new_movie,
                                 headers=dict(
                                     Authorization='Bearer ' + DIRECTOR_JWT
                                 ))
        self.assertEqual(res.status_code, 403)

    def test_api_can_get_all_movies(self):
        """Test API can get all movies (GET request)."""

        res1 = self.client().get('/movies',
                                 headers=dict(
                                     Authorization='Bearer ' + DIRECTOR_JWT
                                 ))
        self.assertEqual(res1.status_code, 200)

    def test_api_can_get_movie_by_id(self):
        """Test API can get a single movie by using it's id."""
        res = self.client().post('/movies',
                                 json=self.new_movie,
                                 headers=dict(
                                     Authorization='Bearer ' + PRODUCER_JWT
                                 ))
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)

        res1 = self.client().get('/movies/{}'.format(data['id']),
                                 headers=dict(
                                     Authorization='Bearer ' + DIRECTOR_JWT
        ))
        self.assertEqual(res1.status_code, 200)
        data1 = json.loads(res1.data)
        self.assertEqual(data1['title'], 'Titanic')
        self.assertEqual(data1['release_year'], 1999)

    def test_movie_can_be_edited(self):
        """Test API can edit an existing movie. (PUT request)"""
        res = self.client().post('/movies',
                                 json=self.new_movie,
                                 headers=dict(
                                     Authorization='Bearer ' + PRODUCER_JWT
                                 ))
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)

        res1 = self.client().patch('/movies/{}'.format(data['id']),
                                   json={"title": "Titanic2"},
                                   headers=dict(
                                       Authorization='Bearer ' + DIRECTOR_JWT
        ))
        self.assertEqual(res1.status_code, 200)

    def test_movie_deletion_fails(self):
        """Test API can delete an existing movie. (DELETE request)."""
        res = self.client().post('/movies',
                                 json=self.new_movie,
                                 headers=dict(
                                     Authorization='Bearer ' + PRODUCER_JWT
                                 ))
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)

        res = self.client().delete('/movies/{}'.format(data['id']),
                                   headers=dict(
            Authorization='Bearer ' + DIRECTOR_JWT
        ))
        self.assertEqual(res.status_code, 403)

    def test_actors_creation(self):
        """Test API can create a actor (POST request)"""
        res = self.client().post('/actors',
                                 json=self.new_actor,
                                 headers=dict(
                                     Authorization='Bearer ' + DIRECTOR_JWT
                                 ))
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['name'], 'Leo Di Cap')
        self.assertEqual(data['age'], 40)
        self.assertEqual(data['gender'], 'male')

    def test_api_can_get_all_actors(self):
        """Test API can get all actors (GET request)."""
        res = self.client().post('/actors',
                                 json=self.new_actor,
                                 headers=dict(
                                     Authorization='Bearer ' + DIRECTOR_JWT
                                 ))
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        id = data['id']

        res1 = self.client().get('/actors',
                                 headers=dict(
                                     Authorization='Bearer ' + DIRECTOR_JWT
                                 ))
        self.assertEqual(res1.status_code, 200)
        data1 = json.loads(res1.data)
        self.assertTrue(any(actor['id'] == id for actor in data1))

    def test_api_can_get_actor_by_id(self):
        """Test API can get a single actor by using it's id."""
        res = self.client().post('/actors',
                                 json=self.new_actor,
                                 headers=dict(
                                     Authorization='Bearer ' + DIRECTOR_JWT
                                 ))
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)

        res1 = self.client().get('/actors/{}'.format(data['id']),
                                 headers=dict(
                                     Authorization='Bearer ' + DIRECTOR_JWT
        ))
        self.assertEqual(res1.status_code, 200)
        data1 = json.loads(res1.data)
        self.assertEqual(data1['name'], 'Leo Di Cap')
        self.assertEqual(data1['age'], 40)
        self.assertEqual(data1['gender'], 'male')

    def test_actor_can_be_edited(self):
        """Test API can edit an existing actor. (PUT request)"""
        res = self.client().post('/actors',
                                 json=self.new_actor,
                                 headers=dict(
                                     Authorization='Bearer ' + DIRECTOR_JWT
                                 ))
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)

        res1 = self.client().patch('/actors/{}'.format(data['id']),
                                   json={"name": "Brad"},
                                   headers=dict(
                                       Authorization='Bearer ' + DIRECTOR_JWT
        ))
        self.assertEqual(res1.status_code, 200)
        data1 = json.loads(res1.data)
        self.assertEqual(data1['name'], 'Brad')
        self.assertEqual(data1['age'], 40)

    def test_actor_deletion(self):
        """Test API can delete an existing actor. (DELETE request)."""
        res = self.client().post('/actors',
                                 json=self.new_actor, headers=dict(
                                     Authorization='Bearer ' + DIRECTOR_JWT
                                 ))
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)

        res = self.client().delete('/actors/{}'.format(data['id']),
                                   headers=dict(
                                       Authorization='Bearer ' + DIRECTOR_JWT
        ))
        self.assertEqual(res.status_code, 204)

        # Test to see if it exists, should return a 404
        result = self.client().get('/actors/{}'.format(data['id']),
                                   headers=dict(
                                       Authorization='Bearer ' + DIRECTOR_JWT
        ))
        self.assertEqual(result.status_code, 404)


class AssistantCastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case for a director"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        setup_db(self.app)

        self.new_movie = {
            'title': 'Titanic',
            'release_year': 1999,
        }

        self.new_actor = {
            'name': 'Leo Di Cap',
            'age': 40,
            'gender': 'male',
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_movies_creation_fails(self):
        """Test API can create a movie (POST request)"""
        res = self.client().post('/movies',
                                 json=self.new_movie,
                                 headers=dict(
                                     Authorization='Bearer ' + ASSISTANT_JWT
                                 ))
        self.assertEqual(res.status_code, 403)

    def test_api_can_get_all_movies(self):
        """Test API can get all movies (GET request)."""

        res1 = self.client().get('/movies',
                                 headers=dict(
                                     Authorization='Bearer ' + ASSISTANT_JWT
                                 ))
        self.assertEqual(res1.status_code, 200)

    def test_api_can_get_movie_by_id(self):
        """Test API can get a single movie by using it's id."""
        res = self.client().post('/movies',
                                 json=self.new_movie,
                                 headers=dict(
                                     Authorization='Bearer ' + PRODUCER_JWT
                                 ))
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)

        res1 = self.client().get('/movies/{}'.format(data['id']),
                                 headers=dict(
                                     Authorization='Bearer ' + ASSISTANT_JWT
        ))
        self.assertEqual(res1.status_code, 200)
        data1 = json.loads(res1.data)
        self.assertEqual(data1['title'], 'Titanic')
        self.assertEqual(data1['release_year'], 1999)

    def test_movie_can_not_be_edited(self):
        """Test API can edit an existing movie. (PUT request)"""
        res = self.client().post('/movies',
                                 json=self.new_movie,
                                 headers=dict(
                                     Authorization='Bearer ' + PRODUCER_JWT
                                 ))
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)

        res1 = self.client().patch('/movies/{}'.format(data['id']),
                                   json={"title": "Titanic2"},
                                   headers=dict(
                                       Authorization='Bearer ' + ASSISTANT_JWT
        ))
        self.assertEqual(res1.status_code, 403)

    def test_movie_deletion_fails(self):
        """Test API can delete an existing movie. (DELETE request)."""
        res = self.client().post('/movies',
                                 json=self.new_movie,
                                 headers=dict(
                                     Authorization='Bearer ' + PRODUCER_JWT
                                 ))
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)

        res = self.client().delete('/movies/{}'.format(data['id']),
                                   headers=dict(
            Authorization='Bearer ' + ASSISTANT_JWT
        ))
        self.assertEqual(res.status_code, 403)

    def test_actors_creation_fails(self):
        """Test API can create a actor (POST request)"""
        res = self.client().post('/actors',
                                 json=self.new_actor,
                                 headers=dict(
                                     Authorization='Bearer ' + ASSISTANT_JWT
                                 ))
        self.assertEqual(res.status_code, 403)

    def test_api_can_get_all_actors(self):
        """Test API can get all actors (GET request)."""
        res = self.client().post('/actors',
                                 json=self.new_actor,
                                 headers=dict(
                                     Authorization='Bearer ' + PRODUCER_JWT
                                 ))
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        id = data['id']

        res1 = self.client().get('/actors',
                                 headers=dict(
                                     Authorization='Bearer ' + ASSISTANT_JWT
                                 ))
        self.assertEqual(res1.status_code, 200)
        data1 = json.loads(res1.data)
        self.assertTrue(any(actor['id'] == id for actor in data1))

    def test_api_can_get_actor_by_id(self):
        """Test API can get a single actor by using it's id."""
        res = self.client().post('/actors',
                                 json=self.new_actor,
                                 headers=dict(
                                     Authorization='Bearer ' + PRODUCER_JWT
                                 ))
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)

        res1 = self.client().get('/actors/{}'.format(data['id']),
                                 headers=dict(
                                     Authorization='Bearer ' + ASSISTANT_JWT
        ))
        self.assertEqual(res1.status_code, 200)
        data1 = json.loads(res1.data)
        self.assertEqual(data1['name'], 'Leo Di Cap')
        self.assertEqual(data1['age'], 40)
        self.assertEqual(data1['gender'], 'male')

    def test_actor_can_not_be_edited(self):
        """Test API can edit an existing actor. (PUT request)"""
        res = self.client().post('/actors',
                                 json=self.new_actor,
                                 headers=dict(
                                     Authorization='Bearer ' + PRODUCER_JWT
                                 ))
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)

        res1 = self.client().patch('/actors/{}'.format(data['id']),
                                   json={"name": "Brad"},
                                   headers=dict(
                                       Authorization='Bearer ' + ASSISTANT_JWT
        ))
        self.assertEqual(res1.status_code, 403)

    def test_actor_deletion_fails(self):
        """Test API can delete an existing actor. (DELETE request)."""
        res = self.client().post('/actors',
                                 json=self.new_actor, headers=dict(
                                     Authorization='Bearer ' + PRODUCER_JWT
                                 ))
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)

        res = self.client().delete('/actors/{}'.format(data['id']),
                                   headers=dict(
                                       Authorization='Bearer ' + ASSISTANT_JWT
        ))
        self.assertEqual(res.status_code, 403)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
