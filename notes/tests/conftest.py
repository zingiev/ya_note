from django.test import TestCase, Client  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore
from django.urls import reverse

from notes.models import Note


User = get_user_model()


class TestData(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Чел простой')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.note = Note.objects.create(
            title='Заголовок', text='Текст заметки', author=cls.author
        )
        cls.home_url = reverse('notes:home')
        cls.notes_add_url = reverse('notes:add')
        cls.notes_list_url = reverse('notes:list')
        cls.notes_success_url = reverse('notes:success')
        cls.notes_edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.notes_detail_url = reverse('notes:detail', args=(cls.note.slug,))
        cls.notes_delete_url = reverse('notes:delete', args=(cls.note.slug,))
        cls.users_login = reverse('users:login')
        cls.users_logout = reverse('users:logout')
        cls.users_signup = reverse('users:signup')
        cls.form_data = {
            'title': 'Новая заметка',
            'text': 'Текст заметки',
        }
