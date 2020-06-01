from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Post


class BlogTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='jim',
            email='jim@gmail.com',
            password='secret',
        )

        self.post = Post.objects.create(
            title='A good title',
            body='It is the body',
            author=self.user,
        )

    def test_string_representation(self):
        post = Post(title='A new title')
        self.assertEqual(str(post), post.title)

    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'A good title')
        self.assertEqual(f'{self.post.body}', 'It is the body')
        self.assertEqual(f'{self.post.author}', 'jim')

    def post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'It is the body')
        self.assertTemplateUsed(response, 'home.html')

    def test_post_detail_view(self):
        response = self.client.get('/post/1/')
        no_response = self.client.get('/post/1000000000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'A good title')
        self.assertTemplateUsed(response, 'post_detail.html')

    def test_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), '/post/1/')

    def test_post_create_view(self):
        response = self.client.post(reverse('post_new'), {
            'title': "A new title",
            'body': 'A new Body',
            "author": self.user,
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A new title")
        self.assertContains(response, 'A new Body')

    def test_post_update_view(self):
        response = self.client.post(reverse("post_edit", args='1'), {
            'title': 'Updated title',
            'body': "Updated body",
        })
        self.assertEqual(response.status_code, 302)

    def test_post_delete_view(self):
        response = self.client.get(reverse('post_delete', args='1'))
        self.assertEqual(response.status_code, 200)
