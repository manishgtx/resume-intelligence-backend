from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field

class MatchStatus(str, Enum):
    STRONG = "strong"
    PARTIAL = "partial"
    MISSING = "missing"
    OVERQUALIFIED = "overqualified"
    IRRELEVANT = "irrelevant"
    