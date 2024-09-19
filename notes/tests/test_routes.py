from http import HTTPStatus

from django.contrib.auth import get_user_model

from .conftest import TestData


User = get_user_model()


class TestRoutes(TestData):

    def test_pages_availability(self):
        urls = (
            self.home_url,
            self.users_login,
            self.users_logout,
            self.users_signup
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_notes_edit_and_detail_and_delete(self):
        user_statuses = (
            (self.author_client, HTTPStatus.OK),
            (self.reader_client, HTTPStatus.NOT_FOUND)
        )
        for user, status in user_statuses:
            urls = (
                self.notes_edit_url,
                self.notes_detail_url,
                self.notes_delete_url
            )
            for url in urls:
                with self.subTest(user=user, url=url):
                    response = user.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        urls = (
            self.notes_add_url,
            self.notes_edit_url,
            self.notes_detail_url,
            self.notes_delete_url,
            self.notes_list_url,
            self.notes_success_url
        )
        for url in urls:
            with self.subTest(url=url):
                redirect_url = f'{self.users_login}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)

    def test_avaliablity_pages_author(self):
        urls = (
            self.notes_list_url,
            self.notes_success_url,
            self.notes_add_url
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
