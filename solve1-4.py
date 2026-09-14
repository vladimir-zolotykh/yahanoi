def solve1():
    move(1, 3)


def solve2():
    move(1, 2)  # src -> tmp
    move(1, 3)  # src -> dst
    move(2, 3)  # tmp -> dst


def solve3():
    move(1, 3)  # src -> tmp
    move(1, 2)  # src -> dst
    move(3, 2)  # tmp -> dst
    move(1, 3)
    move(2, 1)
    move(2, 3)
    move(1, 3)


def solve4():
    move(1, 2)
    move(1, 3)
    move(2, 3)
    move(1, 2)
    move(3, 1)
    move(3, 2)
    move(1, 2)
    move(1, 3)
    move(2, 3)
    move(2, 1)
    move(3, 1)
    move(2, 3)
    move(1, 2)
    move(1, 3)
    move(2, 3)
