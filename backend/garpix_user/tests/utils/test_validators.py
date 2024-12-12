from rest_framework.test import APITestCase

from garpix_user.utils.validators import PositiveWithInfValidator


class PositiveWithInfValidatorTest(APITestCase):
    def setUp(self) -> None:
        self.validator = PositiveWithInfValidator(limit_value=1000)

    def test_validator_true(self) -> None:
        for i in range(0, -100, -5):
            self.assertTrue(self.validator.compare(i, 0))

    def test_validator_false(self) -> None:
        self.assertFalse(self.validator.compare(-1, 0))
        for i in range(1, 100, 5):
            self.assertFalse(self.validator.compare(i, 0))
