from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here

        disk_to_number = {"disk1": 1, "disk2": 2, "disk3": 3, "disk4": 4, "disk5": 5}
        disk_map = lambda disk: int(disk_to_number[disk.bindings_dict["?X"]])

        peg_1 = parse_input("fact: (above ?X peg1)")
        peg_1_disks = self.kb.kb_ask(peg_1)
        peg_1_disks = tuple(sorted(map(disk_map, peg_1_disks))) if peg_1_disks else ()
        
        peg_2 = parse_input("fact: (above ?X peg2)")
        peg_2_disks = self.kb.kb_ask(peg_2)
        peg_2_disks = tuple(sorted(map(disk_map, peg_2_disks))) if peg_2_disks else ()

        peg_3 = parse_input("fact: (above ?X peg3)")
        peg_3_disks = self.kb.kb_ask(peg_3)
        peg_3_disks = tuple(sorted(map(disk_map, peg_3_disks))) if peg_3_disks else ()

        return (peg_1_disks, peg_2_disks, peg_3_disks)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here

        pegs = ["peg1", "peg2", "peg3"]

        disk_to_move = str(movable_statement.terms[0].term)
        source_peg = str(movable_statement.terms[1].term)
        dest_peg = str(movable_statement.terms[2].term)

        structure_input = lambda to_join: parse_input(''.join(to_join))

        dest_top = self.kb.kb_ask(structure_input(["fact: (top ?X ", dest_peg, ")"]))
        if dest_top: 
            dest_top = dest_top[0].bindings_dict["?X"]
            self.kb.kb_retract(structure_input(["fact: (top ", dest_top, " ", dest_peg, ")"]))
            self.kb.kb_assert(structure_input(["fact: (on ", disk_to_move, " ", dest_top, ")"]))
        else:
            self.kb.kb_retract(structure_input(["fact: (empty ", dest_peg,")"]))
            self.kb.kb_assert(structure_input(["fact: (on ", disk_to_move, " ", dest_peg, ")"]))

        self.kb.kb_assert(structure_input(["fact: (top ", disk_to_move, " ", dest_peg, ")"]))

        under_disk_to_move = self.kb.kb_ask(structure_input(["fact: (on ", disk_to_move, " ?X)"]))[0].bindings_dict["?X"]
        self.kb.kb_retract(structure_input(["fact: (on ", disk_to_move, " ", under_disk_to_move, ")"]))
        self.kb.kb_retract(structure_input(["fact: (top ", disk_to_move, " ", source_peg, ")"]))

        if under_disk_to_move in pegs: self.kb.kb_assert(structure_input(["fact: (empty ", under_disk_to_move, ")"]))
        else: self.kb.kb_assert(structure_input(["fact: (top ", under_disk_to_move, " ", source_peg, ")"]))

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        tile_names = {"tile1": 1, "tile2": 2, "tile3": 3, "tile4": 4, "tile5": 5, 
                        "tile6": 6, "tile7": 7, "tile8": 8, "empty": -1}
        positions = ["pos1", "pos2", "pos3"]
        tile_positions = {}

        structure_input = lambda to_join: parse_input(''.join(to_join))
        tile_map = lambda tile: int(tile_names[tile.bindings_dict["?X"]])

        board = []

        for y_pos in positions:
            row = []
            for x_pos in positions:

                x_tiles = self.kb.kb_ask(structure_input(["fact: (x ?X ", x_pos ,")"]))
                y_tiles = self.kb.kb_ask(structure_input(["fact: (y ?X ", y_pos, ")"]))
                x_tiles = list(map(tile_map, x_tiles))
                y_tiles = list(map(tile_map, y_tiles))

                tile = list(set(x_tiles) & set(y_tiles))[0]
                row.append(tile)
            board.append(tuple(row))

        return tuple(board)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here

        tile_to_move = str(movable_statement.terms[0].term)
        start_x = str(movable_statement.terms[1].term)
        start_y = str(movable_statement.terms[2].term)
        end_x = str(movable_statement.terms[3].term)
        end_y = str(movable_statement.terms[4].term)

        structure_input = lambda to_join: parse_input(''.join(to_join))
        
        self.kb.kb_retract(structure_input(["fact: (x ", tile_to_move, " ", start_x, ")"]))
        self.kb.kb_retract(structure_input(["fact: (y ", tile_to_move, " ", start_y, ")"]))
        self.kb.kb_retract(structure_input(["fact: (x empty ", end_x, ")"]))
        self.kb.kb_retract(structure_input(["fact: (y empty ", end_y, ")"]))

        self.kb.kb_assert(structure_input(["fact: (x ", tile_to_move, " ", end_x, ")"]))
        self.kb.kb_assert(structure_input(["fact: (y ", tile_to_move, " ", end_y, ")"]))
        self.kb.kb_assert(structure_input(["fact: (x empty ", start_x, ")"]))
        self.kb.kb_assert(structure_input(["fact: (y empty ", start_y, ")"]))

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))