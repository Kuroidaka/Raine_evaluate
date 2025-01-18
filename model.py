from pydantic import BaseModel
from typing import Dict

class MemoryEvaluationClusters(BaseModel):
    Personal_Information: bool
    Habits_and_Preferences: bool
    Significant_Events: bool
    Relationships_and_Connections: bool
    Plans_and_Goals: bool
    Appointments_and_Time_Specific_Information: bool
    Ownership_and_Possessions: bool
    Locations_and_Places: bool
    Contextual_and_Multi_Session_Memory: bool


class EvalResponse(BaseModel):
    Accuracy: int
    Relevance: int
    Coherence: int
    Fluency: int
    Comments: str

