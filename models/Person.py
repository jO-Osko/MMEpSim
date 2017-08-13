#!/usr/bin/env python
# -*- coding: utf-8 -*-
from enum import Enum, unique
from typing import List, Any, TypeVar, Type

from models.Country import Country
from models.random import select, random_weighted_select

__author__ = "Filip Koprivec"
__email__ = "koprivec.fili@gmail.com"

"""
Objekt ’Person’, ki predstavlja indiviualno osebo in z njo povezane funkcije 
ter pomožni objekti
"""
T = TypeVar("T", bound="ListableEnum")


class ListableEnum(Enum):
    @classmethod
    def items_g(cls: Type[T]) -> List[T]:
        cls_ = cls  # type: Any
        return list(cls_)


@unique
class AgeGroup(ListableEnum):
    """
    Objekt ki predstavlja starostno skupino osebka. Vrednosti oznake
    predstavljajo približne starostne meje in so odprte za dopolnjevanje.
    """
    CHILD = 0, 14
    ADULT = 15, 64
    OLD = 65, 100


AGE_GROUPS = AgeGroup.items_g()


@unique
class SexType(ListableEnum):
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


SEX_TYPES = SexType.items_g()


@unique
class InfectionStatus(ListableEnum):
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
class VaccinationStatus(ListableEnum):
    """
    Objekt, ki predstavlja trenutno stanje cepljenosti posameznika.
    Posameznik je lahko:
    NOT_VACCINATED: Posameznik ni cepljen
    FULLY_VACCINATED: Posameznik je primerno in popolnoma cepljen
    FRESHLY_VACCINATED: Posameznik je sveže cepljen, kar lahko negativno vpliva
    na uspešnost cepiva
    STALE_VACCINATION: Posameznik je bil cepljen dolgo nazaj, cepivo je lahko
    izgubilo moč/zaščito, ali pa je bil cepljen za drugačen sev bolezni.
    INEFFECTIVE_VACCINATION: Cepivo ni učinkovito
    """
    NOT_VACCINATED = 0
    FULLY_VACCINATED = 1
    FRESHLY_VACCINATED = 2
    STALE_VACCINATION = 3
    INEFFECTIVE_VACCINATION = 4


VACCINATION_TYPES = VaccinationStatus.items_g()


# See: https://en.wikipedia.org/wiki/Incubation_period#/media/File:Concept_of_incubation_period.svg

@unique
class DiseaseStatus(ListableEnum):
    """
    Objekt, ki predstavlja stanje bolezni
    Možni vrednosti:
    INCUBATION_PERIOD: Inkubacijska doba: posameznik je okužen, a se simptomi še niso pokazali
    DISEASE_PERIOD: Bolezen je razvita, simptomi so jasno vidni
    """
    INCUBATION_PERIOD = 0
    DISEASE_PERIOD = 1


@unique
class InfectivityStatus(ListableEnum):
    """
    Objekt, ki predstavlja stanje nalezljivosti človeka
    Možni vrednosti:
    NOT_INFECTIVE: Posameznik je v latentnem obdobju, sicer okužen, a ne prenaša (še) bolezni
    INFECTIVE: Posameznik lahko okuži druge
    """
    NOT_INFECTIVE = 0
    INFECTIVE = 1


class Person:
    """
    Objekt ’Person’ (oseba), ki vsebuje vse potrebne informacije o osebi
    """

    __slots__ = (
        "age_group", "sex_type", "infection_status", "disease_duration", "disease_status", "infectivity_status",
        "vaccination_status"
    )

    def __init__(self, age_group: AgeGroup = AgeGroup.ADULT, sex_type: SexType = SexType.WOMAN,
                 infection_status: InfectionStatus = InfectionStatus.NOT_INFECTED,
                 disease_duration: int = 0,
                 disease_status: DiseaseStatus = DiseaseStatus.INCUBATION_PERIOD,
                 infectivity_status: InfectivityStatus = InfectivityStatus.NOT_INFECTIVE,
                 vaccination_status: VaccinationStatus = VaccinationStatus.NOT_VACCINATED) \
            -> None:
        self.age_group = age_group
        self.sex_type = sex_type
        self.infection_status = infection_status
        self.disease_duration = disease_duration
        self.disease_status = disease_status
        self.infectivity_status = infectivity_status
        self.vaccination_status = vaccination_status

    @classmethod
    def from_country_data(cls, country: Country) -> "Person":
        """
        Naredi naklučno osebo
        :param country: podatki o državi
        :return: Naključna nova oseba
        """
        select = random_weighted_select
        age_group = select(AGE_GROUPS, country.age_distribution)
        sex_type = select(SEX_TYPES, country.sex_distribution)
        vaccination_status = select(VACCINATION_TYPES, country.vaccine_distribution)

        return cls(age_group, sex_type, vaccination_status=vaccination_status)


def main() -> bool:
    return True


if __name__ == "__main__":
    main()
