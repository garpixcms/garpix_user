from unittest.mock import MagicMock

from rest_framework.test import APITestCase

from garpix_user.utils.repluralize import rupluralize, translation


class RepluralizeTest(APITestCase):
    def setUp(self):
        self.arg = "arg1,arg2,arg3"

    def test_repluralize(self) -> None:
        translation.get_language = MagicMock(return_value="eu")

        self.assertEqual(rupluralize(11, self.arg), "arg1")
        self.assertEqual(rupluralize(-11, self.arg), "arg1")

        self.assertEqual(rupluralize(22, self.arg), "arg2")
        self.assertEqual(rupluralize(-22, self.arg), "arg2")

    def test_repluralize_ru(self) -> None:
        translation.get_language = MagicMock(return_value="ru")

        self.assertEqual(rupluralize(21, self.arg), "arg1")
        self.assertEqual(rupluralize(-21, self.arg), "arg1")

        self.assertEqual(rupluralize(22, self.arg), "arg2")
        self.assertEqual(rupluralize(-22, self.arg), "arg2")

        self.assertEqual(rupluralize(15, self.arg), "arg3")
        self.assertEqual(rupluralize(-15, self.arg), "arg3")

        self.assertTrue(translation.get_language.called)
