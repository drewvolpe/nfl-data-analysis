

import random

import numpy as np

def sim_run(num_teams=32, num_games=120):
    win_pcts = []
    for team_num in range(0, num_teams):
        wins = 0
        for game_num in range(0, num_games):
            if random.randint(0,1):  # heads they win
                wins += 1
        pct = wins / (num_games*1.0)
        win_pcts.append(pct)
    return win_pcts


def sim_runs(num_runs):
    """ returns list of std devs for running sim num_runs times """
    stds = []
    for i in range(0, num_runs):
        stds.append(np.std(sim_run()))
    return stds

