from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


MSG_ERROR_INVALID_CELL = ("Invalid cell for a cat or the mouse|" +
                          "Gato o ratón en posición no válida")
MSG_ERROR_GAMESTATUS = "Game status not valid|Estado no válido"
MSG_ERROR_MOVE = "Move not allowed|Movimiento no permitido"
MSG_ERROR_NEW_COUNTER = "Insert not allowed|Inseción no permitida"
MSG_ERROR_CAT = "Cat not created|Gato no creado"


blanks = [0, 2, 4, 6, 9, 11, 13, 15, 16, 18, 20, 22, 25, 27, 29, 31, 32,
          34, 36, 38, 41, 43, 45, 47, 48, 50, 52, 54, 57, 59, 61, 63]


class GameStatus(models.Model):
    CREATED = 1
    ACTIVE = 2
    FINISHED = 3


class Game(models.Model):
    cat_user = models.ForeignKey(User,
                                 blank=True,
                                 null=True,
                                 related_name="games_as_cat",
                                 on_delete=models.CASCADE)
    mouse_user = models.ForeignKey(User,
                                   blank=True,
                                   null=True,
                                   related_name="games_as_mouse",
                                   on_delete=models.CASCADE)
    cat1 = models.IntegerField(blank=False, default=0)
    cat2 = models.IntegerField(blank=False, default=2)
    cat3 = models.IntegerField(blank=False, default=4)
    cat4 = models.IntegerField(blank=False, default=6)
    mouse = models.IntegerField(blank=False, default=59)
    cat_turn = models.BooleanField(default=True)
    status = models.IntegerField(default=GameStatus.CREATED, blank=False)
    MIN_CELL = 0
    MAX_CELL = 63

    def __str__(self):
        if self.status == 1:
            st = "Created"
            str2 = ("Cat [X] cat_user_test(" + str(self.cat1) + ", " +
                    str(self.cat2) + ", " + str(self.cat3) + ", " +
                    str(self.cat4) + ")")
        else:
            if self.cat_turn:
                str2 = ("Cat [X] cat_user_test(" + str(self.cat1) + ", " +
                        str(self.cat2) + ", " + str(self.cat3) + ", " +
                        str(self.cat4) + ") --- Mouse [ ] mouse_user_test(" +
                        str(self.mouse) + ")")
            else:
                str2 = ("Cat [ ] cat_user_test(" + str(self.cat1) + ", " +
                        str(self.cat2) + ", " + str(self.cat3) + ", " +
                        str(self.cat4) + ") --- Mouse [X] mouse_user_test(" +
                        str(self.mouse) + ")")
            if self.status == 2:
                st = "Active"
            else:
                st = "Finished"
        name = "(" + str(self.id) + ", " + st + ")" + "\t"
        return name + str2

    def clean(self):
        flag = 0
        tokens = [self.cat1, self.cat2, self.cat3, self.cat4, self.mouse]

        if self.cat_user is None:
            raise ValidationError(MSG_ERROR_CAT)

        if self.mouse_user is None:
            pass
        else:  # both mouse and cat exist
            if self.status == GameStatus.CREATED:
                self.status = GameStatus.ACTIVE

        for token in tokens:
            if (token not in blanks):
                flag = 1
                break

        if flag != 1:
            return super(Game, self).clean()
        else:
            raise ValidationError(MSG_ERROR_INVALID_CELL)

    def save(self, *args, **kwargs):
        flag = 0
        tokens = [self.cat1, self.cat2, self.cat3, self.cat4, self.mouse]

        if self.cat_user is None:
            raise ValidationError(MSG_ERROR_CAT)

        if self.mouse_user is None:
            pass
        else:  # both mouse and cat exist
            if self.status == GameStatus.CREATED:
                self.status = GameStatus.ACTIVE

        for token in tokens:
            if (int(token) not in blanks):
                flag = 1
                break

        if flag != 1:
            return super(Game, self).save()
        else:
            raise ValidationError(MSG_ERROR_INVALID_CELL)


class Move(models.Model):
    origin = models.IntegerField(blank=True, default=0)
    target = models.IntegerField(blank=True, default=0)
    game = models.ForeignKey(Game,
                             blank=True,
                             null=True,
                             related_name="moves",
                             on_delete=models.CASCADE)
    player = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    date = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):

        cells = [int(self.game.mouse),
                 int(self.game.cat1),
                 int(self.game.cat2),
                 int(self.game.cat3),
                 int(self.game.cat4)]

        if (self.player != self.game.cat_user and
                self.player != self.game.mouse_user):
            raise ValidationError(MSG_ERROR_MOVE)

        if int(self.origin) not in cells:
            raise ValidationError(MSG_ERROR_MOVE)

        if int(self.target) in cells:
            raise ValidationError(MSG_ERROR_MOVE)

        derecha_abajo = int(self.origin) + 9
        izquierda_abajo = int(self.origin) + 7
        izquierda_arriba = int(self.origin) - 9
        derecha_arriba = int(self.origin) - 7

        moves_cat = (((int(self.target) == derecha_abajo) or
                     (int(self.target) == izquierda_abajo)) and
                     (int(self.target) in blanks))

        moves_mouse = (((int(self.target) == derecha_abajo) or
                       (int(self.target) == izquierda_abajo) or
                       (int(self.target) == izquierda_arriba) or
                       (int(self.target) == derecha_arriba)) and
                       (int(self.target) in blanks))

        condition_cat = (self.game.cat_turn and moves_cat and
                         int(self.origin) != int(self.game.mouse))
        condition_mouse = ((self.game.cat_turn is False) and moves_mouse and
                           int(self.origin) == int(self.game.mouse))

        condition = (condition_cat or condition_mouse)

        if (self.game.status == GameStatus.ACTIVE) and condition:
            try:
                if self.game.cat_turn:
                    if int(self.origin) == int(self.game.cat1):
                        (self.game.cat1) = (self.target)
                    if int(self.origin) == int(self.game.cat2):
                        (self.game.cat2) = (self.target)
                    if int(self.origin) == int(self.game.cat3):
                        (self.game.cat3) = (self.target)
                    if int(self.origin) == int(self.game.cat4):
                        (self.game.cat4) = (self.target)
                else:
                    if int(self.origin) == int(self.game.mouse):
                        (self.game.mouse) = (self.target)

                cats = [int(self.game.cat1), int(self.game.cat2),
                        int(self.game.cat3), int(self.game.cat4)]

                # Si ha acabado el juego
                # si sus únicos movimientos posibles estan ocupados por gatos
                mouse_lost = ((int(self.game.mouse)+9 in cats or
                               int(self.game.mouse)+9 not in blanks) and
                              (int(self.game.mouse)+7 in cats or
                               int(self.game.mouse)+7 not in blanks) and
                              (int(self.game.mouse)-9 in cats or
                               int(self.game.mouse)-9 not in blanks) and
                              (int(self.game.mouse)-7 in cats or
                               int(self.game.mouse)-7 not in blanks))

                # El ratón supera la posición de los gatos o llega al fina del
                # tablero
                mouse_win = ((int(self.game.mouse) < int(self.game.cat1) and
                              int(self.game.mouse) < int(self.game.cat2) and
                              int(self.game.mouse) < int(self.game.cat3) and
                              int(self.game.mouse) < int(self.game.cat4)) or
                             (int(self.game.mouse) in [0, 2, 4, 6]))

                # Ratón pierde tras haber movido el gato, pasa a mover el raton
                if(mouse_lost and self.game.cat_turn is True):
                    self.game.status = GameStatus.FINISHED
                # Raton gana tras haber movido el mismo, pasa a mover el gato
                if(mouse_win and self.game.cat_turn is False):
                    self.game.status = GameStatus.FINISHED

                self.game.cat_turn = (not self.game.cat_turn)

                self.game.save()
                return super(Move, self).save()
            except ValidationError(MSG_ERROR_MOVE):
                raise
        else:
            raise ValidationError(MSG_ERROR_MOVE)


class CounterManager(models.Manager):

    def create(self, *args, **kwargs):
        raise ValidationError(MSG_ERROR_NEW_COUNTER)

    def inc(self):
        instances = Counter.objects.all()
        if not instances or not instances[0]:
            counter = Counter(value=1)
            super(Counter, counter).save()
            return 1

        else:
            counter = instances[0]
            current = counter.value + 1
            counter.value = current
            super(Counter, counter).save()
            return current

    def get_current_value(self):
        instances = Counter.objects.all()
        if not instances or not instances[0]:
            counter = Counter(value=0)
            super(Counter, counter).save()
            return 0
        else:
            counter = instances[0]
            return counter.value


class Counter(models.Model):
    value = models.IntegerField(blank=True, null=True)
    objects = CounterManager()

    def save(self, *args, **kwargs):
        raise ValidationError(MSG_ERROR_NEW_COUNTER)

    def __str__(self):
        return str(self.value)
