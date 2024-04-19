from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
from django.test import TestCase
# Импортируем функцию reverse(), она понадобится для получения адреса страницы.
from django.urls import reverse
from notes.forms import NoteForm
from notes.models import Note
from django.test import Client


# User = get_user_model()

# class TestDetailPage(TestCase):

#     @classmethod
#     def setUpTestData(cls):
#         cls.author = User.objects.create(username='Пользователь')
        
#         cls.note = Note.objects.create(
#             title='Заголовок',
#             text='Текст',
#             slug='slug',
#             author=cls.author)
#         cls.detail_url = reverse('notes:add')
        


#     def test_anonymous_client_has_no_form(self):
#         response = self.client.get(self.detail_url)
#         self.assertNotIn('form', response.context)
        
#     def test_authorized_client_has_form(self):
#         self.auth_client.force_login(self.author)
#         response = self.client.get(self.detail_url)
#         self.assertIn('form', response.context)
#         # Проверим, что объект формы соответствует нужному классу формы.
#         self.assertIsInstance(response.context['form'], NoteForm)
        