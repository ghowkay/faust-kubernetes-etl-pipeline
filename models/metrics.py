import faust
from datetime import datetime

class Metrics(faust.Record, validation=True):
    created_at: datetime
    value: int
    node_id: str
    capacity: int