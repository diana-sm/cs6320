from dataclasses import dataclass

@dataclass
class Parameter:
    name: str
    min_val: int
    max_val: int
    default_val: int
    current_val = default_val