# 'Question' is one of the ten questions asked on NBA Pickem. find_stat(question) searches for the relevant stat

def find_stat(question):
    if 'win' in question:
        stat = 'winner'
    elif 'rebounds' in question:
        stat = 'rebounds'
    elif 'assists' in question:
        stat = 'assists'
    elif 'steals' in question:
        stat = 'steals'
    elif 'block' in question:
        stat = 'blocks'
    elif 'field goal' in question:
        stat = 'field goal'
    elif '3 pointers' in question or '3-pointers' in question:
        stat = '3 pointers'
    elif 'free throws' in question:
        stat = 'free throws'
    elif 'points' in question:
        stat = 'points'
    else:
        return 'ERROR: Question not recognized'

    return stat
