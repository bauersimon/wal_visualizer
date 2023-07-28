from sys import argv

OK = '\033[32m'
FAIL = '\033[91m'
ENDC = '\033[0m'


def test(name, expected, actual):
    if not "test" in argv:
        return
    elif not expected == actual:
        print(f"{FAIL}FAIL{ENDC} {name}\nExpected:\t{expected}\nActual:\t\t{actual}")
    else:
        print(f"{OK}PASS{ENDC} {name}")
