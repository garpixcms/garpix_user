from django.conf import settings
from django.urls import reverse
from django.test import override_settings

from garpix_user.models import UserSession
from garpix_user.tests.utils.settings import GARPIX_USER_SETTINGS, GARPIX_USER_CONFIRMATION_SETTINGS
from garpix_user.tests.utils.test_case_mixin import ApiTestMixin
from django.utils.translation import ugettext_lazy as _

BASE_GARPIX_USER_SETTINGS = getattr(settings, 'GARPIX_USER', dict())


@override_settings(GARPIX_USER=GARPIX_USER_SETTINGS)
class RegistrationApiTest(ApiTestMixin):
    def setUp(self):
        self.set_init_data()

    def test_registration_by_username(self):
        """
        Check registration by username
        """

        self.User.USERNAME_FIELDS = ('username',)

        response = self.client.post(
            reverse('garpix_user:garpix_user_api:api_registration'),
            {
                'username': self.new_user_data['username'],
                'password': self.new_user_data['password'],
                'password_2': self.new_user_data['password']
            },
            HTTP_ACCEPT='application/json'
        )
        self.assertEqual(response.status_code, 201)

        response = self.client.post(
            reverse('garpix_user:garpix_user_api:api_login'),
            {
                'username': self.new_user_data['username'],
                'password': self.new_user_data['password'],
            },
            HTTP_ACCEPT='application/json'
        )
        self.check_login_result(response)

    def test_registration_by_email(self):
        """
        Check registration by email
        """

        self.User.USERNAME_FIELDS = ('email',)

        response = self.client.post(
            reverse('garpix_user:garpix_user_api:api_registration'),
            {
                'email': self.new_user_data['email'],
                'password': self.new_user_data['password'],
                'password_2': self.new_user_data['password']
            },
            HTTP_ACCEPT='application/json'
        )
        self.assertEqual(response.status_code, 201)

        response = self.client.post(
            reverse('garpix_user:garpix_user_api:api_login'),
            {
                'username': self.new_user_data['email'],
                'password': self.new_user_data['password'],
            },
            HTTP_ACCEPT='application/json'
        )
        self.check_login_result(response)

    def test_registration_by_phone(self):
        """
        Check registration by phone number
        """

        self.User.USERNAME_FIELDS = ('phone',)

        response = self.client.post(
            reverse('garpix_user:garpix_user_api:api_registration'),
            {
                'phone': self.new_user_data['phone'],
                'password': self.new_user_data['password'],
                'password_2': self.new_user_data['password']
            },
            HTTP_ACCEPT='application/json'
        )
        self.assertEqual(response.status_code, 201)

        response = self.client.post(
            reverse('garpix_user:garpix_user_api:api_login'),
            {
                'username': self.new_user_data['phone'],
                'password': self.new_user_data['password'],
            },
            HTTP_ACCEPT='application/json'
        )
        self.check_login_result(response)

    def test_registration_by_phone_or_email(self):
        """
        Check registration by phone number or email if User.USERNAME_FIELDS = ('phone', 'email')
        """

        self.User.USERNAME_FIELDS = ('phone', 'email')

        response = self.client.post(
            reverse('garpix_user:garpix_user_api:api_registration'),
            {
                'phone': self.new_user_data['phone'],
                'email': self.new_user_data['email'],
                'password': self.new_user_data['password'],
                'password_2': self.new_user_data['password']
            },
            HTTP_ACCEPT='application/json'
        )
        self.assertEqual(response.status_code, 201)

        response = self.client.post(
            reverse('garpix_user:garpix_user_api:api_login'),
            {
                'username': self.new_user_data['phone'],
                'password': self.new_user_data['password'],
            },
            HTTP_ACCEPT='application/json'
        )
        self.check_login_result(response)

        response = self.client.post(
            reverse('garpix_user:garpix_user_api:api_login'),
            {
                'username': self.new_user_data['email'],
                'password': self.new_user_data['password'],
            },
            HTTP_ACCEPT='application/json'
        )
        self.check_login_result(response)

    def test_registration_incorrect_password(self):
        """
        Check registration failed if the password is incorrect
        """

        self.User.USERNAME_FIELDS = ('phone',)

        # password don't match
        response = self.client.post(
            reverse('garpix_user:garpix_user_api:api_registration'),
            {
                'phone': self.new_user_data['phone'],
                'password': self.new_user_data['password'],
                'password_2': '1q2W3e4R5t6Y'
            },
            HTTP_ACCEPT='application/json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json(), {'password_2': [_('Passwords do not match')]})

        # incorrect password
        min_length = GARPIX_USER_SETTINGS.get('MIN_LENGTH_PASSWORD', 8)
        min_digits = GARPIX_USER_SETTINGS.get('MIN_DIGITS_PASSWORD', 2)
        min_chars = GARPIX_USER_SETTINGS.get('MIN_CHARS_PASSWORD', 2)
        min_uppercase = GARPIX_USER_SETTINGS.get('MIN_UPPERCASE_PASSWORD', 1)

        # check for min length
        response = self.client.post(
            reverse('garpix_user:garpix_user_api:api_registration'),
            {
                'phone': self.new_user_data['phone'],
                'password': 'qwerty',
                'password_2': 'qwerty'
            },
            HTTP_ACCEPT='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json(), {
            'password': [_('Password must be at least {min_length} characters long.'.format(min_length=min_length))]})

        # check for min digits
        response = self.client.post(
            reverse('garpix_user:garpix_user_api:api_registration'),
            {
                'phone': self.new_user_data['phone'],
                'password': 'qwertyq1',
                'password_2': 'qwertyq1'
            },
            HTTP_ACCEPT='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json(), {
            'password': [_('Password must container at least {min_digits} digits.'.format(min_digits=min_digits))]})

        # check for min char
        response = self.client.post(
            reverse('garpix_user:garpix_user_api:api_registration'),
            {
                'phone': self.new_user_data['phone'],
                'password': '12345678',
                'password_2': '12345678'
            },
            HTTP_ACCEPT='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json(), {
            'password': [_('Password must container at least {min_chars} chars.'.format(min_chars=min_chars))]})

        # check for uppercase letter
        response = self.client.post(
            reverse('garpix_user:garpix_user_api:api_registration'),
            {
                'phone': self.new_user_data['phone'],
                'password': 'q1w2e3r4t5y6',
                'password_2': 'q1w2e3r4t5y6'
            },
            HTTP_ACCEPT='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json(), {'password': [
            _('Password must container at least {min_uppercase} uppercase letter.'.format(
                min_uppercase=min_uppercase))]})

    @override_settings(GARPIX_USER=GARPIX_USER_CONFIRMATION_SETTINGS)
    def test_registration_unconfirmed_data(self):
        """
        Check registration failed if email and/or phone number was not confirmed before registrations, but
        the USE_PREREGISTRATION_EMAIL_CONFIRMATION and/or USE_PREREGISTRATION_PHONE_CONFIRMATION settings were set
        """

        # email
        self.User.USERNAME_FIELDS = ('email',)

        response = self.client.post(
            reverse('garpix_user:garpix_user_api:api_registration'),
            {
                'email': self.new_user_data['email'],
                'password': self.new_user_data['password'],
                'password_2': self.new_user_data['password']
            },
            HTTP_ACCEPT='application/json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json(), {'email': [_('Email was not confirmed')]})

        # phone
        self.User.USERNAME_FIELDS = ('phone',)

        response = self.client.post(
            reverse('garpix_user:garpix_user_api:api_registration'),
            {
                'phone': self.new_user_data['phone'],
                'password': self.new_user_data['password'],
                'password_2': self.new_user_data['password']
            },
            HTTP_ACCEPT='application/json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json(), {'phone': [_('Phone number was not confirmed')]})

    def test_registration_used_data(self):
        """
        Check registration failed if phone and/or email was already registered
        """

        self.User.USERNAME_FIELDS = ('phone', 'email')

        # email

        response = self.client.post(
            reverse('garpix_user:garpix_user_api:api_registration'),
            {
                'email': self.user_data['email'],
                'password': self.new_user_data['password'],
                'password_2': self.new_user_data['password']
            },
            HTTP_ACCEPT='application/json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json(), {'email': [_('This email is already in use')]})

        # phone

        response = self.client.post(
            reverse('garpix_user:garpix_user_api:api_registration'),
            {
                'phone': self.user_data['phone'],
                'password': self.new_user_data['password'],
                'password_2': self.new_user_data['password']
            },
            HTTP_ACCEPT='application/json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json(), {'phone': [_('This phone is already in use')]})

    @override_settings(GARPIX_USER=BASE_GARPIX_USER_SETTINGS)
    def test_registration_after_email_confirmation(self):
        """
        Check registration is OK after email confirmation
        """

        if BASE_GARPIX_USER_SETTINGS.get('USE_EMAIL_CONFIRMATION', False) and BASE_GARPIX_USER_SETTINGS.get('USE_PREREGISTRATION_EMAIL_CONFIRMATION', False):
            self.User.USERNAME_FIELDS = ('email',)

            response = self.client.post(
                reverse('garpix_user:garpix_user_api:api_confirm_email-send-code'),
                {
                    'email': self.new_user_data['email']
                },
                HTTP_ACCEPT='application/json'
            )

            self.assertEqual(response.status_code, 200)
            self.assertIn('token_number', response.json())

            token = response.json()['token_number']

            user_session = UserSession.objects.get(token_number=token)

            if BASE_GARPIX_USER_SETTINGS.get('USE_EMAIL_LINK_CONFIRMATION', False):
                user_session.confirm_email(email_confirmation_code=user_session.email_confirmation_code)
                user_session.save()
            else:

                response = self.client.post(
                    reverse('garpix_user:garpix_user_api:api_confirm_email-check-code'),
                    {
                        'email_confirmation_code': user_session.email_confirmation_code
                    },
                    HTTP_ACCEPT='application/json',
                    **{f'HTTP_{UserSession.HEAD_NAME}': token}
                )

                self.assertEqual(response.status_code, 204)

            response = self.client.post(
                reverse('garpix_user:garpix_user_api:api_registration'),
                {
                    'email': self.new_user_data['email'],
                    'password': self.new_user_data['password'],
                    'password_2': self.new_user_data['password']
                },
                HTTP_ACCEPT='application/json',
                **{f'HTTP_{UserSession.HEAD_NAME}': token}
            )
            self.assertEqual(response.status_code, 201)

    @override_settings(GARPIX_USER=BASE_GARPIX_USER_SETTINGS)
    def test_registration_after_phone_confirmation(self):
        """
        Check registration is OK after phone confirmation
        """

        if BASE_GARPIX_USER_SETTINGS.get('USE_PHONE_CONFIRMATION', False) and BASE_GARPIX_USER_SETTINGS.get('USE_PREREGISTRATION_PHONE_CONFIRMATION', False):
            self.User.USERNAME_FIELDS = ('phone',)

            response = self.client.post(
                reverse('garpix_user:garpix_user_api:api_confirm_phone-send-code'),
                {
                    'phone': self.new_user_data['phone']
                },
                HTTP_ACCEPT='application/json'
            )

            self.assertEqual(response.status_code, 200)
            self.assertIn('token_number', response.json())

            token = response.json()['token_number']

            user_session = UserSession.objects.get(token_number=token)

            response = self.client.post(
                reverse('garpix_user:garpix_user_api:api_confirm_phone-check-code'),
                {
                    'phone_confirmation_code': user_session.phone_confirmation_code
                },
                HTTP_ACCEPT='application/json',
                **{f'HTTP_{UserSession.HEAD_NAME}': token}
            )

            self.assertEqual(response.status_code, 200)

            response = self.client.post(
                reverse('garpix_user:garpix_user_api:api_registration'),
                {
                    'phone': self.new_user_data['phone'],
                    'password': self.new_user_data['password'],
                    'password_2': self.new_user_data['password']
                },
                HTTP_ACCEPT='application/json',
                **{f'HTTP_{UserSession.HEAD_NAME}': token}
            )
            self.assertEqual(response.status_code, 201)
