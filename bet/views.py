from django.shortcuts import render
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect
import datetime
from django.db.models import Q


def Index(request):
    wins = Winner.objects.all()
    drs = Draw.objects.all()
    if request.method == "GET":
        if 'league_id' in request.GET and request.GET['league_id']:
            new_l = request.GET.getlist('league_id')
            queries = [Q(pk=value) for value in new_l]
            query = queries.pop()
            for item in queries:
                query |= item
            leag_query = League.objects.filter(query)
        else:
            leag_query = ''
    kinds = KindOfSport.objects.all()
    leagues = League.objects.all()
    tours = Tour.objects.all()
    match_memb = MatchMembers.objects.all()
    context = {'kinds': kinds, 'leagues': leagues, 'tours': tours, 'match_memb': match_memb, 'leag_query': leag_query, 'wins': wins, 'drs': drs, }
    return render(request, 'bet/index.html', context)

def match_bet(request, m_id):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        try:
            bet = Bet.objects.get(match=m_id, account_number=request.user.pk)
        except Bet.DoesNotExist:
            bet = ''
            pass
        try:
            win = Winner.objects.get(match=m_id)
        except Winner.DoesNotExist:
            win = ''
            pass
        try:
            dr = Draw.objects.get(match=m_id)
        except Draw.DoesNotExist:
            dr = ''
            pass
        if request.method == "POST":
            acc = Player.objects.get(pk=request.user.pk)
            date = datetime.datetime.today()
            match = Match.objects.get(pk=m_id)
            bet_t = Teams.objects.get(pk=request.POST['bet_team'])
            b_amount = float(request.POST['bet_amount'])
            if (acc.balance-b_amount) >= 0:
                Bet(**dict([('account_number', acc), ('match', match), ('date', date),
                                  ('bet_team', bet_t),
                                  ('bet_amount', b_amount)])).save()
                Operation(**dict([('account_number', acc), ('date', date), ('card', "Ставка на матч №"+str(match.pk)),
                                  ('operation_type', "Списание"),
                                  ('transaction_amount', b_amount)])).save()
                Player.objects.filter(pk=acc.pk).update(balance=(acc.balance-b_amount))
                added = True
                return render(request, 'bet/match_bet.html', {'added': added})
            else:
                return render(request, 'bet/match_bet.html', {'error': "У вас нет такой суммы на балансе"})
        match_koef = MatchKoef.objects.filter(match_id=m_id)
        tour = Tour.objects.get(match=Match(pk=m_id))
        league = League.objects.get(pk=tour.league.pk)
        kind = KindOfSport.objects.get(pk=league.kind_sport.pk)
        match_memb = MatchMembers.objects.get(match=Match(pk=m_id))
        draw = Teams.objects.get(pk=7)
        context = {'kind': kind, 'league': league, 'tour': tour, 'match_memb': match_memb, 'draw': draw, 'bet': bet, 'win': win, 'dr': dr, 'match_koef': match_koef, }
        return render(request, 'bet/match_bet.html', context)

@login_required
def user_balance(request):
    operations = Operation.objects.filter(account_number=request.user.pk).order_by('-date')
    context = {'operations': operations }
    return render(request, 'bet/balance.html', context)

@login_required
def user_payin(request, type):
    if request.method == "POST":
        acc = Player.objects.get(pk=request.user.pk)
        date = datetime.datetime.today()
        t_amount = float(request.POST['transaction_amount'])
        Operation(**dict([('account_number', acc), ('date', date), ('card', request.POST['card']),
                          ('operation_type', "Зачисление"),
                          ('transaction_amount', t_amount)])).save()
        Player.objects.filter(pk=acc.pk).update(balance=(acc.balance+t_amount))
        added = True
        return render(request, 'bet/payin.html', {'added': added})
    if type == "card":
        card = "card"
        context = {'card': card, }
    elif type == "phone":
        phone = "phone"
        context = {'phone': phone, }
    elif type == "wm":
        wm = "wm"
        context = {'wm': wm, }
    else:
        return redirect('user_balance')
    return render(request, 'bet/payin.html', context)

@login_required
def user_payout(request, type):
    #context = {'player': player }
    return render(request, 'bet/payout.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('index')

def register(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        player_form = PlayerForm(data=request.POST)
        if user_form.is_valid() and player_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            player = player_form.save(commit=False)
            player.account_number = user
            player.save()

            registered = True
        else:
            print(user_form.errors, player_form.errors)
    else:
        user_form = UserForm()
        player_form = PlayerForm()

    return render(request, 'bet/register.html',
                  {'user_form': user_form,
                   'player_form': player_form,
                   'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return redirect('index')
            else:
                return HttpResponse('Account not active')
        else:
            print("Username: {} and password {}".format(username,password))
            return HttpResponse("Введен неправильный пароль или логин!")
    else:
        return render(request, 'bet/login.html')
