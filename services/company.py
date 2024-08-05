from typing import Optional
from sqlalchemy.orm import Session

from schemas import schemas
from database import models


def get_all_companies(search: str, db: Session):
    if not search:
        search = ""

    return db.query(models.Company).filter(models.Company.company_name.like(f'%{search}%')).all()


def insert_company(company: schemas.CompanyCreate, db: Session):
    to_insert = models.Company(company_name=company.company_name)

    db.add(to_insert)
    db.commit()

    db.refresh(to_insert)

    return to_insert
