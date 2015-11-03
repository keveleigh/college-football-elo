#!/usr/bin/env python

"""
This scrapes college football team information and calculates an all-time ELO.

In order to use this, you will need to download bs4, pygraph, pygraphviz, and graphviz.

Team dictionary format: {Team Name: [ESPN ID, FBS/FCS, Wins, Losses, ImageURL, {Opponent1: Outcome1, Opponent2: Outcome2, ... , OpponentN: OutcomeN}, [Opponent1, Outcome1], [Opponent2, Outcome2], ... , [OpponentN, OutcomeN]]}
ID dictionary format: {ESPN ID: Team Name}

Command format: python graphs.py reuse year school division
"""

import urllib.request
import re
import datetime
import sys
import ast
import os
import argparse

from bs4 import BeautifulSoup

allSchools = set()
allGames = {}

powerFive = ['Boston College',
             'Clemson',
             'Duke',
             'Florida State',
             'Georgia Tech',
             'Louisville',
             'Miami (FL)',
             'North Carolina',
             'North Carolina State',
             'Pittsburgh',
             'Syracuse',
             'Virginia',
             'Virginia Tech',
             'Wake Forest',
             'Baylor',
             'Iowa State',
             'Kansas',
             'Kansas State',
             'Oklahoma',
             'Oklahoma State',
             'TCU',
             'Texas',
             'Texas Tech',
             'West Virginia',
             'Illinois',
             'Indiana',
             'Iowa',
             'Maryland',
             'Michigan',
             'Michigan State',
             'Minnesota',
             'Nebraska',
             'Northwestern',
             'Ohio State',
             'Penn State',
             'Purdue',
             'Rutgers',
             'Wisconsin',
             'Arizona',
             'Arizona State',
             'California',
             'Colorado',
             'Oregon',
             'Oregon State',
             'Stanford',
             'UCLA',
             'USC',
             'Utah',
             'Washington',
             'Washington State',
             'Alabama',
             'Arkansas',
             'Auburn',
             'Florida',
             'Georgia',
             'Kentucky',
             'LSU',
             'Mississippi State',
             'Missouri',
             'Ole Miss',
             'South Carolina',
             'Tennessee',
             'Texas A&M',
             'Vanderbilt']
             
def get_games(school, schedule_link):
    global allGames
    
    url = urllib.request.urlopen(schedule_link)
    html = url.read().decode('windows-1252')
    html = fix_html(html)
    
    soup = BeautifulSoup(html, 'lxml')
    games = soup.findAll("td", {"height" : "18"})
    
    print(school)
    
    offset = 0
        
    for i in range(0,len(games)//2,7):
        # print games[i].text.strip()
        # print games[i+1].text.strip()
        # print games[i+2].text.strip()
        # print games[i+3].text.strip()
        # print games[i+4].text.strip()
        # print games[i+5].text.strip()
        # print games[i+6].text.strip()
        
        if(len(games[i + offset].attrs) < 2):
            offset = offset + 1
            
        i = i + offset
              
        key = games[i+1].text.strip()
        
        if(school < games[i+3].text.strip()):
            result = (school.strip(), int(games[i+2].text.strip()), games[i+3].text.strip(), int(games[i+4].text.strip()))
        else:
            result = (games[i+3].text.strip(), int(games[i+4].text.strip()), school.strip(), int(games[i+2].text.strip()))

        if key not in allGames:
            newValue = set()
            newValue.add(result)
            allGames[key] = newValue
        else:
            allGames[key].add(result)

def get_schedules(school, school_link):
    """Scrape cfbdatawarehouse's pages for data."""
    
    url = urllib.request.urlopen(school_link)
    html = url.read().decode('windows-1252')
    html = fix_html(html)
        
    soup = BeautifulSoup(html, 'lxml')
    schedule_links = soup.find_all(href=re.compile('yearly_results'))
    
    for link in schedule_links[:len(schedule_links)//2]:
        if('-20' in link.text):
            print(link.text)
            get_games(school, school_link[:len(school_link)-9] + link['href'])
    

def get_schools():
    global allSchools
    
    url = urllib.request.urlopen('http://www.cfbdatawarehouse.com/data/div_ia_team_index.php')
    html = url.read().decode('windows-1252')
    html = fix_html(html)
            
    soup = BeautifulSoup(html, 'lxml')  
    school_links = soup.find_all(href=re.compile('active/'))
    
    for school in school_links[:len(school_links)//2]:
        allSchools.add(school.text)
        get_schedules(school.text, 'http://www.cfbdatawarehouse.com/data/' + school['href'])

def fix_html(html):
    i = html.index('<html')
    while True:
        try:
            i=html.index('</html>', i+1)
            i2= html.index('<html', i)
            i3= html.index('>', i)            
            html= html[:i]+html[i+7:i2]+html[i3:]
        except ValueError:
            break           
    return html

def main():
    global allSchools
    global allGames
    
    parser = argparse.ArgumentParser()
    parser.add_argument('reuse', help='specify whether to use the cached data or scrape new data', choices=['reuse', 'scrape'], type=str)
    args = parser.parse_args()
    
    if args.reuse == 'reuse' and os.path.isfile('allGames.txt') and os.path.isfile('allSchools.txt'):
        schools = open('allSchools.txt', 'r')
        allSchools = ast.literal_eval(schools.read())
        games = open('allGames.txt', 'r')
        allGames = ast.literal_eval(games.read())
    elif args.reuse == 'reuse':
        print('There isn\'t any cached data. Please scrape first.')
        return
    else: 
        get_schools();
            
        f = open('allSchools.txt', 'w')
        f.write(str(allSchools))
        f.close()
        
        f = open('allGames.txt', 'w')
        f.write(str(allGames))
        f.close()

##    allScores = allScores.items()
##    allScores.sort(key=lambda x: float(x[1]))
##    for n,s in allScores:
##        print n + ': ' + str(s)

if __name__ == '__main__':
    import time
    start = time.time()
    main()
    print(time.time() - start, 'seconds')
