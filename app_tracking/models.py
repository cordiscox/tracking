# app/models.py
import datetime
from .database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey
from datetime import datetime

#THIS CLASS NEED TO CHANGE TO A PRODUCT SCHEMA - TO APP_PRODUCTION.
class Tracking_Product(Base):
    __tablename__ = 'tracking.product'
    
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)

    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, onupdate=datetime.now())
    
class Tracking_Station(Base):
    __tablename__ = 'tracking.station'

    station_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)

    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, onupdate=datetime.utcnow)


class Tracking_Zone(Base):
    __tablename__ = 'tracking.zone'

    zone_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)
    #### To draw the zone
    canvas_x = Column(Integer)
    canvas_y = Column(Integer)
    canvas_width = Column(Integer, default=100)
    canvas_height = Column(Integer, default=50)
    #########################
    next_zone = Column(Integer, nullable=True)
    preview_zone = Column(Integer, nullable=True)
    #########################
    ### One Zone can be in the same station
    station_id = Column(Integer, ForeignKey('tracking.station.station_id'), index=True, nullable=False)
    
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, onupdate=datetime.now())

#Aca van todas las piezas que se crean - estan se tienen que ir generando nuevos registros mientras se vayan moviendo por zonas. 
class Tracking(Base):
    __tablename__ = 'tracking.tracking'

    tracking_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('tracking.product.product_id'), index=True, nullable=False)
    zone_id = Column(Integer, ForeignKey('tracking.zone.zone_id'), index=True, nullable=False)
       
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, onupdate=datetime.now())
