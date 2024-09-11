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

    def test_cant_create_two_to_notes(self):
        for i in range(2):
            self.auth_client.post(self.url, data=self.form_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)

    def test_filling_slug(self):
        self.auth_client.post(self.url, data=self.form_data)
        note = Note.objects.get()
        self.assertIsNotNone(note.slug)


class TestNoteEditDelete(TestCase):
    NOTES_TITLE = 'Новая заметка'
    NOTES_TEXT = 'Текст заметки'
    NEW_NOTES_TEXT = 'Новый текст'

    @classmethod
    def setUpTestData(cls) -> None:
        cls.author = User.objects.create(username='Кот рыжий')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader = User.objects.create(username='Читатель')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.note = Note.objects.create(
            title=cls.NOTES_TITLE, text=cls.NOTES_TEXT, author=cls.author)
        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.delete_url = reverse('notes:delete', args=(cls.note.slug,))
        cls.form_data = {
            'title': cls.NOTES_TITLE,
            'text': cls.NEW_NOTES_TEXT,
            'author': cls.author
        }

    def test_author_can_delete_note(self):
        self.author_client.delete(self.delete_url)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 0)

    def test_user_cant_delete_note_of_another_user(self):
        response = self.reader_client.delete(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)

    def test_author_can_edit_note(self):
        self.author_client.post(self.edit_url, data=self.form_data)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.NEW_NOTES_TEXT)

    def test_user_cant_edit_note_of_another_user(self):
        response = self.reader_client.post(self.edit_url, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.NOTES_TEXT)
