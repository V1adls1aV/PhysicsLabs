from enum import StrEnum


class RelationDegree(StrEnum):
    NONE = "none"
    LINEAR = "linear"
    QUADRATIC = "quadratic"


relation_degrees = [
    RelationDegree.NONE,
    RelationDegree.LINEAR,
    RelationDegree.QUADRATIC,
]
