from datamodel.tests import BaseModelTest
from datamodel.models import Game, GameStatus, Move


class GameEndTests(BaseModelTest):
    def setUp(self):
        super().setUp()

    def test1(self):
        """Raton gana al llegar al final"""
        game = Game.objects.create(
            cat_user=self.users[0], mouse_user=self.users[1], status=GameStatus.ACTIVE)

        game.cat2 = 9
        game.cat3 = 18
        game.cat4 = 22
        game.mouse = 11
        game.save()

        Move.objects.create(game=game, player=self.users[0], origin=9, target=16)
        Move.objects.create(game=game, player=self.users[1], origin=11, target=4)

        self.assertEqual(game.status, GameStatus.FINISHED)

    def test2(self):
        """Raton gana al sobrepasar al último gato"""
        game = Game.objects.create(
            cat_user=self.users[0], mouse_user=self.users[1], status=GameStatus.ACTIVE)

        game.cat1 = 34
        game.cat2 = 31
        game.cat3 = 32
        game.cat4 = 45
        game.mouse = 36
        game.save()

        Move.objects.create(game=game, player=self.users[0], origin=31, target=38)
        Move.objects.create(game=game, player=self.users[1], origin=36, target=27)
        self.assertEqual(game.status, GameStatus.FINISHED)

    def test3(self):
        """Gatos ganan por inmovilizar ratón"""
        game = Game.objects.create(
            cat_user=self.users[0], mouse_user=self.users[1], status=GameStatus.ACTIVE)

        game.mouse = 41
        game.cat1 = 32
        game.cat2 = 34
        game.cat3 = 48
        game.cat4 = 43
        game.save()

        Move.objects.create(game=game, player=self.users[0], origin=43, target=50)
        self.assertEqual(game.status, GameStatus.FINISHED)

    def test4(self):
        """Gatos ganan por inmovilizar raton en la esquina"""
        game = Game.objects.create(
            cat_user=self.users[0], mouse_user=self.users[1], status=GameStatus.ACTIVE)

        game.cat1 = 41
        game.cat2 = 48
        game.cat3 = 29
        game.cat4 = 11
        game.mouse = 57
        game.save()

        Move.objects.create(game=game, player=self.users[0], origin=41, target=50)
        self.assertEqual(game.status, GameStatus.FINISHED)
