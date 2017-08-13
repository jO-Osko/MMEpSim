#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

from models.Board import Board
from models.Disease import Measles

__author__ = "Filip Koprivec"
__email__ = "koprivec.fili@gmail.com"

"""
Glavni program
"""

from models.Country import Slovenia


def main() -> bool:
    t = time.time()
    board = Board.create_board(Slovenia, Measles, 1)
    print(time.time() - t)
    return True


if __name__ == "__main__":
    main()
