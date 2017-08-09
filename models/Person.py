#!/usr/bin/env python
# -*- coding: utf-8 -*-
from enum import Enum, unique

__author__ = "Filip Koprivec"
__email__ = "koprivec.fili@gmail.com"

"""
Objekt ’Person’, ki predstavlja indiviualno osebo in z njo povezane funkcije 
ter pomožni objekti
"""


@unique
class AgeGroup(Enum):
    """
    Objekt ki predstavlja starostno skupino osebka. Vrednosti oznake
    predstavljajo približne starostne meje in so odprte za dopolnjevanje.
    """
    CHILD = 0, 18
    ADULT = 19, 65
    OLD = 66, 100


@unique
class SexType(Enum):
    """
    Objekt SexType, ki predstavlja spol osebe. Za potrebe politične
    (ne)korektnosti predstavlja biološki spol, je fiksen in je striktno binaren.
    Možni vrednosti:
    WOMAN: Osebek je ženskega spola
    MAN: Osebek je moškega spola
    Podatek je pomemben za primerjanje širenja bolezni, ki se glede na spol
    razlikujejo (pri HPV virusu so moški zgolj prenašalci, medtem ko "zbolijo"
    zgolj ženske).
    """
    WOMAN = 0
    MAN = 1


@unique
class InfectionStatus(Enum):
    """
    Objekt, ki predstavlja trenutno stanje infekcije posameznika. Posameznik je
    lahko:
    NOT_INFECTED: Posameznik še ni bil okužen z virusom/bakterijo
    CURRENTLY_INFECTED: Posameznik je trenutno okužen
    PREVIOUSLY_INFECTED: Posameznik trenutno ni okužen, vendar je bil okužen
    v preteklosti

    Delitev na tri in ne zgolje dve različni stanji je pomembna zaradi možnosti
    ponovnih okužb, ali odpornosti na ponovno okužbo.
    """
    NOT_INFECTED = 0
    CURRENTLY_INFECTED = 1
    PREVIOUSLY_INFECTED = 2


@unique
class VaccinationStatus(Enum):
    """
    Objekt, ki predstavlja trenutno stanje cepljenosti posameznika.
    Posameznik je lahko:
    NOT_VACCINATED: Posameznik ni cepljen
    FULLY_VACCINATED: Posameznik je primerno in popolnoma cepljen
    FRESHLY_VACCINATED: Posameznik je sveže cepljen, kar lahko negativno vpliva
    na uspešnost cepiva
    STALE_VACCINATION: Posameznik je bil cepljen dolgo nazaj, cepivo je lahko
    izgubilo moč/zaščito, ali pa je bil cepljen za drugačen sev bolezni.

    """
    NOT_VACCINATED = 0
    FULLY_VACCINATED = 1
    FRESHLY_VACCINATED = 2
    STALE_VACCINATION = 3


class Person:
    """
    Objekt ’Person’ (oseba), ki vsebuje vse potrebne informacije o osebi
    """

    __slots__ = (
        "age_group", "sex_type", "infection_status", "vaccination_status"
    )

    def __init__(self, age_group: AgeGroup = AgeGroup.ADULT,
                 sex_type: SexType = SexType.WOMAN,
                 infection_status: InfectionStatus = InfectionStatus.NOT_INFECTED,
                 vaccination_status: VaccinationStatus = VaccinationStatus.NOT_VACCINATED) \
            -> None:
        self.age_group = age_group
        self.sex_type = sex_type
        self.infection_status = infection_status
        self.vaccination_status = vaccination_status


def main() -> bool:
    return True


if __name__ == "__main__":
    main()
