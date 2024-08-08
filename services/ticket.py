from datetime import datetime
import json
from math import ceil
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database import models
from schemas import schemas
from auth import deps


def get_tickets_one_user(
    db: Session,
    current_user: schemas.UserBase,
    page_number: int
):
    user = db.query(models.User).filter(
        models.User.username == current_user.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not authorized!")

    all_tickets = db.query(models.Ticket).filter(
        models.Ticket.passenger_id == user.id).order_by(models.Ticket.departure_date_time).offset((page_number-1)*10).limit(10).all()
    return all_tickets


def get_tickets_one_user_count(
    db: Session,
    current_user: schemas.UserBase,
):
    user = db.query(models.User).filter(
        models.User.username == current_user.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not authorized!")

    all_tickets = db.query(models.Ticket).filter(
        models.Ticket.passenger_id == user.id).order_by(models.Ticket.departure_date_time).all()

    return ceil(len(all_tickets) / 10)


def create_ticket(db: Session, ticket: schemas.Ticket, current_user: schemas.UserBase):
    user = db.query(models.User).filter(
        models.User.username == current_user.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not authorized!")

    user_id = user.id

    datetime_obj = datetime.fromisoformat(
        str(ticket.departure_date_time).replace('Z', '+00:00'))

    formatted_datetime_str = datetime_obj.strftime('%Y-%m-%d %H:%M')

    ticket.departure_date_time = formatted_datetime_str

    ticket_dict = ticket.model_dump()
    ticket_dict['passenger_id'] = user_id

    to_create = models.Ticket(**ticket_dict)

    db.add(to_create)
    db.commit()
    db.refresh(to_create)

    return to_create


def delete_ticket_user(db: Session, id: int, current_user: schemas.UserBase):

    ticket_to_delete = db.query(models.Ticket).filter(
        models.Ticket.id == id).first()

    if not ticket_to_delete:
        raise HTTPException(status_code=404, detail="Ticket not found!")

    db.delete(ticket_to_delete)

    db.commit()
