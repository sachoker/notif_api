from django.utils.timezone import now
from rest_framework.test import APITestCase

from api.models import Mailing, Client, Message


class TestModel(APITestCase):
    def test_creates_mailings(self):
        mailing = Mailing.objects.create(
            date_start=now(),
            date_end=now(),
            text="Simple text",
            time_start=now().time(),
            time_end=now().time(),
            tag="test",
        )
        self.assertIsInstance(mailing, Mailing)
        self.assertEqual(mailing.tag, "test")

    def test_creates_clients(self):
        client = Client.objects.create(
            phone_number="76543256430",
            mobile_operator_code="1",
            tag="test",
            timezone="UTC",
        )
        self.assertIsInstance(client, Client)
        self.assertEqual(client.phone_number, "76543256430")

    def test_creates_messages(self):
        mailing = Mailing.objects.create(
            date_start=now(),
            date_end=now(),
            text="Simple text",
            time_start=now().time(),
            time_end=now().time(),
            tag="test",
        )
        client = Client.objects.create(
            phone_number="76523256430",
            mobile_operator_code="1",
            tag="test",
            timezone="UTC",
        )
        self.test_creates_clients()
        message = Message.objects.create(
            sending_status="No sent", mailing_id=mailing.id, client_id=client.id
        )
        self.assertIsInstance(message, Message)
        self.assertEqual(message.sending_status, "No sent")