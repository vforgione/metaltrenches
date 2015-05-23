from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from model_mommy import mommy

from .models import Review
from ..music.models import Band, Album


class PublishingTests(TestCase):
    def setUp(self):
        band = mommy.make(Band)
        band.save()
        album = mommy.make(Album, band=band)
        album.save()
        user = mommy.make(User)
        user.save()
        self.review = mommy.make(Review, author=user, album=album)

    def test_published_manager(self):
        past_date = timezone.now() - timedelta(days=7)
        self.review.published = past_date
        self.review.save()
        self.assertEqual(Review.published_objects.count(), 1)
        self.assertEqual(Review.scheduled_objects.count(), 0)
        self.assertEqual(Review.draft_objects.count(), 0)

    def test_scheduled_manager(self):
        future_date = timezone.now() + timedelta(days=7)
        self.review.published = future_date
        self.review.save()
        self.assertEqual(Review.published_objects.count(), 0)
        self.assertEqual(Review.scheduled_objects.count(), 1)
        self.assertEqual(Review.draft_objects.count(), 0)

    def test_draft_manager(self):
        self.review.published = None
        self.review.save()
        self.assertEqual(Review.published_objects.count(), 0)
        self.assertEqual(Review.scheduled_objects.count(), 0)
        self.assertEqual(Review.draft_objects.count(), 1)
