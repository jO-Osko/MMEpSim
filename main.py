#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

from matplotlib import cm
from matplotlib.mlab import bivariate_normal
from numpy import meshgrid, linspace
from numpy.ma import arange
import numpy as np
import os

import pickle

from Simulation import Simulation, draw_analysis
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
    # Initialize data

    country = Slovenia
    disease = Measles
    board_config = BoardConfig(cell_ratio=10)
    seed = 10

    experiment_name = "Slovenia-Measels-10-10.pickle"
    folder = "experiments"
    try:
        os.mkdir(folder)
    except OSError:
        pass
    file_name = os.path.join(folder, experiment_name)

    show_progress = False
    simulation_steps = 10

    simulation = Simulation(country, disease, board_config, seed=seed)

    loaded = False

    if show_progress:
        simulation_data = []

        def show_progressed():
            fig = plt.figure()

            tmp = plt.imshow(simulation.board.to_final_np_image_array(), interpolation='nearest')
            del tmp
            fig.canvas.draw()

            def animate():
                data = simulation.simulate_steps(simulation_steps, False)
                simulation_data.extend(data)
                print(data[-1].pp())
                plt.clf()
                tmp = plt.imshow(simulation.board.to_final_np_image_array(), interpolation='nearest')
                del tmp
                fig.canvas.draw()
                time.sleep(0.1)
                if simulation.board.stopped:
                    plt.close()
                    return
                fig.canvas.manager.window.after(100, animate)

            fig.canvas.manager.window.after(100, animate)
            plt.show()

        show_progressed()
    else:
        try:
            simulation_data, simulation = pickle.load(open(file_name, "rb"))
            loaded = True
        except:
            simulation_data = simulation.simulate(verbose=False)

    if not loaded:
        pickle.dump((simulation_data, simulation), open(file_name, "wb"))

    draw_analysis(simulation_data, simulation)

    return True


if __name__ == "__main__":
    main()
