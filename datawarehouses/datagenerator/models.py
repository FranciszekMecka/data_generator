from django.db import models

# Create your models here.

class Pracownik(models.Model):
    ID_pracownika = models.AutoField(primary_key=True)
    Imie = models.CharField(max_length=100)
    Nazwisko = models.CharField(max_length=100)
    Stanowisko = models.CharField(max_length=100)

class TrasaNarciarska(models.Model):
    ID_trasy = models.AutoField(primary_key=True)
    Poziom_trudnosci = models.CharField(max_length=100)
    Dlugosc_trasy = models.DecimalField(max_digits=5, decimal_places=2)

class NadzorTrasy(models.Model):
    ID_pracownika = models.ForeignKey(Pracownik, on_delete=models.CASCADE)
    ID_trasy = models.ForeignKey(TrasaNarciarska, on_delete=models.CASCADE)
    Data_nadzoru = models.DateField()

class ProblemNaStoku(models.Model):
    ID_problemu = models.AutoField(primary_key=True)
    ID_trasy = models.ForeignKey(TrasaNarciarska, on_delete=models.CASCADE)
    opis_problemu = models.TextField()
    data_zgloszenia = models.DateField()
    data_rozwiazania_problemu = models.DateField()

class PracaKonserwacyjna(models.Model):
    ID_pracy = models.AutoField(primary_key=True)
    ID_trasy = models.ForeignKey(TrasaNarciarska, on_delete=models.CASCADE)
    ID_konserwatora = models.ForeignKey(Pracownik, on_delete=models.CASCADE)
    opis_pracy = models.TextField()
    data_rozpoczecia = models.DateField()
    data_zakonczenia = models.DateField()

class Karnet(models.Model):
    rodzaj_karnetu = models.IntegerField()
    cena_karnetu = models.DecimalField(max_digits=5, decimal_places=2)

class SprzedazKarnetow(models.Model):
    ID_karnetu = models.AutoField(primary_key=True)
    PESEL_klienta = models.CharField(max_length=11)  # Assuming PESEL is an 11-character string
    rodzaj_karnetu = models.ForeignKey(Karnet, on_delete=models.CASCADE)
    data_zakupu = models.DateField()

class KlientLoyalty(models.Model):
    PESEL = models.CharField(max_length=11, primary_key=True)

class RejestrPrzejazdow(models.Model):
    ID_przejazdu = models.AutoField(primary_key=True)
    ID_trasy = models.ForeignKey(TrasaNarciarska, on_delete=models.CASCADE)
    ID_karnetu = models.ForeignKey(Karnet, on_delete=models.CASCADE)
    Data = models.DateField()
