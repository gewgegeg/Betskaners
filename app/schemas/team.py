from pydantic import BaseModel

class TeamBase(BaseModel):
    name: str
    logo_url: str | None = None
    rating: float = 1000.0

class TeamCreate(TeamBase):
    pass

class Team(TeamBase):
    id: int
    total_matches: int
    wins: int
    losses: int

    class Config:
        from_attributes = True 