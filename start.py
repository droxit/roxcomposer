#!/usr/bin/env python3.5

import sys

# NOT USED ATM
# if a test framework is used and the test cases get more complex use and extend this


# execute tests
def tests():
    print('Starting tests...')

if __name__ == '__main__':
    task = sys.argv[1]

    if task is 'tests':
        tests()

