from main import locateFrontAndBack, numberOfBlockingVehiclesHeuristic, numberOfBlockingPositions, minClearable

board = [
    ['C', 'C', 'D', 'D', 'D', 'N'],
    ['B', 'A', 'A', 'X', 'X', 'N'],
    ['B', 'O', 'O', 'P', 'P', 'N'],
    ['G', '.', '.', 'L', 'L', '.'],
    ['G', 'U', 'U', 'U', '.', 'R'],
    ['.', 'D', 'D', 'D', '.', 'R'],
]



def test_my_h1():
    testcases = [
        {
            "name": "A",
            "input":  [
    ['B', '.', 'D', 'D', 'D', 'N'],
    ['B', '.', '.', 'X', 'X', 'N'],
    ['.', 'A', 'A', 'P', 'P', 'N'],
    ['G', '.', '.', 'L', 'L', '.'],
    ['G', 'U', 'U', 'U', '.', 'R'],
    ['.', 'D', 'D', 'D', '.', 'R'],],
            "expected": 2
        },
        {
            "name": "A",
            "input": [
                ['I', 'I', 'B', '.', '.', '.'],
                ['C', '.', 'B', 'H', 'H', 'H'],
                ['C', '.', 'A', 'A', 'D', '.'],
                ['.', '.', '.', '.', 'D', '.'],
                ['E', 'E', 'G', 'G', 'G', 'F'],
                ['.', '.', '.', '.', '.', 'F'], ],
            "expected": 1
        },
        {
            "name": "A",
            "input": [
                ['C', '.', 'B', '.', '.', '.'],
                ['C', '.', 'B', 'H', 'H', 'H'],
                ['A', 'A', 'D', 'D', '.', '.'],
                ['.', '.', '.', '.', '.', '.'],
                ['E', 'E', 'G', 'G', 'G', 'F'],
                ['.', '.', '.', '.', '.', 'F'], ],
            "expected": 1
        },
        {
            "name": "A",
            "input": [
                ['.', '.', '.', 'G', 'F', '.'],
                ['.', '.', 'B', 'G', 'F', '.'],
                ['A', 'A', 'B', 'C', 'F', '.'],
                ['.', '.', '.', 'C', 'D', 'D'],
                ['.', '.', '.', 'C', '.', '.'],
                ['.', '.', 'E', 'E', '.', '.'], ],
            "expected": 3
        },
        {
            "name": "A",
            "input": [
                ['.', '.', 'B', 'G', 'F', '.'],
                ['.', '.', 'B', 'G', 'F', '.'],
                ['A', 'A', '.', '.', '.', '.'],
                ['.', '.', '.', 'C', 'D', 'D'],
                ['.', '.', '.', 'C', '.', '.'],
                ['.', '.', 'E', 'E', '.', '.'], ],
            "expected": 0
        }
    ]
    for case in testcases:
        actual = numberOfBlockingVehiclesHeuristic(case["input"])
        assert (case["expected"]) == actual


def test_my_h2():
    testcases = [
        {
            "name": "A",
            "input":  [
    ['B', '.', 'D', 'D', 'D', 'N'],
    ['B', '.', '.', 'X', 'X', 'N'],
    ['.', 'A', 'A', 'P', 'P', 'N'],
    ['G', '.', '.', 'L', 'L', '.'],
    ['G', 'U', 'U', 'U', '.', 'R'],
    ['.', 'D', 'D', 'D', '.', 'R'],],
            "expected": 3
        },
        {
            "name": "A",
            "input": [
                ['I', 'I', 'B', '.', '.', '.'],
                ['C', '.', 'B', 'H', 'H', 'H'],
                ['C', '.', 'A', 'A', 'D', '.'],
                ['.', '.', '.', '.', 'D', '.'],
                ['E', 'E', 'G', 'G', 'G', 'F'],
                ['.', '.', '.', '.', '.', 'F'], ],
            "expected": 1
        },
        {
            "name": "A",
            "input": [
                ['C', '.', 'B', '.', '.', '.'],
                ['C', '.', 'B', 'H', 'H', 'H'],
                ['A', 'A', 'D', 'D', '.', '.'],
                ['.', '.', '.', '.', '.', '.'],
                ['E', 'E', 'G', 'G', 'G', 'F'],
                ['.', '.', '.', '.', '.', 'F'], ],
            "expected": 2
        },
        {
            "name": "A",
            "input": [
                ['.', '.', '.', 'G', 'F', '.'],
                ['.', '.', 'B', 'G', 'F', '.'],
                ['A', 'A', 'B', 'C', 'F', '.'],
                ['.', '.', '.', 'C', 'D', 'D'],
                ['.', '.', '.', 'C', '.', '.'],
                ['.', '.', 'E', 'E', '.', '.'], ],
            "expected": 3
        },
        {
            "name": "A",
            "input": [
                ['.', '.', 'B', 'G', 'F', '.'],
                ['.', '.', 'B', 'G', 'F', '.'],
                ['A', 'A', '.', '.', '.', '.'],
                ['.', '.', '.', 'C', 'D', 'D'],
                ['.', '.', '.', 'C', '.', '.'],
                ['.', '.', 'E', 'E', '.', '.'], ],
            "expected": 0
        }
    ]
    for case in testcases:
        actual = numberOfBlockingPositions(case["input"])
        assert (case["expected"]) == actual



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



def test_my_h4():
    testcases = [
    #     {
    #         "name": "A",
    #         "input":  [
    # ['B', '.', 'D', 'D', 'D', 'N'],
    # ['B', '.', '.', 'X', 'X', 'N'],
    # ['.', 'A', 'A', 'P', 'P', 'N'],
    # ['G', '.', '.', 'L', 'L', '.'],
    # ['G', 'U', 'U', 'U', '.', 'R'],
    # ['.', 'D', 'D', 'D', '.', 'R'],],
    #         "expected": 2
    #     },
        {
            "name": "new",
            "input": [
                ['B', 'B', 'I', 'C', 'C', 'C'],
                ['E', 'E', 'I', '.', 'G', 'L'],
                ['D', 'A', 'A', 'J', 'G', 'L'],
                ['D', '.', '.', 'J', 'F', 'F'],
                ['M', 'M', 'M', '.', '.', 'N'],
                ['.', '.', '.', '.', '.', 'N'], ],
            "expected": 5
        },
        # {
        #     "name": "b",
        #     "input": [
        #         ['I', 'I', 'B', 'Z', 'Z', '.'],
        #         ['C', '.', 'B', 'H', 'H', '.'],
        #         ['C', '.', 'A', 'A', 'D', '.'],
        #         ['.', '.', '.', '.', 'D', '.'],
        #         ['E', 'E', 'G', 'G', 'G', 'F'],
        #         ['.', '.', '.', 'P', 'P', 'F'], ],
        #     "expected": 3
        # },
        # {
        #     "name": "c",
        #     "input": [
        #         ['C', '.', 'B', '.', '.', '.'],
        #         ['C', '.', 'B', 'H', 'H', 'H'],
        #         ['A', 'A', 'D', 'D', '.', '.'],
        #         ['.', '.', '.', '.', '.', '.'],
        #         ['E', 'E', 'G', 'G', 'G', 'F'],
        #         ['.', '.', '.', '.', '.', 'F'], ],
        #     "expected": 1
        # },
        # {
        #     "name": "A",
        #     "input": [
        #         ['.', '.', '.', 'G', 'F', '.'],
        #         ['.', '.', 'B', 'G', 'F', '.'],
        #         ['A', 'A', 'B', 'C', 'F', '.'],
        #         ['.', '.', '.', 'C', 'D', 'D'],
        #         ['.', '.', '.', 'C', '.', '.'],
        #         ['.', '.', 'E', 'E', '.', '.'], ],
        #     "expected": 4
        # },
        # {
        #     "name": "A",
        #     "input": [
        #         ['.', '.', 'B', 'G', 'F', '.'],
        #         ['.', '.', 'B', 'G', 'F', '.'],
        #         ['A', 'A', '.', '.', '.', '.'],
        #         ['.', '.', '.', 'C', 'D', 'D'],
        #         ['.', '.', '.', 'C', '.', '.'],
        #         ['.', '.', 'E', 'E', '.', '.'], ],
        #     "expected": 0
        # }
    ]
    for case in testcases:
        actual = minClearable(case["input"])
        assert (case["expected"]) == actual
