
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi import APIRouter

from ..auth.deps import get_current_admin_user

from ..database.dbconfig import get_db
from ..services.user import create_user, get_users, get_user_by_email, get_users_filtered, get_user_by_username, delete_user_by_id, update_role_by_id
from ..schemas.schemas import User, UserCreate, UserPublic, UserRegister

user_router = APIRouter()


@user_router.get("/users/{page_number}", response_model=list[User], tags=["user"])
def get_all_users(page_number: int, admin_user: Annotated[User, Depends(get_current_admin_user)], username: Optional[str] = None, full_name: Optional[str] = None, email: Optional[str] = None, role: Optional[str] = None,  db: Session = Depends(get_db)):
    users = []

    if (email or username or full_name or role):
        users = get_users_filtered(
            page_number, db, username=username, full_name=full_name, email=email, role=role)
    else:
        users = get_users(db, page_number)
    return users


# Registracija korisnika koji nije ni admin ni vozac i nema account (ne treba da bude prijavljen da bi koristio ovu rutu)
@user_router.post("/signup/", response_model=UserPublic, tags=['user'])
def register_user(user_in: UserRegister, db: Session = Depends(get_db)):
    user = get_user_by_email(db=db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user_create = UserRegister.model_validate(user_in)
    user = create_user(db=db, user_create=user_create)
    return user


@user_router.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["user"])
def delete_user(id: str, current_user: Annotated[User, Depends(get_current_admin_user)], db: Session = Depends(get_db)):
    return delete_user_by_id(id=id, db=db)


@ user_router.put("/users/{id}", response_model=User, tags=["user"])
def update_role(admin_user: Annotated[User, Depends(get_current_admin_user)], id: int, role_type: str, db: Session = Depends(get_db)):
    return update_role_by_id(id=id, role_type=role_type, db=db)
