import os
import time
from raft.electable.RaftElectable import RaftElectable
from raft.electable.RaftElectablePeer import RaftElectablePeer
from raft.electable.RaftElectableContext import RaftElectableContext
from raft.electable.RaftElectableState import RaftElectableState

# Read environment variables for node configuration
IP_ADDRESS = "0.0.0.0"
PORT = int(os.getenv("RAFT_PORT", "5000"))
NODE_ID = os.getenv("RAFT_NODE_ID", "node1")

# Define the cluster nodes
# Each node listens on port 5000 internally, and can be addressed by name
# on the Docker network.
ALL_PEERS = [
    RaftElectablePeer(id="node1", address="node1", port=5000),
    RaftElectablePeer(id="node2", address="node2", port=5000),
    RaftElectablePeer(id="node3", address="node3", port=5000)
]

# Filter out the current node from its own peer list
PEERS = [p for p in ALL_PEERS if p.get_id() != NODE_ID]

# Initialize the node
node = RaftElectable(
    id=NODE_ID,
    peers=PEERS,
    address=IP_ADDRESS,
    port=PORT
)

print(f"Node {node.context.get_id()} started at {IP_ADDRESS}:{
      PORT} with peers: {[p.get_id() for p in PEERS]}")

# Transition to FOLLOWER state
node.state.transition_to(RaftElectableState.FOLLOWER)

# Keep the main thread alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Shutting down node.")
    node.state.cleanup_current_state()
    node.context.get_socket().close()
    print("Node shut down gracefully.")
