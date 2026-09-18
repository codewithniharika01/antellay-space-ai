from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


from app.auth.auth import get_current_user
from app.models.user import User
from app.database.database import get_db
from app.models.satellite import Satellite
from app.schemas.satellite import (
    SatelliteCreate,
    SatelliteResponse,
    SatelliteUpdate,
)

router = APIRouter(
    prefix="/satellites",
    tags=["Satellites"]
)


@router.post(
    "",
    response_model=SatelliteResponse,
    status_code=201
)
def create_satellite(
    satellite: SatelliteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing = (
        db.query(Satellite)
        .filter(Satellite.norad_id == satellite.norad_id)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Satellite with this NORAD ID already exists"
        )

    new_satellite = Satellite(**satellite.model_dump())

    db.add(new_satellite)
    db.commit()
    db.refresh(new_satellite)

    return new_satellite


@router.get(
    "",
    response_model=list[SatelliteResponse]
)
def get_satellites(
    db: Session = Depends(get_db)
):
    return db.query(Satellite).all()


@router.get(
    "/{satellite_id}",
    response_model=SatelliteResponse
)
def get_satellite(
    satellite_id: int,
    db: Session = Depends(get_db)
):
    satellite = (
        db.query(Satellite)
        .filter(Satellite.id == satellite_id)
        .first()
    )

    if not satellite:
        raise HTTPException(
            status_code=404,
            detail="Satellite not found"
        )

    return satellite


@router.put(
    "/{satellite_id}",
    response_model=SatelliteResponse
)
def update_satellite(
    satellite_id: int,
    satellite_data: SatelliteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    satellite = (
        db.query(Satellite)
        .filter(Satellite.id == satellite_id)
        .first()
    )

    if not satellite:
        raise HTTPException(
            status_code=404,
            detail="Satellite not found"
        )

    for key, value in satellite_data.model_dump().items():
        setattr(satellite, key, value)

    db.commit()
    db.refresh(satellite)

    return satellite


@router.delete("/{satellite_id}")
def delete_satellite(
    satellite_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    satellite = (
        db.query(Satellite)
        .filter(Satellite.id == satellite_id)
        .first()
    )

    if not satellite:
        raise HTTPException(
            status_code=404,
            detail="Satellite not found"
        )

    db.delete(satellite)
    db.commit()

    return {
        "message": "Satellite deleted successfully"
    }
