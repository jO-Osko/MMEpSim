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


Slovenia = Country(1_978_029, [0.51, 0.49], [0.1335, 0.677, 0.1895], [0.1, 0.70, 0.05, 0.1, 0.05])
