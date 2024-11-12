# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import engine, get_db, SessionLocal
from contextlib import asynccontextmanager
from typing import List
from .test_data_loader import TestDataLoader

# Crear todas las tablas
models.Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando APP")
    print("Carga datos de prueba al iniciar la aplicación.")
    db = SessionLocal()
    data_loader = TestDataLoader(db)
    data_loader.clear_data()  # Opcional: limpia datos de prueba anteriores
    data_loader.load_data()
    db.close()
    yield 
    print("Cerrando APP")
    db.close()

app = FastAPI(lifespan=lifespan)


# Endpoints para Tracking_Product
@app.post("/products/", response_model=schemas.TrackingProduct)
def create_product(product: schemas.TrackingProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db=db, name=product.name, description=product.description, is_available=product.is_available)

@app.get("/products/{product_id}", response_model=schemas.TrackingProduct)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db=db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.get("/products/", response_model=list[schemas.TrackingProduct])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud.get_all_products(db=db, skip=skip, limit=limit)
    return products

# Endpoints para Tracking_Station
@app.post("/stations/", response_model=schemas.TrackingStation)
def create_station(station: schemas.TrackingStationCreate, db: Session = Depends(get_db)):
    return crud.create_station(db=db, name=station.name)

@app.get("/stations/{station_id}", response_model=schemas.TrackingStation)
def read_station(station_id: int, db: Session = Depends(get_db)):
    db_station = crud.get_station(db=db, station_id=station_id)
    if db_station is None:
        raise HTTPException(status_code=404, detail="Station not found")
    return db_station

@app.get("/stations/", response_model=list[schemas.TrackingStation])
def read_stations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    stations = crud.get_all_stations(db=db, skip=skip, limit=limit)
    return stations

# Endpoints para Tracking_Zone
@app.post("/zones/", response_model=schemas.TrackingZone)
def create_zone(zone: schemas.TrackingZoneCreate, db: Session = Depends(get_db)):
    return crud.create_zone(db=db, name=zone.name, canvas_x=zone.canvas_x, canvas_y=zone.canvas_y, 
                            station_id=zone.station_id, canvas_width=zone.canvas_width, canvas_height=zone.canvas_height, 
                            next_zone=zone.next_zone, preview_zone=zone.preview_zone)

@app.get("/zones/{zone_id}", response_model=schemas.TrackingZone)
def read_zone(zone_id: int, db: Session = Depends(get_db)):
    db_zone = crud.get_zone(db=db, zone_id=zone_id)
    if db_zone is None:
        raise HTTPException(status_code=404, detail="Zone not found")
    return db_zone

@app.get("/zones/", response_model=list[schemas.TrackingZone])
def read_zones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    zones = crud.get_all_zones(db=db, skip=skip, limit=limit)
    return zones

# ---------------------------
# Endpoints para Tracking (Movimientos de productos)
# ---------------------------

@app.post("/trackings/", response_model=schemas.Tracking)
def create_tracking(tracking: schemas.TrackingCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo registro de seguimiento de un producto en una zona.
    """
    return crud.create_tracking(db=db, product_id=tracking.product_id, zone_id=tracking.zone_id)

@app.get("/trackings/{tracking_id}", response_model=schemas.Tracking)
def read_tracking(tracking_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un registro de seguimiento específico por ID.
    """
    db_tracking = crud.get_tracking(db=db, tracking_id=tracking_id)
    if db_tracking is None:
        raise HTTPException(status_code=404, detail="Tracking record not found")
    return db_tracking

@app.get("/trackings/", response_model=list[schemas.Tracking])
def read_trackings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtiene todos los registros de seguimiento con opciones de paginación.
    """
    trackings = crud.get_all_tracking(db=db, skip=skip, limit=limit)
    return trackings

@app.get("/trackings/product/{product_id}", response_model=list[schemas.Tracking])
def get_product_tracking_history(product_id: int, db: Session = Depends(get_db)):
    """
    Obtiene el historial de movimientos de un producto específico por su ID.
    """
    trackings = db.query(models.Tracking).filter(models.Tracking.product_id == product_id).all()
    if not trackings:
        raise HTTPException(status_code=404, detail="No tracking records found for the specified product")
    return trackings

@app.get("/trackings/zone/{zone_id}", response_model=list[schemas.Tracking])
def get_zone_tracking_history(zone_id: int, db: Session = Depends(get_db)):
    """
    Obtiene el historial de productos que pasaron por una zona específica.
    """
    trackings = db.query(models.Tracking).filter(models.Tracking.zone_id == zone_id).all()
    if not trackings:
        raise HTTPException(status_code=404, detail="No tracking records found for the specified zone")
    return trackings
