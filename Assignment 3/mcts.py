from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, Optional, Tuple

from gridworld import MDP, State, Action, sample_next_state_and_reward


@dataclass
class MCTSConfig:
    gamma: float = 0.95
    c_uct: float = 1.4
    rollouts: int = 200
    max_depth: int = 200


class Node:
    def __init__(self, state: State, parent: Optional[Tuple["Node", Action]] = None) -> None:
        self.state = state
        self.parent = parent
        self.children: Dict[Action, Node] = {}
        self.visits = 0
        self.value_sum = 0.0

    @property
    def q(self) -> float:
        return 0.0 if self.visits == 0 else self.value_sum / float(self.visits)


class MCTS:
    def __init__(self, mdp: MDP, cfg: MCTSConfig, rng=None, heuristic=None) -> None:
        self.mdp = mdp
        self.cfg = cfg
        self.rng = rng
        self.heuristic = heuristic
        if self.rng is None:
            import random

            self.rng = random.Random(0)

    def search(self, root_state: State) -> Action:
        root = Node(root_state)
        for _ in range(self.cfg.rollouts):
            node = root
            path = []
            depth = 0
            # Selection
            while node.children and not self.mdp.is_terminal(node.state) and depth < self.cfg.max_depth:
                total_visits = sum(child.visits for child in node.children.values())
                best_score = -float('inf')
                best_a = None
                best_child = None
                for a, child in node.children.items():
                    q = child.q
                    n = child.visits
                    N = total_visits
                    c = self.cfg.c_uct
                    uct = q + c * math.sqrt(math.log(N + 1) / (1 + n))
                    if uct > best_score:
                        best_score = uct
                        best_a = a
                        best_child = child
                path.append((node, best_a))
                node = best_child
                depth += 1
            # Expansion
            if not self.mdp.is_terminal(node.state):
                untried = [a for a in self.mdp.actions(node.state) if a not in node.children]
                if untried:
                    a = self.rng.choice(untried)
                    s_next, r = sample_next_state_and_reward(self.mdp, node.state, a, self.rng)
                    child = Node(s_next, parent=(node, a))
                    node.children[a] = child
                    path.append((node, a))
                    node = child
                    depth += 1
            # Rollout
            s = node.state
            total_reward = 0.0
            gamma = self.cfg.gamma
            rollout_depth = depth
            discount = 1.0
            while not self.mdp.is_terminal(s) and rollout_depth < self.cfg.max_depth:
                actions = list(self.mdp.actions(s))
                if not actions:
                    break
                a = self.rng.choice(actions)
                s_next, r = sample_next_state_and_reward(self.mdp, s, a, self.rng)
                total_reward += discount * r
                discount *= gamma
                s = s_next
                rollout_depth += 1
            # Backpropagation
            G = total_reward
            for n, _ in reversed(path):
                n.visits += 1
                n.value_sum += G
                G *= gamma
            node.visits += 1
            node.value_sum += G

        # choose action with most visits
        best_a = None
        best_v = -1
        for a, ch in root.children.items():
            if ch.visits > best_v:
                best_v = ch.visits
                best_a = a
        if best_a is None:
            actions = list(self.mdp.actions(root_state))
            if not actions:
                raise RuntimeError("MCTS on terminal state")
            best_a = actions[0]
        return best_a

