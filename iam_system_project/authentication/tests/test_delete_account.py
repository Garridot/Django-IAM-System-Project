from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class CustomDeleteAccountViewTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user_data = {
            'email': 'testuser@example.com', 
            'password': 'Testp@ssword123',         
        }
        self.user = get_user_model().objects.create_user(**self.user_data)
        self.url = reverse('profile_delete')  # Change 'delete_account' to the actual name of your delete account view

    def test_delete_account_view(self):
        # Ensure the delete account page is accessible
        self.client.login(email=self.user_data['email'], password='Testp@ssword123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # Ensure delete account form submission works
        response = self.client.post(self.url, data={'password': 'Testp@ssword123', 'confirmation': True})
        self.assertEqual(response.status_code, 302)  # Check if the delete account form was submitted successfully

        # Check if the user is redirected to the correct URL (after successful account deletion)
        self.assertRedirects(response, reverse('login')) 

        # Ensure the user is no longer in the database
        self.assertFalse(get_user_model().objects.filter(email=self.user_data['email']).exists())

        # Ensure the user is now logged out
        self.assertNotIn('_auth_user_id', self.client.session)

    
    def test_delete_account_view_incorrect_password(self):
        # Ensure delete account form submission fails with incorrect password
        response = self.client.post(self.url, data={'password': 'IncorrectPassword', 'confirmation': True})
        
        # Adjust the expectation to check for 200 status code
        self.assertEqual(response.status_code, 200)  # Form submission should fail

        # Check if appropriate error message is displayed
        self.assertContains(response, 'Invalid password or confirmation checkbox not checked.')

        # Ensure the user is still in the database
        self.assertTrue(get_user_model().objects.filter(email=self.user_data['email']).exists())

    def test_delete_account_view_missing_confirmation(self):
        # Ensure delete account form submission fails without confirmation checkbox
        response = self.client.post(self.url, data={'password': 'Testp@ssword123'})
        
        # Adjust the expectation to check for 200 status code
        self.assertEqual(response.status_code, 200)  # Form submission should fail

        # Check if appropriate error message is displayed
        self.assertContains(response, 'Invalid password or confirmation checkbox not checked.')

        # Ensure the user is still in the database
        self.assertTrue(get_user_model().objects.filter(email=self.user_data['email']).exists())