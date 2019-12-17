from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.shortcuts import redirect, reverse
from django.http import HttpResponseNotFound
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from datamodel.models import Counter, Game, GameStatus, Move
from django.contrib.auth.decorators import login_required
from datamodel import constants
from . import forms

# Create your views here.


def index(request):
    return render(request, 'mouse_cat/index.html')


def anonymous_required(f):
    def wrapped(request):
        if request.user.is_authenticated:
            return HttpResponseForbidden(errorHTTP(request,
                                         exception="Action restricted to\
                                                    anonymous users|Servicio\
                                                    restringido a usuarios\
                                                    anónimos"))
        else:
            return f(request)
    return wrapped


def errorHTTP(request, exception=None):
    context_dict = {"msg_error": "Action restricted to anonymous users|Servicio\
                    restringido a usuarios anónimos"}
    context_dict[constants.ERROR_MESSAGE_ID] = exception
    return render(request, "mouse_cat/error.html", context_dict)


@anonymous_required
def user_register(request):
    # A boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = forms.SignupForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Update our variable to indicate that the template
            # registration was successful.
            return user_login(request)
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            return render(request,
                          'mouse_cat/signup.html',
                          {'user_form': user_form})
            # print(user_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        user_form = forms.SignupForm(data=request.POST)
        return render(request,
                      'mouse_cat/signup.html',
                      {'user_form': user_form})


@anonymous_required
def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed
        # to request.POST['<variable>'], because the
        # request.POST.get('<variable>') returns None if the
        # value does not exist, while request.POST['<variable>']
        # will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value),no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                # Inicializamos a 0 el counter de la session
                request.session['counter'] = 0
                return redirect(reverse('index'))
            else:
                # An inactive account was used - no logging in!
                return render(request, 'mouse_cat/login.html', {"user_form":
                              AuthenticationForm, "return_service":
                              "Username/password is not valid|Usuario/clave\
                               no válidos"})
        else:
            # Bad login details were provided. So we can't log the user in.
            formul = AuthenticationForm("Username/password is not\
                                        valid|Usuario/clave no válidos")
            return render(request, 'mouse_cat/login.html',
                          {"user_form": formul,
                           "return_service": "Username/password is not\
                            valid|Usuario/clave no válidos"})

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'mouse_cat/login.html',
                      {"user_form": AuthenticationForm})


@login_required
def user_logout(request):
    logout(request)
    # Inicializamos a 0 el counter de la session
    request.session['counter'] = 0
    return redirect(reverse('index'))


def counter_service(request):
    if 'counter' in request.session:
        request.session['counter'] = request.session['counter'] + 1
    else:
        # Si no había un campo counter, lo inicializamos a 1,
        # porque al ejecutar este service hacemos una peticion
        request.session['counter'] = 1

    Counter.objects.inc()
    # super(Counter, counter_global).save()

    return render(request, 'mouse_cat/counter.html',
                  {'counter_session': request.session['counter'],
                   'counter_global': Counter.objects.all()[0]})


@login_required
def select_game_service(request, game_id=None):
    user = request.user
    context_dict = {}
    if not game_id:
        as_cat = Game.objects.filter(cat_user=user, status=GameStatus.ACTIVE)
        if as_cat:
            context_dict['as_cat'] = as_cat
        as_mouse = Game.objects.filter(mouse_user=user,
                                       status=GameStatus.ACTIVE)
        if as_mouse:
            context_dict['as_mouse'] = as_mouse
        return render(request, 'mouse_cat/select_game.html', context_dict)
    else:
        game = Game.objects.filter(id=game_id).first()
        if (not game or game.status != GameStatus.ACTIVE or
           (game.cat_user != user and game.mouse_user != user)):
            return HttpResponseNotFound(errorHTTP(request,
                                                  "Game does not exist"))
        request.session['game_id'] = game.id
        render(request, 'mouse_cat/select_game.html', {"game": game})
        return redirect(reverse('show_game'))


@login_required
def move_service(request):
    if request.method == "POST":

        if constants.GAME_SELECTED_SESSION_ID not in request.session:
            return HttpResponseNotFound()

        else:

            gameid = request.session['game_id']

            game = Game.objects.get(id=gameid)

            if game.cat_turn:
                jug = game.cat_user
            else:
                jug = game.mouse_user

            pos_ini = request.POST.get('origin')
            pos_fin = request.POST.get('target')

            Move.objects.create(game=game,
                                origin=pos_ini,
                                target=pos_fin,
                                player=jug)
            game.save()

            return redirect(reverse('show_game'))

    return HttpResponseNotFound()


@login_required
def create_game_service(request):
    user = request.user  # Obtained the user
    # Create the game with the user as cat
    game = Game.objects.create(cat_user=user)
    game.save()
    return render(request, 'mouse_cat/new_game.html', {"game": game})


@login_required
def join_game_service(request):
    us = request.user
    # usamos -id ya que tiene que ser el de mayor id, no jugar contra ti mismo
    game = Game.objects.filter(status=GameStatus.CREATED).exclude(cat_user=us)
    game = game.filter(mouse_user=None).order_by('-id')

    if not game:
        return render(request, 'mouse_cat/join_game.html',
                      {"game": game, "msg_error":
                       constants.JOIN_GAME_ERROR_NOGAME})
    else:
        n_game = game.first()
        n_game.mouse_user = us
        n_game.save()
        return render(request, 'mouse_cat/join_game.html', {"game": n_game})


@login_required
def show_game_service(request):
    if 'game_id' in request.session:
        game_id = request.session['game_id']
    else:
        return render(request, 'mouse_cat/error.html', {"msg_error": "No games\
                      selected | No hay juegos seleccionados"})

    game = Game.objects.filter(id=game_id).first()

    if not game:
        return render(request, 'mouse_cat/error.html', {"msg_error": "No games\
                      selected | No hay juegos seleccionados"})

    gatos = [game.cat1, game.cat2, game.cat3, game.cat4]
    board = [0] * 64
    for i in range(64):
        if i in gatos:
            board[i] = 1
        if i == game.mouse:
            board[i] = -1

    moveform = forms.MoveForm()
    context_dict = {"game": game, "board": board, "move_form": moveform}
    return render(request, 'mouse_cat/game.html', context_dict)
