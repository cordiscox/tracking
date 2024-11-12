# app/crud.py
from sqlalchemy.orm import Session
from .schemas import TrackingProduct, TrackingStation, TrackingZone, Tracking
from datetime import datetime


# CRUD for TrackingProduct
def create_product(db: Session, name: str, description: str = None, is_available: bool = True):
    db_product = TrackingProduct(name=name, description=description, is_available=is_available)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product(db: Session, product_id: int):
    return db.query(TrackingProduct).filter(TrackingProduct.product_id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(TrackingProduct).offset(skip).limit(limit).all()


# CRUD for TrackingStation
def create_station(db: Session, name: str):
    db_station = TrackingStation(name=name)
    db.add(db_station)
    db.commit()
    db.refresh(db_station)
    return db_station

def get_station(db: Session, station_id: int):
    return db.query(TrackingStation).filter(TrackingStation.station_id == station_id).first()

def get_stations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(TrackingStation).offset(skip).limit(limit).all()


# CRUD for TrackingZone
def create_zone(db: Session, name: str, station_id: int, canvas_x: int, canvas_y: int, next_zone: int = None, preview_zone: int = None):
    db_zone = TrackingZone(
        name=name,
        station_id=station_id,
        canvas_x=canvas_x,
        canvas_y=canvas_y,
        next_zone=next_zone,
        preview_zone=preview_zone
    )
    db.add(db_zone)
    db.commit()
    db.refresh(db_zone)
    return db_zone

def get_zone(db: Session, zone_id: int):
    return db.query(TrackingZone).filter(TrackingZone.zone_id == zone_id).first()

def get_zones(db: Session, skip: int = 0, limit: int = 100):
    return db.query(TrackingZone).offset(skip).limit(limit).all()

# CRUD for Tracking (Tracking movements)
def create_tracking(db: Session, product_id: int, zone_id: int):
    db_tracking = Tracking(product_id=product_id, zone_id=zone_id)
    db.add(db_tracking)
    db.commit()
    db.refresh(db_tracking)
    return db_tracking

def get_tracking(db: Session, tracking_id: int):
    return db.query(Tracking).filter(Tracking.tracking_id == tracking_id).first()

def get_trackings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Tracking).offset(skip).limit(limit).all()