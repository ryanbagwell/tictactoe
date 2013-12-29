
WINNING_SEQUENCES = [
    (0, 4, 8),
    (2, 4, 6),
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
]

class Sequence(list):

    def __init__(self, lst, board):
        super(Sequence, self).__init__(lst)

        squares = [v for k, v in board.iteritems() if k in self]
        self.ohs = len(filter(lambda o: o == 'o', squares))
        self.exes = len(filter(lambda x: x == 'x', squares))
        self.empties = len(filter(lambda y: y == '', squares))
        self.diagonal = (self == [0,4,8] or self == [2,4,6])



class Board(dict):

    def __init__(self, data):
        super(Board, self).__init__(data)


    def get_available_sequences(self):

        available_sequences = []

        for seq in WINNING_SEQUENCES:

            for i in seq:

                if self[i] is '':
                    available_sequences.append(seq)
                    continue

        return available_sequences


    def get_best_sequence(self):

        two_exes = []
        one_ex = []
        #zero_



        for seq in self.get_available_sequences():

            squares = [v for k, v in self.board.iteritems() if k in seq]

            """ check for the number of 'o' values """
            ohs = filter(lambda o: o == 'o', squares)

            """ if there are already two 'o' values, we need to
                make a move in this sequence """

            if len(ohs) is 2: return seq

            """ check for the number of 'x' values """
            exes = filter(lambda x: x == 'x', squares)


            """ check for the number of empty values """
            empties = filter(lambda y: y == '', squares)
















