#!/usr/bin/python3
###############################################################################
#
#   Produce a specific scenario from an scenario definition
#
###############################################################################

import sys
import argparse
import yaml
import random

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
parser.add_argument('--mode', dest='mode', required=True)

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
        print(exc)
        sys.exit(1)

# Initialise the Trello API
trello = TrelloClient(
    api_key=trello['developer_public_key'],
    api_secret=trello['member_token']
)

board = trello.get_board('5d06060f86abdf60cfde5788')

def Rand(start, end, num):
    res = []

    for j in range(num):
        res.append(random.randint(start, end))

    return res

def generate(board):

    # Quick and dirty - create all the lists
    correct = board.add_list(name='Correct Actions')
    selected = board.add_list(name='Selected Actions')
    possible = board.add_list(name='Possible Actions')

    # Load in the scenario file
    with open(args.scenario, 'r') as stream:
        try:
            scenario = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)

    # init control sructures for pruning
    prunedActions=[]
    actionNames=[]
    actionCount = 0
    for action in scenario['actions']:
        actionNames.append(action['name'])
        actionCount += 1

    # Init presentation structure
    presentList = random.sample(range(1, actionCount+1), actionCount)

    # Process the scenario
    for action in scenario['actions']:

        # Collapse the set of outcomes for the action
        outPop = []
        outW = []
        for outcome in action['outcomes']:
            outPop.append(outcome['name'])
            outW.append(outcome['weight'])

        choice = random.choices(
            population=outPop,
            weights=outW,
            k=1
            )
        outcome = action['outcomes'][outPop.index(choice[0])]
        # Add the selected outcome for later use
        action['outcome'] = outcome

        # Add a card for the correct actions
        if action['name'] not in prunedActions:
            card = correct.add_card(
                    name=action['name'],
                    desc=outcome['text']
                    )
            # Add a URL if defined for the outcome
            if 'asset' in outcome:
                card.attach(
                        name='Outcome of action',
                        url=outcome['asset']
                        )
            # Add a URL if defined for the action
            if 'asset' in action:
                card.attach(
                        name='Action to take',
                        url=action['asset']
                        )

        # Prune correct actions if needed
        if 'blacklist' in outcome:
            for prune in outcome['blacklist']:
                prunedActions.append(prune)
        if 'whitelist' in outcome:
            for prune in actionNames:
                if prune not in outcome['whitelist']:
                    prunedActions.append(prune)

    # Generate the potential action list
    for idx in presentList:
        action = scenario['actions'][idx-1]
        outcome = action['outcome']
        # Add a card to the possible actions
        card = possible.add_card(
                name=action['name'],
                desc=outcome['text']
                )
        # Add a URL if defined for the outcome
        if 'asset' in outcome:
            card.attach(
                    name='Outcome of action',
                    url=outcome['asset']
                    )
        # Add a URL if defined for the action
        if 'asset' in action:
            card.attach(
                    name='Action to take',
                    url=action['asset']
                    )

        #card.add_checklist(
        #        title = 'Interpret the outcome',
        #        items = pop
        #        )


    return

def result(board):
    print('Not implemented')
    return

def destroy(board):
    # Archive all lists
    for list in board.list_lists():
        list.close()
    return

if args.mode == 'generate':
    print('Generating board...')
    generate(board)
elif args.mode == 'result':
    print('Resulting board...')
    result(board)
elif args.mode == 'destroy':
    print('Destroying board...')
    destroy(board)
else:
    print('Specify a mode')

# Bail out
sys.exit(0)

