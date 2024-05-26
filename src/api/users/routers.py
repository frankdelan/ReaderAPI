from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.services.users import UserService
from database import get_async_session
from api.users.utils import hash_password, verify_password

router = APIRouter(
    prefix='/user',
    tags=['User']
)


@router.post('/register')
async def register_user(user_id: int, password: str,
                        session: AsyncSession = Depends(get_async_session)):
    hashed_password: str = await hash_password(password)
    try:
        await UserService.add_user(session, user_id, hashed_password)
        return {'status': 'success',
                'data': None,
                'detail': 'Пользователь зарегистрирован'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/auth')
async def auth_user(user_id: int, password: str,
                    session: AsyncSession = Depends(get_async_session)):
    hashed_password: str = await UserService.get_password(session, user_id)
    if await verify_password(password, hashed_password):
        return {'status': 'success',
                'data': None,
                'detail': 'Пользователь прошел аутентификацию'}
    else:
        return {'status': 'error',
                'data': None,
                'detail': 'Неверный пароль'}



