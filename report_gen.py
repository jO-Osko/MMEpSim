#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Pomožni program za generiranje poročila
"""
from typing import List

from Simulation import Simulation, draw_analysis
from models.Board import BoardConfig
from models.Country import Country
from models.Disease import Measles

__author__ = "Filip Koprivec"
__email__ = "koprivec.filip+template@gmail.com"

random_seeds = [2017 - 2 * j for j in range(11, -1, -1)]


def generate_table(data) -> str:
    begin = """\\begin{table}[h]
\\centering
\\caption{Napis}
\\label{my-label}
\\begin{tabular}{|l||l|l|l|l|}
\\hline
\\backslashbox{seed}{atributi} & Število okuženih & Število mrtvih & Delež prizadete populacije \\\\ \\hline \\hline\n"""
    row = "{seed} & {infected} & {dead} & {affected} \\\\ \\hline\n"
    end = """\\end{tabular}
\\end{table}"""

    rtr = begin

    for sample in data:
        print(sample)
        rtr += row.format(seed=sample[0][1], infected=sample[3][1], dead=sample[4][1], affected=sample[7][1].replace("%", "\\%"))

    rtr += end

    return rtr


def generate_report(seeds: List[int], vacc_state: float, name: str) -> None:
    country = Country.create_Slovenia(vacc_state)
    disease = Measles
    board_config = BoardConfig(cell_ratio=10)

    data = []

    for seed in seeds:
        simulation = Simulation(country, disease, board_config, seed=seed)
        simulation_data = simulation.simulate(verbose=False)
        data.append(draw_analysis(simulation_data, simulation, show=False))

    print(name)
    print(generate_table(data))


def main() -> None:
    generate_report(random_seeds, 0.95, "PRECEPLJENI")
    # POZOR, TOLE TRAJA
    generate_report(random_seeds, 0.85, "PODCEPLJENI")


if __name__ == '__main__':
    main()
