from enum import Enum


class RaftElectableState(Enum):
    FOLLOWER = "FOLLOWER"
    CANDIDATE = "CANDIDATE"
    LEADER = "LEADER"
    UNKNOWN = "UNKNOWN"

    def __str__(self):
        return self.value

    @staticmethod
    def from_str(label: str):
        if label == "FOLLOWER":
            return RaftElectableState.FOLLOWER
        elif label == "CANDIDATE":
            return RaftElectableState.CANDIDATE
        elif label == "LEADER":
            return RaftElectableState.LEADER
        else:
            return RaftElectableState.UNKNOWN

    def is_known(self):
        return self != RaftElectableState.UNKNOWN

    def is_follower(self):
        return self == RaftElectableState.FOLLOWER

    def is_candidate(self):
        return self == RaftElectableState.CANDIDATE

    def is_leader(self):
        return self == RaftElectableState.LEADER

    def is_unknown(self):
        return self == RaftElectableState.UNKNOWN
