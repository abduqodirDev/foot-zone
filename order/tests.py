from datetime import date, timedelta

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from order.models import BronStadion
from stadion.models import Stadion


class BronStadionAPITestCase(APITestCase):
    def setUp(self):
        self.stadion = Stadion.objects.create(
            title="stadion title",
            description="stadion description",
            price=50000,
            latitude=22,
            longitude=33,
            dush=True,
            yoritish=True,
            start_time="07:00:00",
            end_time="23:00:00"
        )
        self.bron_date = date.today()

        self.bronstadion = BronStadion.objects.create(
            stadion=self.stadion,
            time="22",
            date=self.bron_date
        )
        self.bronstadion1 = BronStadion.objects.create(
            stadion=self.stadion,
            time="21",
            date=self.bron_date,
            is_active=True,
            status='T'
        )

    def test_get_bron_stadion(self):
        request = self.client.get(reverse("order:order", kwargs={'id':self.stadion.id}))
        data = request.data

        stadions = Stadion.objects.all()
        bronstadions = BronStadion.objects.all()

        self.assertEqual(len(stadions), 1)
        self.assertEqual(len(bronstadions), 2)

        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(data), 2)
        self.assertIn("brons", data)
        self.assertIn("stadion", data)

        brons = data['brons']
        stadions = data['stadion']

        self.assertIn("start_time", stadions)
        self.assertIn("end_time", stadions)
        self.assertIn("price", stadions)
        self.assertEqual(str(stadions['start_time']), "07:00:00")
        self.assertEqual(str(stadions['end_time']), "23:00:00")
        self.assertEqual(stadions['price'], 50000)
        self.assertEqual(len(brons), 7)

        self.assertIn(str(self.bron_date), brons)
        self.assertIn(str(self.bron_date + timedelta(days=1)), brons)
        self.assertIn(str(self.bron_date + timedelta(days=2)), brons)
        self.assertIn(str(self.bron_date + timedelta(days=3)), brons)
        self.assertIn(str(self.bron_date + timedelta(days=4)), brons)
        self.assertIn(str(self.bron_date + timedelta(days=5)), brons)
        self.assertIn(str(self.bron_date + timedelta(days=6)), brons)

        bron = brons[str(self.bron_date)]
        self.assertEqual(len(bron), 1)
        self.assertEqual(bron[0]['id'], 2)
        self.assertEqual(bron[0]['time'], "21")
        self.assertEqual(bron[0]['date'], str(self.bron_date))

    # def test_post_bron_stadion(self):
    #     request = self.client.post(
    #         reverse("order:order", kwargs={'id':self.stadion.id}),
    #         data = {
    #             "brons": [
    #                 {
    #                     "bron": "22",
    #                     "date": str(self.bron_date)
    #                 }
    #             ]
    #         }
    #     )
    #     print("just:", request.data)
    #     self.assertEqual(request.status_code, 200)
