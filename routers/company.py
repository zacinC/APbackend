from typing import Annotated, List, Optional
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import APIRouter, status

from auth.deps import get_current_admin_user, get_current_driver_user

from database.dbconfig import get_db
from services.company import get_all_companies, insert_company
from schemas import schemas
from datetime import datetime

company_router = APIRouter()


@company_router.get("/companies", response_model=List[schemas.CompanyShow], tags=["company"])
def get_companies(search: Optional[str] = None, db: Session = Depends(get_db)):
    return get_all_companies(search, db)


@company_router.post("/companies", response_model=schemas.Company, tags=["company"])
def post_company(current_user: Annotated[schemas.User, Depends(get_current_admin_user)], company: schemas.CompanyCreate, db: Session = Depends(get_db)):
    return insert_company(company, db)
