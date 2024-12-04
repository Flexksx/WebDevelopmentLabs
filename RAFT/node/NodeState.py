from enum import Enum

class NodeState(Enum):
    FOLLOWER = "FOLLOWER"
    CANDIDATE = "CANDIDATE"
    LEADER = "LEADER"
    UNKNOWN = "UNKNOWN"
    
    def __str__(self):
        return self.value
    
    @staticmethod
    def from_str(label:str):
        if label == "FOLLOWER":
            return NodeState.FOLLOWER
        elif label == "CANDIDATE":
            return NodeState.CANDIDATE
        elif label == "LEADER":
            return NodeState.LEADER
        else:
            return NodeState.UNKNOWN
        
    def is_known(self):
        return self != NodeState.UNKNOWN
    
    def is_follower(self):
        return self == NodeState.FOLLOWER
    
    def is_candidate(self):
        return self == NodeState.CANDIDATE
    
    def is_leader(self):
        return self == NodeState.LEADER
    
    def is_unknown(self):
        return self == NodeState.UNKNOWN