from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from notes.models import Note


User = get_user_model()


class TestListPage(TestCase):
    LIST_URL = reverse('notes:list')

    @classmethod
    def setUpTestData(cls) -> None:
        cls.author_one = User.objects.create(username='Лев Толстой')
        cls.author_two = User.objects.create(username='Чел простой')
        cls.note_one = Note.objects.create(
            title='Заметка 1', text='Текст',
            slug='zametka1', author=cls.author_one
        )
        cls.note_two = Note.objects.create(
            title='Заметка 2', text='Текст',
            slug='zametka2', author=cls.author_two
        )

    def test_note_context(self):
        self.client.force_login(self.author_one)
        response = self.client.get(self.LIST_URL)
        object_list = response.context['object_list']
        self.assertIn(self.note_one, object_list)

    def test_users_notes(self):
        self.client.force_login(self.author_one)
        response = self.client.get(self.LIST_URL)
        object_list = response.context['object_list']
        self.assertNotIn(self.note_two, object_list)


class TestCreateEditPage(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.author = User.objects.create(username='Лев Толстой')
        cls.note = Note.objects.create(
            title='Заметка', text='Текст',
            slug='zametka', author=cls.author
        )

    def test_has_form_in_page_add_and_edit(self):
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,))
        )
        self.client.force_login(self.author)
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertIn('form', response.context)
