from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
import schemas, models

def get_cars(db: Session, sortby: str = "id", orderby: str = "asc"):
    sort_column = getattr(models.cars, sortby)
    if orderby == "asc":
        sort_column = asc(sort_column)
    else:
        sort_column = desc(sort_column)
    return db.query(models.cars).order_by(sort_column).all()

def get_car(id: int, db: Session):
    return (
        db
        .query(models.cars)
        .filter(models.cars.id == id)
        .first()
    )

def create_car(car: schemas.CarCreate, db: Session):
    db_car = models.cars(
        name=car.name,
        price=car.price
    )

    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car

def update_car(car: schemas.CarUpdate,id: int, db: Session):
    db_car = db.query(models.cars).filter(models.cars.id == id).first()
    if db_car:
        updated_info = car.model_dump(exclude_unset=True)
        for key,value in updated_info.items():
            setattr(db_car, key, value)
        db.commit()
        db.refresh(db_car)
    return db_car

def delete_car(db: Session, id: int):
    db_car = db.query(models.cars).filter(models.cars.id == id).first()
    if db_car:
        db.delete(db_car)
        db.commit()
    return db_car