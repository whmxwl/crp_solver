# src/environment.py
import copy

class SequenceCRPEnv:
    def __init__(self, bays, max_height, initial_state, target_sequence):
        self.bays = bays
        self.max_height = max_height
        self.state = copy.deepcopy(initial_state)
        self.sequence = target_sequence
        self.seq_index = 0

    def get_current_target(self):
        return self.sequence[self.seq_index] if self.seq_index < len(self.sequence) else None

    def retrieve_container(self, bay_index):
        target = self.get_current_target()
        if target is not None and len(self.state[bay_index]) > 0:
            if self.state[bay_index][-1] == target:
                self.state[bay_index].pop()
                self.seq_index += 1
                return True
        return False

    def move_container(self, from_bay, to_bay):
        if len(self.state[from_bay]) == 0 or len(self.state[to_bay]) >= self.max_height:
            return False 
        self.state[to_bay].append(self.state[from_bay].pop())
        return True