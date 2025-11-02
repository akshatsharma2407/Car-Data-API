from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
import crud, models, schemas
from fastapi import FastAPI, HTTPException, Depends, Path, Query
from typing import List
from predict import make_prediction, make_batch_prediction

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@app.get('/cars', response_model= List[schemas.CarOut])
def get_cars(sortby : str = Query('id', description='name of column on which you want to sort'), orderby: str = Query('asc', description='asc or desc'),db: Session = Depends(get_db)):
    if sortby not in ['id','price']:
        raise HTTPException(status_code=400, detail='wrong attribute, select from "id" or "price"')
    if orderby not in ['asc','desc']:
        raise HTTPException(status_code=400, detail='wrong attribute, select from "asc" or "desc"')
    return crud.get_cars(db=db, sortby=sortby, orderby=orderby)

@app.get('/cars/{id}', response_model=schemas.CarOut)
def get_car(id: int = Path(..., description='id of car you want to fatch', examples=[1,2,3]), db: Session = Depends(get_db)):
    car = crud.get_car(id=id,db=db)
    if car is None:
        raise HTTPException(status_code=404, detail='Car not found')
    return car

@app.post('/create_car', response_model=schemas.CarOut)
def create_car(car: schemas.CarCreate, db: Session = Depends(get_db)):
    return crud.create_car(car=car, db=db)

@app.put('/update_car/{id}', response_model=schemas.CarOut)
def update_car(car: schemas.CarUpdate,id: int = Path(..., description='id of car you want to update', examples=[1,2,3]), db: Session = Depends(get_db)):
    db_car = crud.update_car(car=car, id=id, db=db)
    if db_car is None:
        raise HTTPException(status_code=404, detail='car not found')
    return db_car

@app.delete('/delete_car/{id}', response_model=schemas.CarOut)
def delete_car(id: int = Path(..., description='id of car you want to delete',examples=[1,2,3]), db: Session = Depends(get_db)):
    db_car = crud.delete_car(db=db,id=id)
    if db_car is None:
        raise HTTPException(status_code=404, detail='car not found')
    return db_car

@app.post('/prediction', response_model=schemas.PredictionOutputSchema)
def predict(user_input : schemas.PredictionInputSchema):
    prediction = make_prediction(user_input.model_dump())
    return schemas.PredictionOutputSchema(Price= round(prediction,2))


@app.post('/batch_prediction',response_model=List[schemas.PredictionOutputSchema])
def batch_predict(user_Inputs: List[schemas.PredictionInputSchema]):
    predictions = make_batch_prediction([x.model_dump() for x in user_Inputs])
    return [schemas.PredictionOutputSchema(Price=round(prediction,2)) for prediction in predictions]