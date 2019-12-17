import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'ratonGato.settings')

import django
django.setup()
from django.contrib.auth.models import User
from datamodel.models import Game, Move, GameStatus


def test_query():

    # Vemos is existe un usuario con id = 10 y, si no, lo creamos
    user10 = User.objects.get_or_create(id=10)[0]
    if user10.username == "":
        user10.username = '10'
    user10.save()
    # Vemos is existe un usuario con id = 11 y, si no, lo creamos
    user11 = User.objects.get_or_create(id=11)[0]
    if user11.username == "":
        user11.username = '11'
    user11.save()

    game = Game(cat_user=user10)
    game.full_clean()
    game.save()

    ids = []

    games_only_one_user = Game.objects.filter(status=GameStatus.CREATED)
    print(" ---- Games with only one user ----")
    for g in games_only_one_user:
        ids.append(g.id)
        print(g)

    print(" ---- Añadimos el Ratón ----")
    ids.sort()
    game = Game.objects.filter(id=ids[0])[0]
    game.mouse_user = user11
    game.full_clean()
    game.save()
    print(game)

    print(" ---- Movemos el cat2 a la posición 11 ----")
    Move.objects.create(game=game, player=user10, origin=game.cat2, target=11)
    game.full_clean()
    game.save()
    print(game)

    print(" ---- Movemos el Mouse a la posición 52 ----")
    Move.objects.create(game=game, player=user11, origin=game.mouse, target=52)
    game.full_clean()
    game.save()
    print(game)


test_query()
