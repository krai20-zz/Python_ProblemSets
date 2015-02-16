def readTriggerConfig(filename):
    """
    Returns a list of trigger objects
    that correspond to the rules set
    in the file filename
    """
    # Here's some code that we give you
    # to read in the file and eliminate
    # blank lines and comments
    triggerfile = open(filename, "r")
    all = [ line.rstrip() for line in triggerfile.readlines() ]
    lines = []
    for line in all:
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line)

    for line in lines:
        line = line.split()
        if line[0] != 'ADD':
            trigger_definition = line[0]
        keyword = line[1]
        arg = line[1:]

        if

print readTriggerConfig('Triggers.txt')

