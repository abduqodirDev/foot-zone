from django.test import TestCase

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from stadion.models import Stadion, StadionReview
from users.models import User


class AllStadionAPITestCase(APITestCase):

    def test_all_stadion(self):
        user = User.objects.create(username='just')
        user.set_password('just1234')
        user.save()

        stadion = Stadion.objects.create(
            title="stadion title",
            description="stadion description",
            price=50000,
            latitude=22,
            longitude=33,
            dush=True,
            yoritish=True,
            start_time="07:00",
            end_time="23:00",
            user=user
        )

        review = StadionReview.objects.create(
            stadion=stadion,
            user=user,
            comment="this is comment",
            rank=5
        )

        request = self.client.get(reverse("stadion:all-stadion"))

        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.data), 1)
        self.assertEqual(request.data[0]['title'], 'stadion title')
        self.assertEqual(request.data[0]['price'], 50000.0)
        self.assertEqual(request.data[0]['latitude'], 22)
        self.assertEqual(request.data[0]['longitude'], 33)
        self.assertEqual(request.data[0]['photo'], None)
        self.assertEqual(request.data[0]['comment_count'], 1)
        self.assertEqual(request.data[0]['rank_ratio'], 5)
