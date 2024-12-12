import socket
import threading
import time
import random
import json
import os


class Node:
    def __init__(self, node_id, peers, port):
        self.node_id = node_id
        self.peers = peers  # List of peer addresses
        self.state = "Follower"
        self.term = 0
        self.voted_for = None
        self.election_timeout = random.uniform(1.0, 3.0)
        self.last_heartbeat = time.time()
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", self.port))  # Bind to all interfaces

    def start_election(self):
        self.state = "Candidate"
        self.term += 1
        self.voted_for = self.node_id
        votes = 1  # Vote for self
        print(f"Node {self.node_id} starting election for term {self.term}")
        for peer in self.peers:
            message = {
                "type": "RequestVote",
                "term": self.term,
                "candidate_id": self.node_id,
            }
            self.sock.sendto(json.dumps(message).encode(), peer)

    def send_heartbeat(self):
        while self.state == "Leader":
            for peer in self.peers:
                message = {
                    "type": "Heartbeat",
                    "term": self.term,
                    "leader_id": self.node_id,
                }
                self.sock.sendto(json.dumps(message).encode(), peer)
            time.sleep(1)

    def handle_messages(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            message = json.loads(data.decode())
            print(f"Node {self.node_id} received: {message}")
            if message["type"] == "RequestVote":
                # Handle vote request
                if (self.voted_for is None or self.voted_for == message["candidate_id"]) and message["term"] >= self.term:
                    self.voted_for = message["candidate_id"]
                    self.term = message["term"]
                    response = {
                        "type": "VoteResponse",
                        "term": self.term,
                        "vote_granted": True,
                    }
                    self.sock.sendto(json.dumps(response).encode(), addr)


if __name__ == "__main__":
    node_id = int(os.getenv("NODE_ID"))
    peers = [(os.getenv(f"PEER_{i}_HOST"), int(
        os.getenv(f"PEER_{i}_PORT"))) for i in range(int(os.getenv("NUM_PEERS")))]
    port = int(os.getenv("NODE_PORT"))

    node = Node(node_id, peers, port)
    threading.Thread(target=node.handle_messages).start()
    time.sleep(random.uniform(0.5, 1.5))  # Stagger elections
    node.start_election()
