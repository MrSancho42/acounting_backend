from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from services_manager import user_service
from domain import UserException

router = APIRouter(
    prefix='/user-services',
    tags=['user-services'],
    responses={404: {'description': 'Not found'}},
)


class AuthorizeUser(BaseModel):
    email: str
    password: str


class User(AuthorizeUser):
    name: str


class UserId(BaseModel):
    pk_user: int


class UpdateUser(UserId):
    name: str | None = None
    email: str | None = None
    password: str | None = None


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create(user: User):
    try:
        user_service.create(user.dict())
    except UserException.MailAlreadyInUse:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already in use')


@router.get('/read/{pk_user}', response_model=User, status_code=status.HTTP_200_OK)
async def read(pk_user: int):
    user = user_service.read(pk_user)
    return {
        'name': user.name,
        'email': user.email,
        'password': user.password
    }


@router.get('/login', response_model=UserId, status_code=status.HTTP_200_OK)
async def login(email: str, password: str):
    try:
        user = user_service.find_user_by_email(email)
        if user.password != password:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Password mismatch')
        return {'pk_user': user.pk_user}
    except UserException.UserNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')


@router.patch('/update', status_code=status.HTTP_200_OK)
async def update(user: UpdateUser):
    try:
        user_service.update(user.pk_user, user.dict(exclude_unset=True))
    except UserException.MailAlreadyInUse:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Item not found')
