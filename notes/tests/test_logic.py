from http import HTTPStatus

from pytils.translit import slugify  # type: ignore

from notes.forms import WARNING
from notes.models import Note
from .conftest import TestData


class TestNotesCreator(TestData):

    def test_anonymous_user_cant_create_note(self):
        notes_count = Note.objects.count()
        self.client.post(self.notes_add_url, data=self.form_data)
        self.assertEqual(Note.objects.count(), notes_count)

    def test_user_can_create_note(self):
        Note.objects.all().delete()
        response = self.author_client.post(
            self.notes_add_url, data=self.form_data
        )
        self.assertRedirects(response, self.notes_success_url)
        self.assertEqual(Note.objects.count(), 1)
        note = Note.objects.get()
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.author, self.author)

    def test_cant_create_two_to_notes(self):
        notes_count = Note.objects.count()
        self.form_data['slug'] = self.note.slug
        response = self.author_client.post(
            self.notes_add_url, data=self.form_data
        )
        self.assertEqual(Note.objects.count(), notes_count)
        slug = response.context['form']['slug'].data
        self.assertFormError(
            response, 'form', 'slug', slug + WARNING
        )

    def test_filling_slug(self):
        Note.objects.all().delete()
        self.author_client.post(self.notes_add_url, data=self.form_data)
        note = Note.objects.get()
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(note.slug, expected_slug)


class TestNoteEditDelete(TestData):
    NEW_NOTES_TEXT = 'Новый текст'

    def test_author_can_delete_note(self):
        notes_count = Note.objects.count()
        self.author_client.delete(self.notes_delete_url)
        self.assertEqual(Note.objects.count(), notes_count - 1)

    def test_user_cant_delete_note_of_another_user(self):
        notes_count = Note.objects.count()
        response = self.reader_client.delete(self.notes_delete_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), notes_count)

    def test_author_can_edit_note(self):
        self.form_data['text'] = self.NEW_NOTES_TEXT
        self.author_client.post(self.notes_edit_url, data=self.form_data)
        note = Note.objects.get(pk=self.note.id)
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.title, self.form_data['title'])

    def test_user_cant_edit_note_of_another_user(self):
        self.form_data['text'] = self.NEW_NOTES_TEXT
        response = self.reader_client.post(
            self.notes_edit_url, data=self.form_data
        )
        note = Note.objects.get(pk=self.note.id)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.author, self.note.author)
        self.assertEqual(note.slug, self.note.slug)
