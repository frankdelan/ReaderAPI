from fastapi import APIRouter, Depends, HTTPException

from api.services.users import UserService
from api.users.schemas import AuthUser
from api.users.utils import hash_password, verify_password

router = APIRouter(
    prefix='/user',
    tags=['User']
)


@router.post('/register')
async def register_user(data: AuthUser,
                        user_service: UserService = Depends(UserService)):
    data.password = await hash_password(data.password)
    try:
        await user_service.add_user(data)
        return {'status': 'success',
                'data': None,
                'detail': 'Пользователь зарегистрирован'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/auth')
async def auth_user(data: AuthUser,
                    user_service: UserService = Depends(UserService)):
    hashed_password: str = await user_service.get_user_password(data.user_id)
    if await verify_password(data.password, hashed_password):
        return {'status': 'success',
                'data': None,
                'detail': 'Пользователь прошел аутентификацию'}
    else:
        return {'status': 'error',
                'data': None,
                'detail': 'Неверный пароль'}



