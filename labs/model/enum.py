from enum import StrEnum


class RelationDegree(StrEnum):
    LINEAR = "linear"
    QUADRATIC = "quadratic"


relation_degrees = [
    RelationDegree.LINEAR,
    RelationDegree.QUADRATIC,
]
