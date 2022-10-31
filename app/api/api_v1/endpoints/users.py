from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.connect import get_db
from app import repo, dao
from app.api import deps

router = APIRouter()


@router.get("/", response_model=list[dao.User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve users.
    """
    users = repo.user_repo.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=dao.User)
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: dao.UserCreate,
):
    """
    Create new user.
    """
    user = repo.user_repo.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = repo.user_repo.create(db, obj_in=user_in)

    return user
