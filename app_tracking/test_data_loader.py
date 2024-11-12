# app/test_data_loader.py
from sqlalchemy.orm import Session
from . import models

class TestDataLoader:
    def __init__(self, db: Session):
        self.db = db

    def load_data(self):
        # Agregar productos de ejemplo
        products = [
            models.Tracking_Product(name="Producto 1", description="Descripción del producto 1"),
            models.Tracking_Product(name="Producto 2", description="Descripción del producto 2"),
            models.Tracking_Product(name="Producto 3", description="Descripción del producto 3"),
        ]
        self.db.add_all(products)
        self.db.commit()  # Confirmar productos antes de proceder

        # Agregar estaciones de ejemplo
        stations = [
            models.Tracking_Station(name="Estación 1"),
            models.Tracking_Station(name="Estación 2"),
        ]
        self.db.add_all(stations)
        self.db.commit()  # Confirmar estaciones antes de proceder

        # Agregar zonas de ejemplo
        zones = [
            models.Tracking_Zone(name="Zona A", canvas_x=10, canvas_y=10, station_id=1),
            models.Tracking_Zone(name="Zona B", canvas_x=20, canvas_y=20, station_id=1),
            models.Tracking_Zone(name="Zona C", canvas_x=30, canvas_y=30, station_id=2),
        ]
        self.db.add_all(zones)
        self.db.commit()  # Confirmar zonas antes de proceder

        # Agregar registros de seguimiento de ejemplo
        trackings = [
            models.Tracking(product_id=1, zone_id=1),
            models.Tracking(product_id=1, zone_id=2),
            models.Tracking(product_id=2, zone_id=1),
            models.Tracking(product_id=3, zone_id=3),
        ]
        self.db.add_all(trackings)
        self.db.commit()  # Confirmar trackings al final

        print("Datos de prueba cargados exitosamente.")

    def clear_data(self):
        """
        Elimina todos los registros de prueba de las tablas para facilitar las pruebas repetidas.
        """
        self.db.query(models.Tracking).delete()
        self.db.query(models.Tracking_Zone).delete()
        self.db.query(models.Tracking_Station).delete()
        self.db.query(models.Tracking_Product).delete()
        self.db.commit()

        print("Datos de prueba eliminados exitosamente.")
