import sys
import race
import os

standings = race.Standings()

Butternut = race.Race('Butternut')
Butternut.load_races('butternut.csv')
standings.addRace(Butternut)

Easton = race.Race('Easton')
Easton.load_races('easton.csv')
standings.addRace(Easton)

Wachusett = race.Race('Wachusett')
Wachusett.load_races('wachusett.csv')
standings.addRace(Wachusett)

Blandford = race.Race('Blandford')
Blandford.load_races('blandford.csv')
standings.addRace(Blandford)

#BerkshireEast = race.Race('BerkshireEast')
#BerkshireEast.load_races('BerkshireEast.csv')
#standings.addRace(BerkshireEast)

standings.saveStandings()

