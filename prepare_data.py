import csv
from datetime import datetime

import numpy as np
#import rpy2.robjects as robjects
from scipy import linspace, polyfit

def compute_home_win_pct_all(rows, winner_col='Winner'):
    # Home
    line_wins = len([row for row in rows \
                         if row[winner_col] == 'Home'])
    line_losses = len([row for row in rows \
                           if row[winner_col] == 'Visitor'])
    line_ties = len([row for row in rows \
                           if row[winner_col] == 'Tie'])
    pct = (line_wins*1.0 / (len(rows))) if rows else 0.0
    return (line_wins, line_losses, line_ties, pct)


def get_team_names(rows):
    teams = set()
    for row in rows:
        teams.add(row['Home Team'])
    return sorted(list(teams))


def add_winners_to_row(row):
    """ calculate win/loss, straight and vs. spread and add it to row dict """
    hs = row['Home Score']
    vs = row['Visitor Score']
        
    if hs > vs:
        row['Winner'] = 'Home'
    elif hs == vs:
        row['Winner'] = 'Tie'
    else:
        row['Winner'] = 'Visitor'

    hs_w_line = hs - row['Line']
    if hs_w_line > vs:
        row['Line Winner'] = 'Home'
    elif hs_w_line == vs:
        row['Line Winner'] = 'Tie'
    else:
        row['Line Winner'] = 'Visitor'

    row['Diff'] = hs - vs


def get_data_rows(date_cutoff=None, csv_filename='data/nfl1978-2012.csv'):
    data_rows = []
    with open(csv_filename, 'rb') as f:
        for row in csv.DictReader(f):
            if not row or not row['Total Line'] or \
               row['Total Line'] == 'Total Line':  # skip extra header rows
                continue

            # strings to floats and dates
            for c in ('Home Score', 'Visitor Score', 'Line'):
                row[c] = float(row[c])
            row['Date'] = datetime.strptime(row['Date'], '%m/%d/%Y')
            add_winners_to_row(row)
            data_rows.append(row)
    #print 'read in %s rows' % len(data_rows)
    #print '%s' % data_rows[0]
    
    if date_cutoff:
        data_rows = [row for row in data_rows if row['Date'] > date_cutoff]
    return data_rows



if __name__ == "__main__":

    # only look back 15 years, from 1998 until 2013
    date_cutoff = datetime(1998, 1, 1)
    data_rows = get_data_rows(date_cutoff)
    print 'Got %s rows since %s' % (len(data_rows), date_cutoff)

    cleaned_filename = 'nfl_cleaned.csv'
    with open(cleaned_filename, 'wb') as f:
        csv_writer = csv.DictWriter(f, data_rows[0].keys())
        csv_writer.writeheader()
        for row in data_rows:
            csv_writer.writerow(row)
    print 'Wrote %s' % cleaned_filename

    team_filename = 'team_win_pct.csv'
    with open(team_filename, 'wb') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['team', 'wins', 'losses', 'ties', 'pct'])
        team_names = get_team_names(data_rows)
        for team in team_names:
            # filter by this team and compute win %
            data_rows2 = [row for row in data_rows if row['Home Team'] == team]
            w, l, t, pct = compute_home_win_pct_all(data_rows2, winner_col='Line Winner')
            print '%s home line W/L: %s - %s - %s (%0.2f%%)' % (team, w, l, t, pct)
            csv_writer.writerow([team, w, l, t, pct])


    for winner_col in ['Line Winner', 'Winner']:

        lines_filename = 'win_pct_%s.csv' % winner_col
        with open(lines_filename, 'wb') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(['line', 'wins', 'losses', 'ties',
                                 'pct', 'n'])

            print '='*10
            print '    %s' % winner_col
            lines = [(x/2.0 if x else 0.0) for x in range(-28,28)] # -14, -13.5, -13,  ..., 13.5, 14
            for line in lines:
                data_rows2 = [row for row in data_rows if row['Line'] == line]
                w, l, t, pct = compute_home_win_pct_all(data_rows2, winner_col=winner_col)
                print '[Line (%s)] All home line W/L: %s - %s - %s (%0.2f%%) n=%s' %\
                    (line, w, l, t, pct, len(data_rows2))
                csv_writer.writerow([line, w, l, t, pct, len(data_rows2)])

        print 'wrote %s' % lines_filename
