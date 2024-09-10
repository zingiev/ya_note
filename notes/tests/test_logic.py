from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note


User = get_user_model()


class TestNotesCreator(TestCase):
    NOTES_TITLE = 'Новая заметка'
    NOTES_TEXT = 'Текст заметки'

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create(username='Главный герой')
        cls.url = reverse('notes:add')
        cls.url_success = reverse('notes:success')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        cls.form_data = {
            'title': cls.NOTES_TITLE,
            'text': cls.NOTES_TEXT,
        }

    def test_anonymous_user_cant_create_note(self):
        self.client.post(self.url, data=self.form_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 0)

    def test_user_can_create_note(self):
        response = self.auth_client.post(self.url, data=self.form_data)
        self.assertRedirects(response, self.url_success)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)
        note = Note.objects.get()
        self.assertEqual(note.title, self.NOTES_TITLE)
        self.assertEqual(note.text, self.NOTES_TEXT)
        self.assertEqual(note.author, self.user)
