#!/usr/bin/python
###############################################################################
#
#   Produce a specific scenario from an scenario definition
#
###############################################################################

import sys
import argparse
import yaml

from trello import TrelloClient

###############################################################################
#
#   Initialisation
#   

# Parse commandline
parser = argparse.ArgumentParser(
  prog='scenario.py',
  description='Render a scenario for an scenario definition file'
  )

parser.add_argument('--scenarioFile', dest='scenario', required=True)
parser.add_argument('--trelloSecrets', dest='trello', required=True)

# Wrap the argument parse so we can return a 3 to the calling program
try:
  args = parser.parse_args()
except SystemExit:
  sys.exit(3)

# Load trello secrets
with open(args.trello, 'r') as stream:
    try:
        trello = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print exc
        sys.exit(1)

#print trello

# Initialise the Trello API
trello = TrelloClient(
    api_key=trello['developer_public_key'],
    api_secret=trello['member_token']
)

board = trello.get_board('5d06060f86abdf60cfde5788')
#print board

# Display board lists
lists = board.list_lists()

print lists

def generate(board):
    return

def result(board):
    return

def destroy(board):
    return

# Load in the scenario file
with open(args.scenario, 'r') as stream:
    try:
        scenario = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print exc
        sys.exit(1)

# Print it for s&g's
print scenario

# For each scenario, collapse the set of outcomes to produce a single path through the scenario
#for action in scenario['actions']:
#    # sum the outcome weights
#    print action;

# Bail out
sys.exit(0)

