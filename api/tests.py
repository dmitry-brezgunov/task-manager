from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from .models import Task, User


class TaskTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_1 = User.objects.create_user(
            username='testuser1', password='testpassword1')
        self.user_2 = User.objects.create_user(
            username='testuser2', password='testpassword2')

        self.token = Token.objects.create(user=self.user_1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.data = {
            'title': 'test title', 'description': 'test description',
            'status': 'IN_WORK', 'completion_date': '25-10-2020 17:30'
        }

        self.patch_data = {
            'title': 'new title', 'description': 'new description',
            'status': 'COMPLETED', 'completion_date': '25-10-2020 17:30'
        }

        self.url = reverse('tasks-list')

    def test_task_create(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.filter(user=self.user_1).count(), 1)

        task = Task.objects.get()
        self.assertEqual(task.title, self.data['title'])
        self.assertEqual(task.description, self.data['description'])
        self.assertEqual(task.status, self.data['status'])
        self.assertEqual(
            task.completion_date.strftime('%d-%m-%Y %H:%M'),
            self.data['completion_date'])
        self.assertEqual(task.add_date.date(), timezone.now().date())

    def test_task_update(self):
        task = Task.objects.create(
            title=self.data['title'], description=self.data['description'],
            user=self.user_1)
        self.url = reverse('tasks-detail', args=[task.id])
        response = self.client.patch(self.url, self.patch_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        task = Task.objects.get(id=task.id)
        self.assertEqual(task.status, self.patch_data['status'])
        self.assertEqual(task.title, self.patch_data['title'])
        self.assertEqual(task.description, self.patch_data['description'])
        self.assertEqual(
            task.completion_date.strftime('%d-%m-%Y %H:%M'),
            self.patch_data['completion_date'])

    def test_tasks_visibility(self):
        task_1 = Task.objects.create(
            title=self.data['title'], description=self.data['description'],
            user=self.user_1)

        task_2 = Task.objects.create(
            title=self.data['title'], description=self.data['description'],
            user=self.user_2)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(response.json()['count'], 1)
        self.assertEquals(response.json()['results'][0]['id'], task_1.id)

        self.url = reverse('tasks-detail', args=[task_2.id])
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_filtering(self):
        Task.objects.create(
            title=self.data['title'], description=self.data['description'],
            user=self.user_1, status=self.data['status'])

        self.client.post(self.url, self.patch_data, format='json')
        self.assertEqual(Task.objects.count(), 2)

        response = self.client.get(self.url, {'status': 'IN_WORK'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 1)

        response = self.client.get(self.url, {'date_from': '01-10-2020'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 1)

        response = self.client.get(self.url, {'date_to': '01-10-2020'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 0)

    def test_history(self):
        self.client.post(self.url, self.data, format='json')
        task = Task.objects.get()
        self.url = reverse('tasks-detail', args=[task.id])
        self.client.patch(self.url, self.patch_data, format='json')

        self.url = reverse('tasks-history', args=[task.id])
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 2)

        results = response.json()['results']
        self.assertEqual(results[0]['title'], self.patch_data['title'])

        self.assertEqual(results[1]['title'], self.data['title'])

    def test_validation(self):
        wrong_data = self.data.copy()
        wrong_data['completion_date'] = '25-10-2019 17:30'
        response = self.client.post(self.url, wrong_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()['non_field_errors'][0],
            'Дата завершения не может быть раньше текущей даты')

        self.client.post(self.url, self.data, format='json')
        task = Task.objects.get()
        self.url = reverse('tasks-detail', args=[task.id])
        response = self.client.patch(self.url, wrong_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()['non_field_errors'][0],
            'Дата завершения не может быть раньше даты создания')
