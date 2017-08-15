from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.contrib import auth
from selenium import webdriver

# Create your tests here.

class ApiTests(TestCase):
    def test_add_not_authenticated(self):
        """Login should be required"""
        response = self.client.post(reverse("add"), {"title": "Hello", "description":"World!"})
        self.assertEqual(response.status_code, 302)

    def test_get_all_not_authenticated(self):
        """Login should be required"""
        response = self.client.get(reverse("all"))
        self.assertEqual(response.status_code, 302)

    def test_change_not_authenticated(self):
        """Login should be required"""
        response = self.client.post(reverse("change"), {"id": 1, "closed": "true"})
        self.assertEqual(response.status_code, 302)

    def test_delete_not_authenticated(self):
        """Login should be required"""
        response = self.client.post(reverse("delete"), {"id": 1})
        self.assertEqual(response.status_code, 302)


    def test_add_returns(self):
        """Adding a todo makes it visible"""
        User.objects.create_user("testuser", "testuser@example.com", "abc")
        self.client.login(username="testuser", password="abc")

        response = self.client.post(reverse("add"),
                                    {"title": "Hello",
                                     "description":"World!"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], 1)
        self.assertEqual(response.json()["title"], "Hello")
        self.assertEqual(response.json()["description"], "World!")
        self.assertEqual(response.json()["closed"], False)
        self.assertIn("created_date", response.json())
        self.assertEqual(response.json()["author"], "testuser")
        self.assertEqual(response.json()["author_id"], 1)

    def test_get_all_empty(self):
        """There are no todos initially"""
        User.objects.create_user("testuser", "testuser@example.com", "abc")
        self.client.login(username="testuser", password="abc")

        response = self.client.get(reverse("all"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

    def test_add_empty(self):
        """Adding an empty todo fails"""
        User.objects.create_user("testuser", "testuser@example.com", "abc")
        self.client.login(username="testuser", password="abc")

        response = self.client.post(reverse("add"), {})
        self.assertEqual(response.status_code, 400)

        response = self.client.get(reverse("all"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)


    def test_get_all_all(self):
        """All the current users todos are returned"""
        User.objects.create_user("testuser", "testuser@example.com", "abc")
        self.client.login(username="testuser", password="abc")

        response = self.client.post(reverse("add"),
                                    {"title": "Hello1",
                                     "description":"World!1"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], 1)

        response = self.client.post(reverse("add"),
                                    {"title": "Hello2",
                                     "description":"World!2"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], 2)

        response = self.client.get(reverse("all"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]["id"], 1)
        self.assertEqual(response.json()[1]["id"], 2)

        response = self.client.post(reverse("add"),
                                    {"title": "Hello3",
                                     "description":"World!3"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], 3)

        response = self.client.get(reverse("all"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)
        self.assertEqual(response.json()[0]["id"], 1)
        self.assertEqual(response.json()[1]["id"], 2)
        self.assertEqual(response.json()[2]["id"], 3)


    def test_get_all_only(self):
        """Only the current users todos are returned"""
        User.objects.create_user("testuser1", "testuser1@example.com", "abc")
        self.client.login(username="testuser1", password="abc")

        response = self.client.post(reverse("add"),
                                    {"title": "Hello1",
                                     "description":"World!1"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], 1)

        response = self.client.post(reverse("add"),
                                    {"title": "Hello2",
                                     "description":"World!2"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], 2)

        response = self.client.get(reverse("all"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]["id"], 1)
        self.assertEqual(response.json()[1]["id"], 2)


        User.objects.create_user("testuser2", "testuser1@example.com", "abc")
        self.client.login(username="testuser2", password="abc")

        response = self.client.get(reverse("all"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

    def test_closing(self):
        """Closing/opening todos works"""
        User.objects.create_user("testuser", "testuser1@example.com", "abc")
        self.client.login(username="testuser", password="abc")

        response = self.client.post(reverse("add"),
                                    {"title": "Hello",
                                     "description":"World!"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], 1)
        self.assertEqual(response.json()["closed"], False)

        response = self.client.post(reverse("change"), {"id": 1, "closed": "true"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], 1)
        self.assertEqual(response.json()["closed"], True)

        response = self.client.get(reverse("all"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["id"], 1)
        self.assertEqual(response.json()[0]["closed"], True)


        response = self.client.post(reverse("change"), {"id": 1, "closed": "true"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], 1)
        self.assertEqual(response.json()["closed"], True)

        response = self.client.get(reverse("all"))
        self.assertEqual(response.json()[0]["id"], 1)
        self.assertEqual(response.json()[0]["closed"], True)


        response = self.client.post(reverse("change"), {"id": 1, "closed": "false"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], 1)
        self.assertEqual(response.json()["closed"], False)

        response = self.client.get(reverse("all"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["id"], 1)
        self.assertEqual(response.json()[0]["closed"], False)

    def test_delete(self):
        """After deleting a todo it no longer exists"""
        User.objects.create_user("testuser", "testuser1@example.com", "abc")
        self.client.login(username="testuser", password="abc")

        response = self.client.post(reverse("add"),
                                    {"title": "Hello1",
                                     "description":"World!1"})
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse("add"),
                                    {"title": "Hello2",
                                     "description":"World!2"})
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse("add"),
                                    {"title": "Hello3",
                                     "description":"World!3"})
        self.assertEqual(response.status_code, 200)


        response = self.client.post(reverse("delete"), {"id": 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["deleted"], 2)

        response = self.client.post(reverse("all"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]["id"], 1)
        self.assertEqual(response.json()[1]["id"], 3)

class UserTests(TestCase):
    def test_register_works(self):
        response = self.client.post(reverse("register"), {"username": "testuser",
                                                          "password1": "abcd1234",
                                                          "password2": "abcd1234"})
        self.assertRedirects(response, reverse("index"))
        user = User.objects.get(username="testuser")
        self.assertEqual(user.id, 1)

    def test_register_empty(self):
        response = self.client.post(reverse("register"), {})
        self.assertRedirects(response, reverse("login"))

    def test_register_username_blank(self):
        """Can't have empty username"""
        response = self.client.post(reverse("register"), {"username": "",
                                                          "password1":"abcd1234",
                                                          "password2":"abcd1234"})
        self.assertRedirects(response, reverse("login"))

    def test_register_password_blank(self):
        """Can't have no password"""
        response = self.client.post(reverse("register"), {"username": "testuser",
                                                          "password1":"",
                                                          "password2":""})
        self.assertRedirects(response, reverse("login"))

    def test_register_password_not_matching(self):
        """Can't give two different passwords at registration"""
        response = self.client.post(reverse("register"), {"username": "testuser",
                                                          "password1":"abcd1234",
                                                          "password2":"4321dcba"})
        self.assertRedirects(response, reverse("login"))

    def test_register_duplicate_user(self):
        """Can't create a user with an existing name"""
        response = self.client.post(reverse("register"), {"username": "testuser",
                                                          "password1":"abcd1234",
                                                          "password2":"abcd1234"})
        self.assertRedirects(response, reverse("index"))
        self.client.logout()
        response = self.client.post(reverse("register"), {"username": "testuser",
                                                          "password1":"abcd1234",
                                                          "password2":"abcd1234"})
        self.assertRedirects(response, reverse("login"))

    def test_register_logs_in(self):
        """Registering a user logs you in immediately"""
        response = self.client.post(reverse("register"), {"username": "testuser",
                                                          "password1":"abcd1234",
                                                          "password2":"abcd1234"})
        self.assertRedirects(response, reverse("index"))
        self.client.login(username="testuser", password="abc")
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_logout(self):
        """Logout should work"""
        response = self.client.post(reverse("register"), {"username": "testuser",
                                                          "password1":"abcd1234",
                                                          "password2":"abcd1234"})
        self.assertRedirects(response, reverse("index"))
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)


        response = self.client.post(reverse("logout"))
        self.assertRedirects(response, reverse("login"))
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)


    def test_login(self):
        """Logout should work"""
        response = self.client.post(reverse("register"), {"username": "testuser",
                                                          "password1":"abcd1234",
                                                          "password2":"abcd1234"})
        self.assertRedirects(response, reverse("index"))
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)


        response = self.client.post(reverse("logout"))
        self.assertRedirects(response, reverse("login"))
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)


        response = self.client.post(reverse("login"), {"username": "testuser",
                                                       "password":"abcd1234"})
        self.assertRedirects(response, reverse("index"))
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)

class BrowserTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(BrowserTests, cls).setUpClass()
        cls.browser = webdriver.Chrome()
        cls.browser.implicitly_wait(1)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(BrowserTests, cls).tearDownClass()

    def register(self, username):
        """Helper method for registration"""
        self.browser.get(self.live_server_url)
        username_input = self.browser.find_element_by_id("register_username")
        username_input.send_keys(username)
        password1_input = self.browser.find_element_by_id("register_password1")
        password1_input.send_keys("abcd1234")
        password2_input = self.browser.find_element_by_id("register_password2")
        password2_input.send_keys("abcd1234")

        button = self.browser.find_element_by_id("register_button")
        button.click()


    def test_register(self):
        self.register("testuser")
        self.browser.find_element_by_tag_name("h2")

    def test_add_todo(self):
        print("hello")
        self.register("testuser")
        title = self.browser.find_element_by_id("title")
        title.send_keys("First")

        description = self.browser.find_element_by_id("description")
        description.send_keys("My first todo")

        submit = self.browser.find_elements_by_tag_name("input")[2]
        submit.click()
