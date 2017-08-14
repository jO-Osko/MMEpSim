#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Modul, ki poenoti funkcije naključni števil, predpiše neke vrste vmesnike(interface)
"""
import random

from typing import List, TypeVar, Callable, Sequence

__author__ = "Filip Koprivec"
__email__ = "koprivec.filip+template@gmail.com"

T = TypeVar("T")

items_t = List[T]
weights_t = Sequence[float]


def random_weighted_select(items: items_t, p: List[float], rand_fun: Callable[[], float] = random.random) -> T:
    """Za hitrejše začetno generiranje, približno 40% hitreje"""
    r = rand_fun()
    cum_s = 0.0
    for ind, item in enumerate(items):
        cum_s += p[ind]
        if cum_s > r:
            return item
    return items[-1]


def random_select(seq: items_t, p: weights_t) -> T:
    """
    Funkcija, ki vrne prvi element pythonovega internega random.choices (funkcija za uteženi izbor števila).
    :param seq: Seznam elementov med katerimi izbiramo
    :param p: Seznam uteži za posamezni element iz seq
    :return: Saključno (uteženo) izbran element iz seznama seq
    """
    return random.choices(seq, p, k=1)[0]


def select(seq: items_t, p: weights_t, rand_choice: Callable[[items_t, weights_t], T] = random_select) -> T:
    """
    Funkcija, ki vrne (uteženo) naključno izbrano število izmed seq, pri tem za izbor uporabi funkcijo podano kot parameter rand_choice ali random_select, če le ta ni podana
    :param seq: Seznam elementov med katerimi izbiramo
    :param p: Seznam uteži za posamezni element iz seq
    :param rand_choice: Funkcija za uteženo izbiranje elementov
    :return: Naključno (uteženo) izbran element iz seznama seq
    """
    return rand_choice(seq, p)


def select_multiple(seq: items_t, p: weights_t, n: int,
                    rand_choice: Callable[[items_t, weights_t], T] = random_select) -> List[T]:
    """
    Funkcija, ki vrne seznam n (uteženo) naključno izbrano število izmed seq, pri tem za ibor uporabi funkcijo podano kot parameter rand_choice ali random_select, če le ta ni podana
    :param seq: Seznam elementov med katerimi izbiramo
    :param p: Seznam uteži za posamezni element iz seq
    :param n: Število elementov v vrnjenem seznamu
    :param rand_choice: Funkcija za uteženo izbiranje elementov
    :return: Seznam (uteženo) naključno izbranih elementov, dolžine n
    """
    return [select(seq, p, rand_choice) for _ in range(n)]
