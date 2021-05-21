from dataclasses import dataclass

@dataclass
class Parameter:
    name: str
    suffix: str
    min_val: int
    max_val: int
    default_val: int
    current_val: int
    granularity: int