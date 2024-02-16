import faust

class AverageCalculation(faust.Record, serializer='json'):
    total: int = 0
    count: int = 0
    average: float = 0