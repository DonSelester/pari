from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class Player(models.Model):
    account_number = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    full_name = models.CharField(max_length=250)
    birthday = models.DateField()
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=13, unique=True)
    balance = models.FloatField(default=0)
    frozen = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return str(self.account_number)

class Operation(models.Model):
    account_number = models.ForeignKey(Player, on_delete=models.CASCADE)
    date = models.DateTimeField()
    card = models.CharField(max_length=20)
    operation_type = models.CharField(max_length=50)
    transaction_amount = models.FloatField()

    def __str__(self):
        return str(self.account_number)

class Match(models.Model):
    date = models.DateTimeField()

    def __str__(self):
        return str(self.pk)

class KindOfSport(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Teams(models.Model):
    title = models.CharField(max_length=50)
    country = models.CharField(max_length=100)
    kind_sport = models.ForeignKey(KindOfSport, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Bet(models.Model):
    account_number = models.ForeignKey(Player, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    date = models.DateTimeField()
    bet_team = models.ForeignKey(Teams, on_delete=models.CASCADE)
    bet_amount = models.FloatField()

    def __str__(self):
        return str(self.account_number) + " - " + str(self.match)

class MatchMembers(models.Model):
    match = models.OneToOneField(Match, on_delete=models.CASCADE, primary_key=True)
    country_id = models.ForeignKey(Teams, related_name='country_id', on_delete=models.CASCADE)
    title_id = models.ForeignKey(Teams, related_name='title_id', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.match) + " : " + str(self.country_id) + " - " + str(self.title_id)

class League(models.Model):
    title = models.CharField(max_length=100)
    kind_sport = models.ForeignKey(KindOfSport, on_delete=models.CASCADE)
    year = models.IntegerField()

    def __str__(self):
        return self.title + " " + str(self.year)

class Tour(models.Model):
    match = models.OneToOneField(Match, on_delete=models.CASCADE, primary_key=True)
    league = models.ForeignKey(League, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.league) + " " + str(self.match)

class LeagueMembers(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    team = models.ForeignKey(Teams, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.league) + " " +  str(self.team)

class Winner(models.Model):
    match = models.OneToOneField(Match, on_delete=models.CASCADE, primary_key=True)
    team = models.ForeignKey(Teams, on_delete=models.CASCADE)

class Draw(models.Model):
    match = models.OneToOneField(Match, on_delete=models.CASCADE, primary_key=True)

class MatchKoef(models.Model):
    match_id = models.IntegerField(primary_key=True)
    bet_team_id = models.IntegerField()
    perc = models.IntegerField()
    koef = models.FloatField()

    class Meta:
        managed = False
        db_table = 'match_koef'

    def __str__(self):
        return str(self.match_id) + " " + str(self.bet_team_id)
