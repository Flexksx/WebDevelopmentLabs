from node.electable.RaftElectablePeer import RaftElectablePeer
from node.electable.RaftElectable import RaftElectable
from node.electable.RaftElectableContext import RaftElectableContext
from node.electable.RaftElectableSocket import RaftElectableUDPSocket

IP_ADDRESS = "0.0.0.0"
PORT = 5000

node = RaftElectable(RaftElectableContext(id="node1", peers=[
    RaftElectablePeer(id="node2", address=IP_ADDRESS, port=PORT+1),
    RaftElectablePeer(id="node3", address=IP_ADDRESS, port=PORT+2)]),
    RaftElectableUDPSocket(address=IP_ADDRESS, port=PORT))

print(f"Node {node.context.get_id()} started.")
node.start()
