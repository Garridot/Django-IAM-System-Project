from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from django.contrib.auth import get_user_model


class CustomPasswordResetViewTest(TestCase):

    def setUp(self):
        # Create a user for testing
        self.user = get_user_model().objects.create_user(email='testuser@example.com', password='Testp@ssword123')

        # Set up the client
        self.client = Client()

    def test_view_render_correct_template(self):
        # Access the password reset view
        response = self.client.get(reverse('password_reset'))

        # Ensure that the view renders the correct template
        self.assertTemplateUsed(response, 'accounts/password_reset/password_reset.html')

    def test_reset_password_sends_email(self):
        # Access the password reset view and submit the form
        response = self.client.post(reverse('password_reset'), {'email': 'testuser@example.com'})

        # Check that the response redirects to the password reset done page
        self.assertRedirects(response, reverse('password_reset_done'))

        # Check that an email was sent
        self.assertEqual(len(mail.outbox), 1)

        # Check the email subject and recipient
        email = mail.outbox[0]
        self.assertEqual(email.subject, 'Password reset on testserver')
        self.assertEqual(email.to, ['testuser@example.com'])

    def test_reset_password_form_invalid_email(self):
        # Access the password reset view with an invalid email
        response = self.client.post(reverse('password_reset'), {'email': 'invalidemail@1234.com'})

        # Check that the response does not redirect
        self.assertEqual(response.status_code, 200)

        # Check that the view renders the correct template
        self.assertTemplateUsed(response, 'accounts/password_reset/password_reset.html')

        # Check for the form error message in the response content
        self.assertContains(response, 'Email address not found.')   
