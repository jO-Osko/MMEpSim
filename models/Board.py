#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Osnovni model za mrežo države
"""
import numpy
from typing import Tuple, List, Any

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

        self.dead = 0  # (0, 0, 0)
        self.healthy = 1  # (0, 0, 1)
        self.infected = 0.5  # (1, 0, 0)

    def get_color(self, person: Person) -> float:
        """
        Vrne barvo posameznika na mreži
        :param person: trenotno gledan posameznik
        :return: vrednost barve
        """
        if person.infectivity_status == InfectionStatus.DEAD:
            return self.dead
        if person.infectivity_status == InfectionStatus.CURRENTLY_INFECTED:
            return self.infected
        return self.healthy
