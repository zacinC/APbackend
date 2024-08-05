
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi import APIRouter

from auth.utils import generate_account_registration_email, send_email

from auth.deps import get_current_active_user, get_current_admin_user

from database.dbconfig import get_db
from services.user import create_user, get_users, get_user_by_email, get_users_filtered, get_user_by_username, delete_user_by_id, update_single_user, get_count_users, get_count_users_filtered
from schemas import schemas

user_router = APIRouter()


@user_router.get("/user/me", response_model=schemas.UserPublic, tags=['user'])
async def read_users_me(
    current_user: Annotated[schemas.UserPublic,
                            Depends(get_current_active_user)]
):
    return current_user


@user_router.get("/users/count", response_model=int, tags=["user"])
def get_users_count(admin_user: Annotated[schemas.User, Depends(get_current_admin_user)], username: Optional[str] = None, full_name: Optional[str] = None, email: Optional[str] = None, role: Optional[str] = None,  db: Session = Depends(get_db)):
    if (email or username or full_name or role):
        return get_count_users_filtered(db, email, username, full_name, role)

    return get_count_users(db)


@user_router.get("/users/{page_number}", response_model=list[schemas.User], tags=["user"])
def get_all_users(page_number: int, admin_user: Annotated[schemas.User, Depends(get_current_admin_user)], username: Optional[str] = None, full_name: Optional[str] = None, email: Optional[str] = None, role: Optional[str] = None,  db: Session = Depends(get_db)):
    users = []

    if (email or username or full_name or role):
        users = get_users_filtered(
            page_number, db, username=username, full_name=full_name, email=email, role=role)
    else:
        users = get_users(db, page_number)
    return users


# Registracija korisnika koji nije ni admin ni vozac i nema account (ne treba da bude prijavljen da bi koristio ovu rutu)
@user_router.post("/signup/", response_model=schemas.UserPublic, tags=['user'])
def register_user(user_in: schemas.UserRegister, db: Session = Depends(get_db)):
    user = get_user_by_email(db=db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user_create = schemas.UserRegister.model_validate(user_in)
    user = create_user(db=db, user_create=user_create)

    email_data = generate_account_registration_email(user)
    send_email(user, email_data["html_content"], email_data["subject"])

    return user


@user_router.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["user"])
def delete_user(id: str, current_user: Annotated[schemas.User, Depends(get_current_admin_user)], db: Session = Depends(get_db)):
    return delete_user_by_id(id=id, db=db)


@user_router.put("/users/{id}", response_model=schemas.User, tags=["user"])
def update_user(id: int, update: schemas.UserUpdate, db: Session = Depends(get_db)):
    return update_single_user(id=id, updated_user=update, db=db)
