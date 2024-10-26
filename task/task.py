def task(file):
    file = open(file, 'w')
    for line in file:
        line += 1