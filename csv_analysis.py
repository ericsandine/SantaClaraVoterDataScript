"""
    pipenv run python csv_analysis --filename=11-4-14.xml
"""

import argparse
import csv
import clarify
import os
import pathlib
import re

p = clarify.Parser()
measure = re.compile('(Measure)(\\s+)(.)', re.IGNORECASE|re.DOTALL)
prop = re.compile('(Prop)(\\s+)(.)', re.IGNORECASE|re.DOTALL)
proposition = re.compile('(Proposition)(\\s+)(.)', re.IGNORECASE|re.DOTALL)

def transformName(name):
    if '-' in name:
        candidate_name = name.split('-')[1].strip().title()
        party = name.split('-')[0].strip().title()
        return '{0} ({1})'.format(candidate_name, party)
    else:
        return name.strip().title()

contests = {}
ballots = ['11-4-14.xml','11-3-15.xml', '11-8-16.xml']

for ballot in ballots:
    p.parse(os.getcwd() + '/' + ballot)
    print(p.election_name)
    for c in p.contests:
        if not measure.search(c.text) and not prop.search(c.text) and not proposition.search(c.text):
            transformed_title = None
            if 'mayor' in c.text.lower():
                transformed_title = c.text.split(',')[1].title().strip() + ' Mayor'
            elif 'member' in c.text.lower():
                transformed_title = c.text.split(',')[1].title().strip() + ' Member'
            else:
                transformed_title = c.text.title()
            sorted_choices = sorted(c.choices, key=lambda votes: votes.total_votes, reverse=True)
            for winner in range(c.vote_for):
                if contests.get(transformed_title):
                    contests[transformed_title].append({'name': transformName(sorted_choices[winner].text), 'elected': ballot.split('-')[2].split('.')[0]})
                else:
                    contests[transformed_title] = [{'name': transformName(sorted_choices[winner].text), 'elected': ballot.split('-')[2].split('.')[0]}]

# for c in contests:
#     print('-----------')
#     print(c)
#     for winner in contests[c]:
#         print(winner)

with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['Office', 'Jurisdiction', 'District', 'Officeholder', 'Date Up for Re-Election', 'On June ballot?', 'Date Elected'])
    for c in contests:
        for winner in contests[c]:
            writer.writerow([c, None, None, winner['name'], None, None, winner.get('elected')])
