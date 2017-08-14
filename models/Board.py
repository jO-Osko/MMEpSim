#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Osnovni model za mrežo države
"""
from math import ceil

import numpy
from random import random
from typing import Tuple, List, Any, Optional

from models.Country import Country
from models.Disease import Disease
from models.Person import Person, InfectionStatus

__author__ = "Filip Koprivec"
__email__ = "koprivec.filip+template@gmail.com"


class Board:
    """
    
    """
    __slots__ = ("country", "disease", "width", "height", "board", "board_config")

    def __init__(self, country: Country, disease: Disease, board_config: "BoardConfig") -> None:
        self.country = country
        self.disease = disease
        self.board_config = board_config
        self.width, self.height = Board.calculate_dimensions(self.country, self.board_config.cell_ratio)
        self.board = []  # type: List[List[Person]]

    def init_board(self) -> None:
        """
        Inicializira mrežo
        :return: None
        """
        self.board = [[Person.from_country_data(self.country) for _ in range(self.width)] for _ in range(self.height)]

    def to_np_image_array(self) -> Any:
        """
        Pretvori mrežo v polje barv
        :return: Polje barv
        """
        return numpy.array(
            [[self.board_config.get_color(person) for person in line] for line in self.board], dtype="float32")

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
        if self.board[i][j].infection_status == InfectionStatus.NOT_INFECTED:
            do_infect = random() < self.disease.disease_info.infection_chance
            if do_infect:
                infected = self.board[i][j].__copy__()
                infected.infection_status = InfectionStatus.CURRENTLY_INFECTED
                return infected
        return None

    def next_step(self) -> None:
        """
        Simulira en korak/dan v modelu
        :return: None
        """
        # Promote to deque if necessary
        changes = []  # type: List[Tuple[int, int, Person]]

        distance = int(ceil(self.disease.disease_info.infectious_distance / self.board_config.cell_ratio) + 1)

        latent = self.disease.disease_info.latent_period
        infectious = self.disease.disease_info.infectious_period
        incubation = self.disease.disease_info.incubation_period
        max_duration = self.disease.disease_info.sickness_period + self.disease.disease_info.incubation_period
        mortality_chance = self.disease.disease_info.mortality_chance
        for line_i, line in enumerate(self.board):
            for col_i, person in enumerate(line):
                # Only infected people interest us
                if person.infection_status != InfectionStatus.CURRENTLY_INFECTED:
                    continue
                # Infect others
                if latent <= person.infection_duration <= infectious:
                    # Do infections
                    for dst in range(1, distance+1):
                        # Handle corner cases by hand
                        # Top
                        dy = -dst
                        temp = self.infect_target(line_i + dy, col_i, dst)
                        if temp is not None:
                            #if line_i + dy > 0:
                            #    self.board[line_i + dy][col_i] = temp
                            #else:
                                changes.append((line_i + dy, col_i, temp))

                        # Bottom
                        dy = dst
                        temp = self.infect_target(line_i + dy, col_i, dst)
                        if temp is not None:
                            changes.append((line_i + dy, col_i, temp))

                        for dy in range(-dst + 1, dst):
                            # Right
                            dx = abs(dst - abs(dy))
                            temp_right = self.infect_target(line_i + dy, col_i + dx, dst)
                            if temp_right is not None:
                                #if dy < 0 and line_i + dy > 0:
                                #    self.board[line_i + dy][(col_i + dx) % self.width] = temp_right
                                #else:
                                    changes.append((line_i + dy, col_i + dx, temp_right))

                            # Left
                            dx = -dx
                            temp_left = self.infect_target(line_i + dy, col_i + dx, dst)
                            if temp_left is not None:
                                #if dy < 0 and line_i + dy > 0:
                                #    self.board[line_i + dy][(col_i + dx) % self.width] = temp_left
                                #else:
                                    changes.append((line_i + dy, col_i + dx, temp_left))
                # Die
                if person.infection_duration > incubation and random() < mortality_chance:
                    person.infection_status = InfectionStatus.DEAD
                    continue
                # Update info
                person.infection_duration += 1
                if person.infection_duration > max_duration:
                    person.infection_status = InfectionStatus.PREVIOUSLY_INFECTED
        print("Changes:", len(changes))
        for i, j, person in changes:
            self.board[i % self.height][j % self.width] = person

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
    __slots__ = ("cell_ratio", "dead", "healthy", "infected")

    def __init__(self, cell_ratio: int = 5) -> None:
        self.cell_ratio = cell_ratio

        self.dead = 0.5  # (0, 0, 0)
        self.healthy = 0.0  # (0, 0, 1)
        self.infected = 1.0  # (1, 0, 0)

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
