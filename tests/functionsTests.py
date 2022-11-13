from main import locateFrontAndBack

board = [
    ['C', 'C', 'D', 'D', 'D', 'N'],
    ['B', 'A', 'A', 'X', 'X', 'N'],
    ['B', 'O', 'O', 'P', 'P', 'N'],
    ['G', '.', '.', 'L', 'L', '.'],
    ['G', 'U', 'U', 'U', '.', 'R'],
    ['.', 'D', 'D', 'D', '.', 'R'],
]


def test_my_locator():
        testcases = [
            {
                "name": "A",
                "input": (0, 0),
                "expected": ((0, 0), (0, 1), (0, 'left'), (0, 'right'))
            },
            {
                "name": "B",
                "input": (0, 1),
                "expected": ((0, 0), (0, 1), (0, 'left'), (0, 'right'))
            },
            {
                "name": "C",
                "input": (0, 2),
                "expected": ((0, 2), (0, 4), (0, 'left'), (0, 'right'))
            },
            {
                "name": "D",
                "input": (0, 3),
                "expected": ((0, 2), (0, 4), (0, 'left'), (0, 'right'))
            },
            {
                "name": "D",
                "input": (0, 3),
                "expected": ((0, 2), (0, 4), (0, 'left'), (0, 'right'))
            },
            {
                "name": "E",
                "input": (0, 5),
                "expected": ((0, 5), (2, 5), (0, 'up'), (1, 'down'))
            },
            {
                "name": "F",
                "input": (1, 5),
                "expected": ((0, 5), (2, 5), (0, 'up'), (1, 'down'))
            },
            {
                "name": "G",
                "input": (2, 5),
                "expected": ((0, 5), (2, 5), (0, 'up'), (1, 'down'))
            },
            {
                "name": "H",
                "input": (3, 0),
                "expected": ((3, 0), (4, 0), (0, 'up'), (1, 'down'))
            },
            {
                "name": "I",
                "input": (4, 0),
                "expected": ((3, 0), (4, 0), (0, 'up'), (1, 'down'))
            },
            {
                "name": "J",
                "input": (3, 3),
                "expected": ((3, 3), (3, 4), (2, 'left'), (1, 'right'))
            },
            {
                "name": "K",
                "input": (4, 5),
                "expected": ((4, 5), (5, 5), (1, 'up'), (0, 'down'))
            },
            {
                "name": "I",
                "input": (5, 5),
                "expected": ((4, 5), (5, 5), (1, 'up'), (0, 'down'))
            },
            {
                "name": "J",
                "input": (5, 1),
                "expected": ((5, 1), (5, 3), (1, 'left'), (1, 'right'))
            },
            {
                "name": "J",
                "input": (5, 2),
                "expected": ((5, 1), (5, 3), (1, 'left'), (1, 'right'))
            },
            {
                "name": "J",
                "input": (5, 3),
                "expected": ((5, 1), (5, 3), (1, 'left'), (1, 'right'))
            },

        ]

        for case in testcases:
            actual = locateFrontAndBack(board, case["input"][0], case["input"][1])
            assert (case["expected"]) == actual