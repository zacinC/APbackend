from typing import Annotated, List, Optional
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import APIRouter, status

from auth.deps import get_current_active_user, get_current_user

from database.dbconfig import get_db
from services.ticket import get_tickets_one_user, create_ticket, delete_ticket_user, get_tickets_one_user_count
from schemas import schemas

ticket_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@ticket_router.get("/tickets/count", response_model=int, tags=["tickets"])
async def get_count_tickets(current_user: Annotated[schemas.User, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    return get_tickets_one_user_count(db, current_user)


@ticket_router.get("/tickets/{page_number}", response_model=List[schemas.Ticket], tags=["tickets"])
async def get_all_tickets_one_user(page_number: int, current_user: Annotated[schemas.User, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    tickets = get_tickets_one_user(db, current_user, page_number)
    return tickets


@ticket_router.post("/tickets", response_model=schemas.Ticket, tags=["tickets"])
async def post_ticket(ticket: schemas.TicketCreate, current_user: Annotated[schemas.User, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    return create_ticket(db=db, ticket=ticket, current_user=current_user)


@ticket_router.delete("/tickets", status_code=status.HTTP_204_NO_CONTENT, tags=["tickets"])
async def delete_ticket(id: int, current_user: Annotated[schemas.User, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    return delete_ticket_user(db=db, id=id, current_user=current_user)
