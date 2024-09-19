from notes.models import Note
from notes.forms import NoteForm
from .conftest import TestData


class TestListPage(TestData):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.note_one = Note.objects.create(
            title='Заметка 1', text='Текст', author=cls.author
        )
        cls.note_two = Note.objects.create(
            title='Заметка 2', text='Текст', author=cls.reader
        )

    def test_note_context(self):
        response = self.author_client.get(self.notes_list_url)
        self.assertIn(self.note_one, response.context['object_list'])

    def test_users_notes(self):
        response = self.author_client.get(self.notes_list_url)
        self.assertNotIn(self.note_two, response.context['object_list'])


class TestCreateEditPage(TestData):

    def test_has_form_in_page_add_and_edit(self):
        for url in self.notes_add_url, self.notes_edit_url:
            with self.subTest():
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
