#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Osnovni model za bolezen
"""
from typing import Optional

__author__ = "Filip Koprivec"
__email__ = "koprivec.filip+template@gmail.com"


class Disease:
    """
    Objekt, ki predstavlje posamezno bolezen
    """

    __slots__ = ("name", "disease_info")

    def __init__(self, name: str, disease_info: "DiseaseInfo") -> None:
        self.name = name
        self.disease_info = disease_info


class DiseaseInfo:
    """
    Objekt, ki predstavlja epidemiološke značilnosti posamezne bolezni
    """

    __slots__ = (
        "incubation_period", "sickness_period", "latent_period", "infectious_period", "mortality_rate",
        "mortality_chance", "infection_rate", "infection_chance", "infectious_distance", "vaccine_modifier"
    )

    def __init__(self, incubation_period: int, sickness_period: int, latent_period: Optional[int],
                 infectious_period: Optional[int], mortality_rate: float, infection_rate: float,
                 infectious_distance: int, vaccine_modifier: float = 1.0) -> None:
        """
        Konstruktor
        :param incubation_period: Inkubacijska doba: Čas do pojavitve znakov bolezni
        :param sickness_period: Čas trajanja bolezni
        :param latent_period: Latentna doba: Čas do pojavitve nalezljivosti
        :param infectious_period: Čas, ko je posameznik nalezljiv
        :param mortality_rate: Verjetnost, da posameznik okužen z boleznijo umre 
        :param infection_rate: Verjetnost, da se nov posameznik okuži z boleznijo
        :param infectious_distance: Največja razdalija na kateri še lahko pride do okužbe
        :param vaccine_modifier: Uspešnost cepiva pri preprečevanju okužbe
        """
        self.incubation_period = incubation_period
        self.sickness_period = sickness_period
        self.latent_period = latent_period or self.incubation_period
        self.infectious_period = infectious_period or self.sickness_period
        self.mortality_rate = mortality_rate
        # Predpostavimo da je smrtnost bolezni po pojavitvi simptomov konstantna
        # Po sickness_period bo posameznik z verjetnostjo moralitiy_rate mrtev
        # (izboljšava: funkcija, ki predpiše smrtnost glede na razvoj bolezni)
        self.mortality_chance = 1 - (1 - self.mortality_rate) ** (1 / self.sickness_period)
        self.infection_rate = infection_rate
        # Enaka ideja kot pri smrtnosti
        self.infection_chance = 1 - (1 - self.infection_rate) ** (1 / self.infectious_period)
        # Možna izboljšava: Uporaba funkcije, ki ob večji oddaljenosti zmanjša možnost okužbe.
        self.infectious_distance = infectious_distance
        self.vaccine_modifier = vaccine_modifier


# Podatki: https://en.wikipedia.org/wiki/Measles
Measles = Disease("Measles, Ošpice", DiseaseInfo(11, 8, 11 - 4, 8, 1 / 400, 0.7, 30))
# Ob zadnjem izbruhu ošpic v Sloveniji je zbolelo 398 ljudi, za enega je bila bolezen usodna
# https://www.dnevnik.si/1042462427/slovenija/1042462427
