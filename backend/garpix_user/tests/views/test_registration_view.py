from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from ...models import GarpixUserPasswordConfiguration, PasswordHistory

User = get_user_model()


class RegistrationViewTest(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        config = GarpixUserPasswordConfiguration.get_solo()
        config.password_history = 1
        config.save()

    def setUp(self):
        self.username = 'testuser1'
        self.password = 'Old-Password123!'
        self.new_password = 'New-Password123!'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user.save()

    # TODO:
    def test_create(self):
        # self.client.force_authenticate(self.user)
        # response = self.client.post(
        #     '/api/garpix_user/change_password/',
        #     {
        #         'password': 'incorrect-password',
        #         'new_password': self.new_password,
        #     },
        # )

        # self.assertEqual(response.status_code, 400)
        # self.assertDictEqual(response.json(), {
        #     'password': ['Password is incorrect'],
        # })
