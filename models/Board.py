#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Osnovni model za mrežo države
"""
from typing import Tuple, List

from models.Country import Country
from models.Disease import Disease
from models.Person import Person

__author__ = "Filip Koprivec"
__email__ = "koprivec.filip+template@gmail.com"


class Board:
    """
    
    """
    __slots__ = ("country", "disease", "cell_ratio", "width", "height", "board")

    def __init__(self, country: Country, disease: Disease, cell_ratio: int = 10) -> None:
        self.country = country
        self.disease = disease
        self.cell_ratio = cell_ratio
        self.width, self.height = Board.calculate_dimensions(self.country, self.cell_ratio)
        self.board = []  # type: List[List[Person]]

    def init_board(self) -> None:
        self.board = [[Person.from_country_data(self.country) for _ in range(self.width)] for _ in range(self.height)]

    @classmethod
    def create_board(cls, country: Country, disease: Disease, cell_ratio: int = 1):
        """
        Funkcija, ki priravi celotno mrežo in poskrbi za pravilno inicializacijo
        :param country: Država na keteri mreža temelji
        :param disease: Bolezen, za katero se bo izvajala simulacija
        :param cell_ratio: Število prebivalce, ki ga predstavlja posamezna celica
        :return: pripravljeno mrežo
        """
        board = cls(country, disease, cell_ratio)
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
