import random

#attack function
#phising
#dos
#data poisoning

def phish(pa):
    if random.random() < pa:
        print('Perform phish attack')
        print('phished successfully')
        return 0
    else:
        return 1

def dos(pa):
    if random.random() < pa:
        print('Perform DoS attack')
        print('transmission of local model')
        return 0
    else:
        return 1

def labelflip(pa):
    if random.random() < pa:
        print('Perform label flipping attack')
        print('label flipped')
        return 0
    else:
        return 1

def mp(pa):
    if random.random() < pa:
        print('Perform model poisoning attack')
        print('local model modified')
        return 0
    else:
        return 1


