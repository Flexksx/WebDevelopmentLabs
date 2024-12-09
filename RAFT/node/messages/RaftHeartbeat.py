import json


class RaftHeartbeat:
    def __init__(self, term, leader_id):
        self.term = term
        self.leader_id = leader_id

    def __str__(self):
        return f"RaftHeartbeat({self.term}, {self.leader_id})"

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def from_json(json_str):
        json_dict = json.loads(json_str)
        return RaftHeartbeat(json_dict["term"], json_dict["leader_id"])

    def to_json(self):
        return json.dumps({"term": self.term, "leader_id": self.leader_id})

    def get_term(self):
        return self.term

    def get_leader_id(self):
        return self.leader_id

    def set_term(self, term):
        self.term = term

    def set_leader_id(self, leader_id):
        self.leader_id = leader_id

    def __eq__(self, other):
        return self.term == other.term and self.leader_id == other.leader_id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.term, self.leader_id))
