from typing import List, Optional
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import APIRouter, status

from ..auth.deps import get_current_user

from ..database.dbconfig import get_db
from ..services.ticket import get_tickets_one_user, create_ticket, delete_ticket_user
from ..schemas import schemas

ticket_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@ticket_router.get("/tickets/{page_number}", response_model=List[schemas.Ticket], tags=["tickets"])
async def get_all_tickets_one_user(page_number:int,db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user: schemas.UserBase = await get_current_user(token=token, db=db)
    tickets = get_tickets_one_user(db, current_user,page_number)
    return tickets


@ticket_router.post("/tickets", response_model=schemas.Ticket, tags=["tickets"])
async def post_ticket(ticket: schemas.TicketCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user: schemas.UserBase = await get_current_user(token=token, db=db)
    return create_ticket(db=db, ticket=ticket, current_user=current_user)


@ticket_router.delete("/tickets", status_code=status.HTTP_204_NO_CONTENT, tags=["tickets"])
async def delete_ticket(id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user: schemas.UserBase = await get_current_user(token=token, db=db)
    return delete_ticket_user(db=db, id=id, current_user=current_user)
