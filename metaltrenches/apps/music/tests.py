from django.test import TestCase

from .models import Genre


class GenreTests(TestCase):
    def test_make_slug(self):
        """
        tests that slugs are at most 20 chars and don"t end with a dash
        """
        # trim to 30 chars
        name1 = "a" * 40
        expected_name1 = "a" * 20
        genre1 = Genre.objects.create(name=name1)
        self.assertEqual(genre1.slug, expected_name1)
        # doesn't end with a dash
        name2 = "a" * 19 + " type of music"
        expected_name2 = "a" * 19
        genre2 = Genre.objects.create(name=name2)
        self.assertEqual(genre2.slug, expected_name2)
