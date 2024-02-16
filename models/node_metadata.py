import faust

class NodeMetadata(faust.Record, validation=True):
    id: str             # Node ID
    instance_type: str  # Instance type of the node
    zone: str  # Availability zone of the node