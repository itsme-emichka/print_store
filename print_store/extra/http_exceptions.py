from fastapi import HTTPException, status


AuthError = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Unrecognized token',
    )


AlreadyExistsError = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail='Already exists'
)


Error404 = HTTPException(status_code=status.HTTP_404_NOT_FOUND)


WrongPasswordError = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Неверный пароль',
)
