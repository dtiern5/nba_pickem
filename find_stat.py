def find_stat(question):
    stat = None
    if 'win' in question:
        stat = 'win'
    elif 'rebounds' in question:
        stat = 'rebounds'
    elif 'assists' in question:
        stat = 'assists'
    elif 'steals' in question:
        stat = 'steals'
    elif 'block' in question:
        stat = 'block'
    elif 'field goal' in question:
        stat = 'field goal'
    elif '3 pointers' in question or '3-pointers' in question:
        stat = 'threes'
    elif 'free throws' in question:
        stat = 'free throws'
    elif 'points' in question:
        stat = 'points'
    else:
        return 'ERROR: Question not recognized'
    return stat