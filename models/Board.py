#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Osnovni model za mrežo države
"""
from math import ceil

import numpy
from random import random
from typing import Tuple, List, Any, Optional, Iterable

from models.Country import Country
from models.Disease import Disease
from models.Person import Person, InfectionStatus, InfectivityStatus, DiseaseStatus
from models.PrintableStructure import PrintableStructure

__author__ = "Filip Koprivec"
__email__ = "koprivec.filip+template@gmail.com"


class Board:
    """
    Objekt, ki predstavlja celotno mrežo na kateri poteka simulacija
    """
    __slots__ = (
        "country", "disease", "width", "height", "board", "board_config", "infected_num", "dead_num", "alive_num",
        "infectious_num", "symptomatic_num", "touched_num", "step_num"
    )

    def __init__(self, country: Country, disease: Disease, board_config: "BoardConfig") -> None:
        self.country = country
        self.disease = disease
        self.board_config = board_config
        self.width, self.height = Board.calculate_dimensions(self.country, self.board_config.cell_ratio)
        self.board = []  # type: List[List[Person]]

        self.infected_num = 0
        self.infectious_num = 0
        self.symptomatic_num = 0
        self.dead_num = 0
        self.touched_num = 0

        self.step_num = 0

    @property
    def stopped(self) -> bool:
        """
        Preveri, ali se je simulacija ustavila
        :return: Ali se je ismulacija ustavila
        """
        return self.infected_num == 0

    def init_board(self) -> None:
        """
        Inicializira mrežo
        :return: None
        """
        self.board = [[Person.from_country_data(self.country) for _ in range(self.width)] for _ in range(self.height)]

    def manually_infect(self, coordinates: Iterable[Tuple[int, int]]) -> None:
        """
        Ročno okužimo nekaj posameznikov, da lahko pričnemo s simulacijo
        :param coordinates: Koordinate posameznikov
        :return: None
        """
        for i, j in coordinates:
            person = self.board[i][j]
            person.touched = True
            if person.infection_status != InfectionStatus.CURRENTLY_INFECTED:
                person.infection_status = InfectionStatus.CURRENTLY_INFECTED
                self.infected_num += 1

    def to_np_image_array(self) -> Any:
        """
        Pretvori mrežo v polje barv
        :return: Polje barv
        """
        return numpy.array(
            [[self.board_config.get_color(person) for person in line] for line in self.board], dtype="float32"
        )

    def to_final_np_image_array(self) -> Any:
        """
        Pretvori mrežo v polje barv
        :return: Polje barv
        """
        return numpy.array(
            [[self.board_config.get_final_color(person) for person in line] for line in self.board], dtype="float32"
        )

    def infect_target(self, i, j, distance) -> Optional[Person]:
        """
        Modelira okužbno novega posameznika
        :param i: y koordinata
        :param j: x koordinata
        :param distance: Razdalja od kužnega posameznika
        :return: Okužen posameznik ali None
        """
        # Think about reinfection
        i = i % self.height
        j = j % self.width
        person = self.board[i][j]
        if not person.touched:
            self.touched_num += 1
            person.touched = True
        if person.infection_status == InfectionStatus.NOT_INFECTED:
            do_infect = random() < self.disease.disease_info.infection_chance
            vaccine_effect = random() < person.vaccination_status.value
            if do_infect and vaccine_effect:
                infected = self.board[i][j].__copy__()
                infected.infection_status = InfectionStatus.CURRENTLY_INFECTED
                return infected
        return None

    def next_step(self) -> "SimulationStepData":
        """
        Simulira en korak/dan v modelu, vrne spremembe ki so se zgodile, negativne vrednosti predstavljajo manj ljudi
        :return: Objket ki predstavlja korak v simulaciji
        """

        self.step_num += 1

        if self.stopped:
            return SimulationStepData.create_empty()

        # Promote to deque if necessary
        newly_infected = []  # type: List[Tuple[int, int, Person]]

        newly_dead_num = 0
        newly_infected_num = 0
        newly_infectious_num = 0
        newly_symptomatic_num = 0
        touched = self.touched_num

        distance = int(ceil(self.disease.disease_info.infectious_distance / self.board_config.cell_ratio) + 1)

        latent = self.disease.disease_info.latent_period
        infectious_end = latent + self.disease.disease_info.infectious_period
        incubation = self.disease.disease_info.incubation_period
        max_duration = incubation + self.disease.disease_info.sickness_period
        mortality_chance = self.disease.disease_info.mortality_chance

        for line_i, line in enumerate(self.board):
            for col_i, person in enumerate(line):
                # Only infected people interest us
                if person.infection_status != InfectionStatus.CURRENTLY_INFECTED:
                    continue
                # Update status
                duration = person.infection_duration

                # Infectious
                if duration == latent:
                    person.infectivity_status = InfectivityStatus.INFECTIVE
                    newly_infectious_num += 1
                elif duration == infectious_end:
                    newly_infectious_num -= 1
                    person.infectivity_status = InfectivityStatus.NOT_INFECTIVE

                if duration == incubation:
                    person.disease_status = DiseaseStatus.SYMPTOMATIC_PERIOD
                    newly_symptomatic_num += 1
                elif duration == max_duration:
                    person.infection_status = InfectionStatus.PREVIOUSLY_INFECTED
                    person.disease_status = DiseaseStatus.INCUBATION_PERIOD
                    newly_symptomatic_num -= 1
                    # For now
                    newly_infected_num -= 1

                # Die
                if person.disease_status is DiseaseStatus.SYMPTOMATIC_PERIOD and random() < mortality_chance:
                    person.infection_status = InfectionStatus.DEAD
                    newly_symptomatic_num -= 1
                    newly_dead_num += 1
                    newly_infected_num -= 1
                    if person.infectivity_status is InfectivityStatus.INFECTIVE:
                        newly_infectious_num -= 1

                person.infection_duration += 1

                # Infect others

                if person.infectivity_status is InfectivityStatus.INFECTIVE:
                    # Do infections
                    for dst in range(1, distance + 1):
                        # Handle corner cases by hand
                        # Top
                        dy = -dst
                        temp = self.infect_target(line_i + dy, col_i, dst)
                        if temp is not None:
                            # if line_i + dy > 0:
                            #    self.board[line_i + dy][col_i] = temp
                            # else:
                            newly_infected.append((line_i + dy, col_i, temp))

                        # Bottom
                        dy = dst
                        temp = self.infect_target(line_i + dy, col_i, dst)
                        if temp is not None:
                            newly_infected.append((line_i + dy, col_i, temp))

                        for dy in range(-dst + 1, dst):
                            # Right
                            dx = abs(dst - abs(dy))
                            temp_right = self.infect_target(line_i + dy, col_i + dx, dst)
                            if temp_right is not None:
                                # if dy < 0 and line_i + dy > 0:
                                #    self.board[line_i + dy][(col_i + dx) % self.width] = temp_right
                                # else:
                                newly_infected.append((line_i + dy, col_i + dx, temp_right))

                            # Left
                            dx = -dx
                            temp_left = self.infect_target(line_i + dy, col_i + dx, dst)
                            if temp_left is not None:
                                # if dy < 0 and line_i + dy > 0:
                                #    self.board[line_i + dy][(col_i + dx) % self.width] = temp_left
                                # else:
                                newly_infected.append((line_i + dy, col_i + dx, temp_left))
                                # Update info

        for i, j, person in newly_infected:
            if self.board[i % self.height][j % self.width].infection_status != InfectionStatus.CURRENTLY_INFECTED:
                self.board[i % self.height][j % self.width] = person
            else:
                # Double infection
                newly_infected_num -= 1

        newly_infected_num += len(newly_infected)

        self.infected_num += newly_infected_num
        self.dead_num += newly_dead_num
        self.infectious_num += newly_infectious_num
        self.symptomatic_num += newly_symptomatic_num

        return SimulationStepData(self.step_num, self.infected_num, newly_infected_num, self.infectious_num,
                                  newly_infectious_num, self.symptomatic_num, newly_symptomatic_num, self.dead_num,
                                  newly_dead_num, self.touched_num, self.touched_num - touched)

    def simulate_steps(self, steps: int = 1) -> List["SimulationStepData"]:
        """
        Simulira več korakov
        :param steps: število korakov
        :return: Tabelo rezultatov posameznega koraka
        """
        return [self.next_step() for _ in range(steps)]

    @classmethod
    def create_board(cls, country: Country, disease: Disease, board_config: "BoardConfig") -> "Board":
        """
        Funkcija, ki priravi celotno mrežo in poskrbi za pravilno inicializacijo
        :param country: Država na keteri mreža temelji
        :param disease: Bolezen, za katero se bo izvajala simulacija
        :param board_config: Število prebivalce, ki ga predstavlja posamezna celica
        :return: pripravljeno mrežo
        """
        board = cls(country, disease, board_config)
        board.init_board()
        return board

    @staticmethod
    def calculate_dimensions(country: Country, cell_ratio: int, ratio: float = 1.0) -> Tuple[int, int]:
        """
        Vrne dimenzije plošče (širina, višina), ki so najbolj primerne za državo ob željenem razmerju širine in višine
        :param country: Država
        :param cell_ratio: Koliko prebivalcev predstavlja posamezna celica
        :param ratio: Razmerje širina/višina
        :return Dimenzije plošče
        """
        height = int((country.population / cell_ratio) ** 0.5)
        width = height
        return height, width


class BoardConfig:
    """
    Objket, ki združuje posamezne nastavitve simulacijske plošče
    """
    __slots__ = (
        "cell_ratio", "dead", "healthy", "infected", "final_dead", "final_touched", "final_infected", "final_untouched"
    )

    def __init__(self, cell_ratio: int = 5) -> None:
        self.cell_ratio = cell_ratio

        self.dead = 0.5  # (0, 0, 0)
        self.healthy = 0.0  # (0, 0, 1)
        self.infected = 1.0  # (1, 0, 0)

        self.final_dead = (0., 0., 0.)  # k
        self.final_infected = (1., 0., 0.)  # "r"
        self.final_touched = (0., 0., 1.)  # "b"
        self.final_untouched = (0., 1., 0.)  # "g"

    def get_color(self, person: Person) -> float:
        """
        Vrne barvo posameznika na mreži
        :param person: trenotno gledan posameznik
        :return: vrednost barve
        """
        if person.infection_status == InfectionStatus.DEAD:
            return self.dead
        if person.infection_status == InfectionStatus.CURRENTLY_INFECTED:
            return self.infected
        return self.healthy

    def get_final_color(self, person: Person) -> Tuple[float, float, float]:
        """
        Vrne natančjenšo barvo posameznika
        :param person: trenutno gledan posameznik
        :return: vrednost barve
        """
        if not person.touched:
            return self.final_untouched
        if person.infection_status == InfectionStatus.NOT_INFECTED:
            return self.final_touched
        if person.infection_status == InfectionStatus.DEAD:
            return self.final_dead
        return self.final_infected


class SimulationStepData(PrintableStructure):
    """
    Objekt ki predstavlja posamezen korak v simulaciji
    """
    __slots__ = (
        "step_num", "infected", "newly_infected", "infectious", "newly_infectious", "symptomatic", "newly_symptomatic",
        "dead", "newly_dead", "touched", "newly_touched"
    )

    __printable_name__ = "SimulationStepData"
    _formatter = "{name}({data})"

    __printable_fields__ = __slots__

    def __init__(self, step_num: int, infected: int, newly_infected: int, infectious: int, newly_infectious: int,
                 symptomatic: int, newly_symptomatic: int, dead: int, newly_dead: int, touched: int,
                 newly_touched: int) -> None:
        self.step_num = step_num
        self.infected = infected
        self.newly_infected = newly_infected
        self.infectious = infectious
        self.newly_infectious = newly_infectious
        self.symptomatic = symptomatic
        self.newly_symptomatic = newly_symptomatic
        self.dead = dead
        self.newly_dead = newly_dead
        self.touched = touched
        self.newly_touched = newly_touched

    @property
    def empty(self) -> bool:
        """
        Preveri ali je simulacijski korak 'prazen'
        :return: 
        """
        return self.step_num == -1

    @classmethod
    def create_empty(cls) -> "SimulationStepData":
        """
        Naredi 'prazen' rezultat (ko se je simulacija že končala)
        :return: Prazen rezultat
        """
        # Ne da se mi pisat -1 dovoljkrat
        return cls(*([-1] * len(cls.__slots__)))
