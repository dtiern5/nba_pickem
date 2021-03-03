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
    elif '3 pointers' or '3-pointers' in question:
        stat = '3 pointers'
    elif 'free throws' in question:
        stat = 'free throws'
    elif 'first points' in question:
        stat = 'first points'
    else:
        return 'ERROR: Question not recognized'
    return stat