#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Modul za model držav
"""

__author__ = "Filip Koprivec"
__email__ = "koprivec.filip+template@gmail.com"

from .random import weights_t


class Country:
    """
    Objekt ki predstavlja značilnosti posamezne države
    """
    __slots__ = (
        "population", "sex_distribution", "age_distribution", "vaccine_distribution"
    )

    def __init__(self, population: int, sex_distribution: weights_t, age_distribution: weights_t,
                 vaccine_distribution: weights_t) -> None:
        self.population = population
        self.sex_distribution = sex_distribution
        self.age_distribution = age_distribution
        self.vaccine_distribution = vaccine_distribution

    @classmethod
    def create_Slovenia(cls, vaccianted: float) -> "Country":
        return cls(1_978_029, [0.51, 0.49], [0.1335, 0.677, 0.1895],
                   [(1 - vaccianted), vaccianted * 0.90, vaccianted * 0.01, vaccianted * 0.04, vaccianted * 0.05])


Slovenia = Country.create_Slovenia(0.85)

# https://podatki.nijz.si/pxweb/sl/NIJZ%20podatkovni%20portal/NIJZ%20podatkovni%20portal__5%20Preventivni%20programi__5a%20Precepljenost%20prebivalstva/CEPI2.px/table/tableViewLayout1/?rxid=cb52104b-25cc-4376-af74-4ed313f29e7d
# https://podatki.nijz.si/pxweb/sl/NIJZ%20podatkovni%20portal/NIJZ%20podatkovni%20portal__5%20Preventivni%20programi__5a%20Precepljenost%20prebivalstva/CEPI1.px/table/tableViewLayout2/?rxid=cb52104b-25cc-4376-af74-4ed313f29e7d
