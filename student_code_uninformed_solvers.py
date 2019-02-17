
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        if self.gm.isWon(): return True

        moves = self.gm.getMovables()

        if not moves:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            return False

        for move in moves:
            self.gm.makeMove(move)
            self.child_state = GameState(self.gm.getGameState(), self.currentState.depth + 1, move)
            self.child_state.parent = self.currentState
            self.currentState = self.child_state
            
            if self.currentState in self.visited and self.visited[self.currentState]: 
                self.gm.reverseMove(move)
                self.currentState = self.currentState.parent
                continue

            self.visited[self.currentState] = True
            break

class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here

        if self.currentState.depth == 0 and len(self.currentState.children) == 0: 
            initial_moves = self.gm.getMovables()
            for move in initial_moves: 
                self.gm.makeMove(move)
                new_child = GameState(self.gm.getGameState(), self.currentState.depth + 1, move)
                new_child.parent = self.currentState
                self.currentState.children.append(new_child)
                self.gm.reverseMove(move)
        else:
            while self.currentState.parent:
                self.gm.reverseMove(self.currentState.requiredMovable)
                self.currentState = self.currentState.parent

        new_state_found = False
        while not new_state_found:
            if len(self.currentState.children) - 1 >= self.currentState.nextChildToVisit:

                to_check_state = self.currentState.children[self.currentState.nextChildToVisit]
                child_state = self.currentState.children[self.currentState.nextChildToVisit]
                self.currentState.nextChildToVisit += 1

                if to_check_state in self.visited and self.visited[to_check_state]: 
                    continue

                parent = child_state.parent
                moves_to_child_state = []

                while parent:
                    moves_to_child_state.insert(0, child_state.requiredMovable)
                    child_state = child_state.parent
                    parent = child_state.parent

                for move in moves_to_child_state:
                    self.gm.makeMove(move)

                self.visited[to_check_state] = True

                if self.gm.isWon(): return True

                moves = self.gm.getMovables()
                for move in moves: 
                    self.gm.makeMove(move)
                    new_child = GameState(self.gm.getGameState(), to_check_state.depth + 1, move)
                    new_child.parent = to_check_state
                    self.currentState.children.append(new_child)
                    self.gm.reverseMove(move)
                new_state_found = True
                self.currentState = to_check_state
                return False

            else: return False