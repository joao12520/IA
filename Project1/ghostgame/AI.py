import math
import copy
import random
from ghostgame.constants import MINIMAX_DEPTH, MCTS_EXPL_FACTOR, MCTS_DEPTH

class AI:
    def __init__(self):
        self.escapedWeight = 1000
        self.distToExitWeight = 10

    def eval(self, state):
        val = 0
        player = state.getTurn()

        for escaped in state.getEscaped(player):
            if escaped <= 1:
                val += escaped * self.escapedWeight
            else:   #Having more than one ghost escape is bad, since it has no value and decreases the number of available pieces to play
                val -= 10*self.escapedWeight

        val += state.sumOfDistsToExit()

        return val

    def get_children(self, state):
        children = []

        for mov in state.possibleMoves():
            newState = copy.deepcopy(state)
            newState.move(mov[0], mov[1])
            children.append(newState)

        return children

    def get_children_first_round(self, state):
        children = []

        for mov1 in state.possibleMoves():
            tempState = copy.deepcopy(state)
            tempState.move(mov1[0], mov1[1])
            for mov2 in tempState.possibleMoves():
                newState = copy.deepcopy(state)
                newState.move(mov2[0], mov2[1])
                children.append(newState)

        return children

class Minimax:
    def __init__(self):
        self.ai = AI()
    def minimax(self, state, depth, playerMax, alpha, beta):
        if depth == 0 or state.isOver():
            return self.ai.eval(state), state

        possibleMoves = self.ai.get_children(state)

        if playerMax:
            best_score = -math.inf
            possibleMoves.sort(key=self.ai.eval, reverse=True)

            for child_state in possibleMoves:
                score, _ = self.minimax(child_state, depth - 1, False, alpha, beta)
                if score > best_score:
                    best_score = score
                    best_child = child_state
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best_score, best_child

        else:
            best_score = math.inf
            possibleMoves.sort(key=self.ai.eval)

            for child_state in possibleMoves:
                score, _ = self.minimax(child_state, depth - 1, True, alpha, beta)
                if score < best_score:
                    best_score = score
                    best_child = child_state
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            return best_score, best_child

class MCTS_Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.visits = 0
        self.score = 0
        self.children = []
        self.parent = parent

    def add_child(self, child_state):
        child = MCTS_Node(child_state, parent=self)
        self.children.append(child)

    def update(self, result):
        self.visits += 1
        self.score += result

    def is_fully_expanded(self):
        return len(self.children) == len(self.state.possibleMoves())

    def select_child(self, expl_factor):
        scores = [c.score / (c.visits + 1) for c in self.children]
        max_score = max(map(abs, scores))
        max_score = max_score if max_score != 0 else 1
        scores = [s / max_score for s in scores]

        scores = [s + expl_factor * math.sqrt(2 * math.log(self.visits) / (c.visits + 1)) for s, c in
                  zip(scores, self.children)]
        return self.children[scores.index(max(scores))]

def simulate(state, depth):
    ai = AI()
    for i in range(depth):
        if state.isOver():
            break
        move = random.choice(state.possibleMoves())
        state.move(move[0], move[1])
    return ai.eval(state)

def mcts(root, iterations):
    for i in range(iterations):
        node = root
        state = copy.deepcopy(root.state)

        # selection
        while node.is_fully_expanded() and not state.isOver():
            node = node.select_child(MCTS_EXPL_FACTOR)
            move = node.state.lastMove
            state.move(move[0], move[1])

        # expansion
        if not state.isOver():
            move = random.choice([
                    move for move in state.possibleMoves() if move not in [child.state.lastMove for child in node.children]
                ])

            state.move(move[0], move[1])
            node.add_child(state)
            state = copy.deepcopy(node.children[-1].state)

        # simulation
        result = simulate(state, MCTS_DEPTH)
        if state.turn != root.state.turn:
            result = -result

        # backpropagation
        while node is not None:
            node.update(result)
            node = node.parent

    # return the best move
    newBoard = max(root.children, key=lambda c: c.score / c.visits).state
    return newBoard