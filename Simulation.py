#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main graphics simulation class
"""
import pickle
import matplotlib.pyplot as plt
from matplotlib import patches
from numpy import arange
from typing import Tuple, Iterable, List, Optional, IO

from models.Board import BoardConfig, Board, SimulationStepData
from models.Country import Country
from models.Disease import Disease

__author__ = "Filip Koprivec"
__email__ = "koprivec.filip+template@gmail.com"


class Simulation:
    def __init__(self, country: Country, disease: Disease, board_config: BoardConfig,
                 initial_infections: Optional[Iterable[Tuple[int, int]]] = None, seed: Optional[int] = None) -> None:
        if seed:
            import random
            random.seed(seed)

        self.seed = seed

        self.board = Board.create_board(country, disease, board_config)

        self.board.init_board()

        self.board.manually_infect(initial_infections or [(self.board.height // 2, self.board.width // 2)])

    def simulate_steps(self, steps: int = 10, verbose= True, save_file: Optional[IO[bytes]] = None) -> List[SimulationStepData]:
        results = []  # type: List[SimulationStepData]
        while not self.board.stopped and steps > 0:
            steps -= 1
            results.append(self.board.next_step())
            if verbose:
                print(results[-1].pp())
        if save_file is not None:
            pickle.dump(results, save_file)
        return results

    def simulate(self, verbose: bool = True, save_file: Optional[IO[bytes]] = None) -> List[SimulationStepData]:
        results = []  # type: List[SimulationStepData]
        while not self.board.stopped:
            results.append(self.board.next_step())
            if verbose:
                print(results[-1].pp())
            else:
                if self.board.step_num % 20 == 0:
                    print(results[-1].pp())
        if save_file is not None:
            pickle.dump((results, self), save_file)
        return results


# Analysis part
def draw_analysis(sim_steps: List[SimulationStepData], simulation: Simulation):
    def attribute_getter(attr_name: str) -> List[int]:
        return list(map(lambda x: getattr(x, attr_name), sim_steps))

    t = arange(sim_steps[-1].step_num)

    infected = attribute_getter("infected")
    infected_col = "r"
    inf_patch = patches.Patch(color=infected_col, label="Okuženi")
    infectious = attribute_getter("infectious")
    infectious_col = "m"
    infcs_patch = patches.Patch(color=infectious_col, label="Kužni")
    symptomatic = attribute_getter("symptomatic")
    symptomatic_col = "c"
    sym_patch = patches.Patch(color=symptomatic_col, label="Simptomatski")
    dead = attribute_getter("dead")
    dead_col = "k"
    dead_patch = patches.Patch(color=dead_col, label="Mrtvi")
    touched = attribute_getter("touched")
    touched_col = "b"
    touched_patch = patches.Patch(color=touched_col, label="Možnost okužbe")
    untouched_col = "g"
    untouched_patch = patches.Patch(color=untouched_col, label="Brez možnosti okužbe")
    f, (graph, img, report) = plt.subplots(1, 3)

    graph.set_title("Število posameznikov glede na stanje bolezni")

    graph.legend(handles=[inf_patch, infcs_patch, sym_patch, dead_patch])

    graph.plot(t, infected, infected_col, t, infectious, infectious_col, t, symptomatic, symptomatic_col, t, dead,
               dead_col)

    img.set_title("Zemljevid stanja okužbe ob koncu")

    img.legend(handles=[untouched_patch, touched_patch, inf_patch, dead_patch])

    img.imshow(simulation.board.to_final_np_image_array(), interpolation="nearest")

    report.set_title("Poročilo")

    report.axis("tight")
    report.axis("off")

    columns = ("Atribut", "Vrednost")

    inf_all = sum(infected)

    data = [
        ["Random seed", simulation.seed],
        ["Število celic", simulation.board.height * simulation.board.width],
        ["Ljudi v celici", simulation.board.board_config.cell_ratio],
        ["Skupaj okuženih", inf_all],
        ["Število mrtvih", simulation.board.dead_num],
        ["Število prebolelih", inf_all - simulation.board.dead_num],
        ["Število prizadetih", simulation.board.touched_num],
        ["Delež prizadete \n populacije",
         "{0:.3f}%".format(float(simulation.board.touched_num) / (simulation.board.height * simulation.board.width))]
    ]

    table = report.table(cellText=data, colLabels=columns, loc='center')

    table.auto_set_font_size(False)
    table.set_fontsize(14)
    table.scale(1, 2)

    try:
        mng = plt.get_current_fig_manager()
        mng.frame.Maximize(True)
    except:
        try:
            mng = plt.get_current_fig_manager()
            mng.window.showMaximized()
        except:
            try:
                mng = plt.get_current_fig_manager()
                mng.resize(*mng.window.maxsize())
            except:
                pass

    plt.show()


def main() -> bool:
    return True


if __name__ == "__main__":
    main()
