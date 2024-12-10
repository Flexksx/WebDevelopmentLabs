import json


class VoteResponse:
    def __init__(self, term: int = None, vote_granted: bool = None):
        self.term = term
        self.vote_granted = vote_granted

    def __str__(self):
        return f"VoteResponse({self.term}, {self.vote_granted})"

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def from_json(json_str):
        json_dict = json.loads(json_str)
        return VoteResponse(json_dict["term"], json_dict["vote_granted"])

    def to_json(self):
        return json.dumps({"message_type": "VoteResponse", "term": self.term, "vote_granted": self.vote_granted})

    def get_term(self):
        return self.term

    def get_vote_granted(self):
        return self.vote_granted

    def set_term(self, term):
        self.term = term

    def set_vote_granted(self, vote_granted):
        self.vote_granted = vote_granted

    def __eq__(self, other):
        return self.term == other.term and self.vote_granted == other.vote_granted

    def __ne__(self, other):
        return not self.__eq__(other)
