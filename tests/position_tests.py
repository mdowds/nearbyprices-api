import unittest
from webargs import ValidationError
from api import position


class PositionTests(unittest.TestCase):

    def test_validateLatitude_WithValidLatitude_NoThrow(self):
        raised = False
        try:
            position.validate_latitude(50.5)
        except:
            raised = True

        self.assertFalse(raised, 'Exception raised')

    def test_validateLatitude_WithInvalidLatitude_Throws(self):
        self.assertRaises(ValidationError, position.validate_latitude, 45)

    def test_validateLongitude_WithValidLongitude_NoThrow(self):
        raised = False
        try:
            position.validate_longitude(-2.2)
        except:
            raised = True

        self.assertFalse(raised, 'Exception raised')

    def test_validateLongitude_WithInvalidLongitude_Throws(self):
        self.assertRaises(ValidationError, position.validate_longitude, 2)


if __name__ == '__main__':
    unittest.main()
