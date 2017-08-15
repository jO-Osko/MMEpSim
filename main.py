#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

from matplotlib import cm
from matplotlib.mlab import bivariate_normal
from numpy import meshgrid, linspace
from numpy.ma import arange
import numpy as np
from models.Board import Board, BoardConfig
from models.Disease import Measles

import matplotlib

from models.Person import InfectionStatus

matplotlib.use('TkAgg')  # do this before importing pylab
import time
import matplotlib.pyplot as plt

__author__ = "Filip Koprivec"
__email__ = "koprivec.fili@gmail.com"

"""
Glavni program
"""

from models.Country import Slovenia


def main() -> bool:
    t = time.time()
    board = Board.create_board(Slovenia, Measles, BoardConfig(cell_ratio=10))
    print(time.time() - t)

    fig = plt.figure()
    print(board.height ** 2)
    board.manually_infect([(board.height // 2, board.width // 2)])
    tmp = plt.imshow(board.to_np_image_array(), interpolation='nearest', cmap="jet")
    del tmp
    fig.canvas.draw()

    step = 0

    def animate():
        nonlocal step
        step += 1
        print("Step:", step)
        t = time.time()
        print("\n".join(
            map(str, board.simulate_steps(10)))
        )
        plt.clf()
        tmp = plt.imshow(board.to_np_image_array(), interpolation='nearest', cmap="jet")
        del tmp
        fig.canvas.draw()
        print(time.time() - t)
        time.sleep(0.1)
        fig.canvas.manager.window.after(100, animate)

    fig.canvas.manager.window.after(100, animate)
    plt.show()

    return True


if __name__ == "__main__":
    main()
