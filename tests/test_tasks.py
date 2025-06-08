from django.test import TestCase
from django.test.utils import override_settings
from unittest.mock import patch

from game.models import GameRound
from game.tasks import start_new_round

@override_settings(DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}})
class StartNewRoundTests(TestCase):
    @patch('game.tasks.generate_crash_point')
    def test_start_new_round_creates_record(self, mock_gen):
        mock_gen.return_value = 1.23
        round_obj = start_new_round()
        self.assertIsInstance(round_obj, GameRound)
        self.assertEqual(round_obj.crash_point, 1.23)
        self.assertTrue(GameRound.objects.filter(id=round_obj.id).exists())

