from django.core.management.base import BaseCommand
from faker import Faker
from datagenerator.models import (
    Pracownik,
    TrasaNarciarska,
    NadzorTrasy,
    ProblemNaStoku,
    PracaKonserwacyjna,
    Karnet,
    SprzedazKarnetow,
    KlientLoyalty,
    RejestrPrzejazdow,
)
import random
from time import perf_counter

class Command(BaseCommand):
    help = 'Generate fake data'

    def handle(self, *args, **kwargs):
        time_start = perf_counter()
        fake = Faker('pl_PL')

        # Generate fake Pracownik (Employee) data
        pracownicy = [Pracownik(Imie=fake.first_name(), Nazwisko=fake.last_name(), Stanowisko=fake.job()) for _ in range(10000)]
        Pracownik.objects.bulk_create(pracownicy)

        # Generate fake TrasaNarciarska (Ski Route) data
        trasy = [TrasaNarciarska(Poziom_trudnosci=random.choice(['Łatwa', 'Średnia', 'Trudna']),
                                 Dlugosc_trasy=fake.random_int(min=100, max=10000) / 100) for _ in range(10000)]
        TrasaNarciarska.objects.bulk_create(trasy)

        # Generate fake NadzorTrasy (Route Supervision) data
        nadzor_trasy = [NadzorTrasy(ID_pracownika=Pracownik.objects.order_by('?').first(),
                                    ID_trasy=TrasaNarciarska.objects.order_by('?').first(),
                                    Data_nadzoru=fake.date_this_decade()) for _ in range(10000)]
        NadzorTrasy.objects.bulk_create(nadzor_trasy)

        # Generate fake ProblemNaStoku (Problem on the Slope) data
        problemy = [ProblemNaStoku(ID_trasy=TrasaNarciarska.objects.order_by('?').first(),
                                   opis_problemu=fake.text(max_nb_chars=200),
                                   data_zgloszenia=fake.date_this_decade(),
                                   data_rozwiazania_problemu=fake.date_this_decade()) for _ in range(10000)]
        ProblemNaStoku.objects.bulk_create(problemy)

        # Generate fake PracaKonserwacyjna (Maintenance Work) data
        prace_konserwacyjne = [PracaKonserwacyjna(ID_trasy=TrasaNarciarska.objects.order_by('?').first(),
                                                 ID_konserwatora=Pracownik.objects.order_by('?').first(),
                                                 opis_pracy=fake.text(max_nb_chars=200),
                                                 data_rozpoczecia=fake.date_this_decade(),
                                                 data_zakonczenia=fake.date_this_decade()) for _ in range(10000)]
        PracaKonserwacyjna.objects.bulk_create(prace_konserwacyjne)

        # Generate fake Karnet (Ticket) data
        karnety = [Karnet(rodzaj_karnetu=random.randint(1, 5), cena_karnetu=fake.random_int(min=50, max=300) / 100) for _ in range(10000)]
        Karnet.objects.bulk_create(karnety)

        # Generate fake SprzedazKarnetow (Ticket Sales) data
        sprzedaze_karnetow = [SprzedazKarnetow(PESEL_klienta=fake.unique.random_int(min=10000000000, max=99999999999),
                                               rodzaj_karnetu=Karnet.objects.order_by('?').first(),
                                               data_zakupu=fake.date_this_decade()) for _ in range(10000)]
        SprzedazKarnetow.objects.bulk_create(sprzedaze_karnetow)

        # Generate fake KlientLoyalty (Loyal Customers) data
        klienci_loyalty = [KlientLoyalty(PESEL=str(fake.unique.random_int(min=10000000000, max=99999999999))) for _ in range(10000)]
        KlientLoyalty.objects.bulk_create(klienci_loyalty)

        # Generate fake RejestrPrzejazdow (Ski Pass Register) data
        rejestr_przejazdow = []
        for _ in range(10000):
            trasa = TrasaNarciarska.objects.order_by('?').first()
            karnet_sprzedaz = SprzedazKarnetow.objects.order_by('?').first()
            rejestr_przejazdow.append(RejestrPrzejazdow(ID_trasy=trasa, ID_karnetu=karnet_sprzedaz.rodzaj_karnetu, Data=fake.date_this_decade()))

        RejestrPrzejazdow.objects.bulk_create(rejestr_przejazdow)
        time_finish = perf_counter()
        print(f"Total time {time_finish - time_start}")
