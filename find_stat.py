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
        stat = '3 pointers'
    elif 'free throws' in question:
        stat = 'free throws'
    elif 'points' in question:
        stat = 'points'
    else:
        return 'ERROR: Question not recognized'
    return stat

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'