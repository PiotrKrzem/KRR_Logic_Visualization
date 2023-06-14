from dataclasses import dataclass, field
from typing import List


INITIALLY = 'initially'
CAUSES = 'causes'
AFTER = 'after'

@dataclass
class State:
    fluents: List[str] = field(default_factory=list)
    cost: int = 0

    def __eq__(self, other) -> bool:
        if len(self.fluents) != len(other.fluents): 
            return False
        for i in range(len(self.fluents)):
            if self.fluents[i] != other.fluents[i]: 
                return False
        return True

@dataclass
class Statement:
    type: str = ''
    markdown: str = ''

@dataclass
class InitiallyStatement(Statement):
    type: str = INITIALLY
    fluent: str = ''

@dataclass
class CausesStatement(Statement):
    type: str = CAUSES
    action: str = ''
    fluents: List[str] = field(default_factory=list)
    if_fluents: List[str] = field(default_factory=list)
    cost: int  = 0

@dataclass
class AfterStatement(Statement):
    type: str = AFTER
    fluent: str = ''
    actions: List[str] = field(default_factory=list)


if __name__ == '__main__':
    a = State(['~ hi', '~ there', '~ hello'])
    b = State(['~ hi', '~ there', '~ hello'])
    c = a == b
    print(c)
