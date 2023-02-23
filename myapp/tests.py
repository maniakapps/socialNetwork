from django.core.exceptions import ValidationError
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse

from myapp.models import User


def _create_image_with_size(size):
    # This method creates an image with the given size (in bytes)
    # and returns a File object that can be used for testing
    from io import BytesIO
    from PIL import Image
    image_file = BytesIO()
    image = Image.new('RGBA', size=(1, 1), color=(255, 0, 0, 0))
    image.save(image_file, 'png')
    image_file.seek(0)
    return image_file


class UserModelTestCase(TestCase):
    def test_create_user(self):
        # Test creating a user with valid data
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password',
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@example.com')

    def test_create_user_invalid(self):
        user_data = {
            'username': '',
            'email': 'invalid_email',
            'password': 'pass',
        }
        response = self.client.post(reverse('user-list'), user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(),
            {
                'username': ['This field may not be blank.'],
                'email': ['Enter a valid email address.'],
                'password': ['Ensure this field has at least 8 characters.'],
            }
        )


