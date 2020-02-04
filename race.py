import csv
import scipy.stats as ss
from operator import itemgetter
import math


class Standings:

    def __init__(self):
        self.u12 = []
        self.u14 = []
        self.numResults = 0
        self.resultList = []
        self.bestOf = 0

    def __addRaceGroup(self, results, group):
        for racer in group:
            idx = next((index for (index, d) in enumerate(results) if d['ID'] == racer['AthleteID']), None)
            if idx is None:
                idx = len(results)
                results += [{ 'ID': racer['AthleteID'], 'name': racer['Full Name'], 'ranks' : [990] * self.numResults}]
            results[idx]['ranks'][self.numResults-3:] = [racer['FirstRunRank'], racer['SecondRunRank'], racer['RaceTimeRank']]

        #look for racers that were not there
        for result in results:
            if len(result['ranks']) is not self.numResults:
                result['ranks'][self.numResults-3:] = [ 990, 990, 990]
            result['BestOf'] = sum(sorted(result['ranks'])[:self.bestOf])

        for idx, val in enumerate(list(ss.rankdata([d['BestOf'] for d in results], method='min'))):
            results[idx].update({'Rank': val})

    def addRace(self, race):
        self.resultList += [race.name + '-Run1', race.name + '-Run2', race.name + '-Comb']
        self.numResults += 3
        #self.bestOf = math.trunc(self.numResults / 2)
        self.bestOf = 5
        self.__addRaceGroup(self.u12, race.u12)
        self.__addRaceGroup(self.u14, race.u14)

    def __save_standing(self, filename, result):
        with open(filename, 'wb') as csvfile:
            fieldnames = ['FinishPlace', 'AthleteID', 'Full Name', 'BirthYear', 'FirstRun', 'FirstRunRank', 'SecondRun', 'SecondRunRank', 'RaceTime', 'RaceTimeRank']

            writer = csv.writer(csvfile)
            headers = ['Rank', 'Name', 'ID'] + self.resultList + ['Best of ' + str(self.bestOf)]
            writer.writerow(headers)
            for racer in sorted(result, key=itemgetter('Rank')):
                row = [racer['Rank'], racer['name'], racer['ID']] + racer['ranks'] + [racer['BestOf']]
                writer.writerow(row)

    def saveStandings(self):
        self.__save_standing('standings-u12.csv', self.u12);
        self.__save_standing('standings-u14.csv', self.u14);


class Race:

    def __init__(self, name):
        self.u12 = []
        self.u14 = []
        self.name = name;

    def _addRank(self, race, key):
        times = ["99:99.99" if d[key] == "" else d[key] for d in race]
        ranks = [990 if times[i] == "99:99.99" else d for i, d in enumerate(list(ss.rankdata(times, method='min')))]

        for idx, val in enumerate(race):
            val.update({key + "Rank": ranks[idx]})

    def print_race(self):
        for row in self.u12:
            print row

    def save_races(self, name):
        self.__save_race(name + "-U12" + ".csv", self.u12)
        self.__save_race(name + "-U14" + ".csv", self.u14)

    def __save_race(self, filename, race):
        with open(filename, 'wb') as csvfile:
            fieldnames = ['FinishPlace', 'AthleteID', 'Full Name', 'BirthYear', 'FirstRun', 'FirstRunRank', 'SecondRun', 'SecondRunRank', 'RaceTime', 'RaceTimeRank']

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')

            writer.writeheader()
            writer.writerows(sorted(race, key=itemgetter('RaceTimeRank')))

    def load_races(self, filename):

        with open(filename, mode='r') as csv_file:
            #skip first two line of file
            csv_file.next()
            csv_file.next()

            #read in race data
            csv_reader = csv.DictReader(csv_file)

            #split into u12 and u14
            for row in csv_reader:
                if row['BirthYear'] == '2006' or row['BirthYear'] == '2007':
                    self.u14.append(row)
                else:
                    self.u12.append(row)

            self._addRank(self.u12, 'FirstRun')
            self._addRank(self.u14, 'FirstRun')
            self._addRank(self.u12, 'SecondRun')
            self._addRank(self.u14, 'SecondRun')
            self._addRank(self.u12, 'RaceTime')
            self._addRank(self.u14, 'RaceTime')


