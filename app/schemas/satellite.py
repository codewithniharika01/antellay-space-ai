from pydantic import BaseModel, ConfigDict


class SatelliteBase(BaseModel):
    name: str
    norad_id: int
    country: str
    mission: str
    status: str


class SatelliteCreate(SatelliteBase):
    pass


class SatelliteUpdate(SatelliteBase):
    pass


class SatelliteResponse(SatelliteBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
    