# .Главная страница доступна анонимному пользователю.
# Аутентифицированному пользователю доступна страница со списком заметок notes/, страница успешного добавления заметки done/, страница добавления новой заметки add/.
# .Страницы отдельной заметки, удаления и редактирования заметки доступны только автору заметки. Если на эти страницы попытается зайти другой пользователь — вернётся ошибка 404.
# При попытке перейти на страницу списка заметок, страницу успешного добавления записи, страницу добавления заметки, отдельной заметки, редактирования или удаления заметки анонимный пользователь перенаправляется на страницу логина.
# .Страницы регистрации пользователей, входа в учётную запись и выхода из неё доступны всем пользователям.

from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель простой')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug='slug',
            author=cls.author)
    # .Главная страница доступна анонимному пользователю.
    # .Страницы регистрации пользователей, входа в учётную запись и выхода из неё доступны всем пользователям.
    def test_pages_availability(self):
        # Проверяем главную, рег, вх, вых анонимам
        urls = (
            ('notes:home', None),
            # ('notes:detail', (self.note.slug)),
            ('users:login', None),
            ('users:logout', None),
            ('users:signup', None),
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
    # .Страницы отдельной заметки, удаления и редактирования заметки доступны только автору заметки. Если на эти страницы попытается зайти другой пользователь — вернётся ошибка 404.
    def test_availability_for_notes_detail_edit_and_delete(self):
        # Проверяем отдельную страницу, ред поста и удаление поста
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND),
        )
        for user, status in users_statuses:
            # Логиним пользователя в клиенте:
            self.client.force_login(user)
            # Для каждой пары "пользователь - ожидаемый ответ"
            # перебираем имена тестируемых страниц:
            for name in ('notes:edit', 'notes:delete', 'notes:detail'):
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=(self.note.slug,))
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    # При попытке перейти на страницу списка заметок, страницу успешного
    # добавления записи, страницу добавления заметки, отдельной заметки,
    # редактирования или удаления заметки анонимный пользователь перенаправляется на страницу логина.
    def test_redirect_for_anonymous_client(self):
        # Проверяем редиректы
        # Сохраняем адрес страницы логина:
        login_url = reverse('users:login')
        # В цикле перебираем имена страниц, с которых ожидаем редирект:
        for name, args in (
            ('notes:edit',(self.note.slug,)),
            ('notes:delete',(self.note.slug,)),
            ('notes:detail',(self.note.slug,)),
            ('notes:add', None),
            ('notes:success', None),
            ('notes:list', None)):
            with self.subTest(name=name):
                # Получаем адрес страницы редактирования или удаления комментария:
                url = reverse(name, args=(args))
                # Получаем ожидаемый адрес страницы логина, 
                # на который будет перенаправлен пользователь.
                # Учитываем, что в адресе будет параметр next, в котором передаётся
                # адрес страницы, с которой пользователь был переадресован.
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                # Проверяем, что редирект приведёт именно на указанную ссылку.
                self.assertRedirects(response, redirect_url) 

    def test_pages_availability_for_auth_user(self):
        self.client.force_login(self.reader)
        for name in ('notes:list', 'notes:add', 'notes:success'):
            response = self.client.get(reverse(name))
        self.assertEqual(response.status_code, HTTPStatus.OK)
    