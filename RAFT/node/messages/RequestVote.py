import json


class RequestVote:
    def __init__(self, term, candidate_id):
        self.term = term
        self.candidate_id = candidate_id

    def __str__(self):
        return f"RequestVote({self.term}, {self.candidate_id})"

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def from_json(json_str):
        json_dict = json.loads(json_str)
        return RequestVote(json_dict["term"], json_dict["candidate_id"])

    def to_json(self):
        return json.dumps({"message_type": "RequestVote", "term": self.term, "candidate_id": self.candidate_id})

    def get_term(self):
        return self.term

    def get_candidate_id(self):
        return self.candidate_id

    def set_term(self, term):
        self.term = term

    def set_candidate_id(self, candidate_id):
        self.candidate_id = candidate_id

    def __eq__(self, other):
        return self.term == other.term and self.candidate_id == other.candidate_id

    def __ne__(self, other):
        return not self.__eq__(other)
