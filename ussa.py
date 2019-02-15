import sys
import race
import os

print sys.argv[1]

print "hello world"

name, _ = os.path.splitext(os.path.basename(sys.argv[1]))

standings = race.Standings()


Butternut = race.Race('Butternut')
Butternut.load_races('butternut.csv')
standings.addRace(Butternut)

Wachusett = race.Race('Wachusett')
Wachusett.load_races('wachusett.csv')
standings.addRace(Wachusett)

Blandford = race.Race('Blandford')
Blandford.load_races('blandford.csv')
standings.addRace(Blandford)

BerkshireEast = race.Race('BerkshireEast')
BerkshireEast.load_races('BerkshireEast.csv')
standings.addRace(BerkshireEast)

standings.saveStandings()

