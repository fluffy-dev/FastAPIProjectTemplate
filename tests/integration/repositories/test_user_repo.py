import pytest
from sqlalchemy import select

from src.auth.repositories.user import UserRepository
from src.auth.entities import UserEntity
from src.auth.models.user import UserModel
from src.auth.exceptions.user import UserAlreadyExist, UserNotFound
from src.auth.dto import UpdateUserDTO, FindUserDTO

pytestmark = pytest.mark.asyncio

async def test_create_user(db_session):
    """
    Verifies that a user can be successfully persisted to the database.
    """
    repo = UserRepository(db_session)
    entity = UserEntity(
        name="Test User",
        login="test_user",
        email="test@example.com",
        password="hashed_secret"
    )

    result = await repo.create(entity)

    assert result.id is not None
    assert result.email == "test@example.com"

    # Verify directly in DB
    stmt = select(UserModel).where(UserModel.id == result.id)
    db_result = await db_session.execute(stmt)
    user_in_db = db_result.scalar_one()
    assert user_in_db.login == "test_user"

async def test_create_duplicate_user_raises_error(db_session):
    """
    Verifies that the repository raises UserAlreadyExist on unique constraint violation.
    """
    repo = UserRepository(db_session)
    entity = UserEntity(
        name="User 1",
        login="unique_login",
        email="unique@example.com",
        password="hashed"
    )
    await repo.create(entity)

    with pytest.raises(UserAlreadyExist):
        await repo.create(entity)

async def test_find_user_by_criteria(db_session):
    """
    Verifies dynamic searching via FindUserDTO.
    """
    repo = UserRepository(db_session)
    # Arrange: Create user manually or via factory
    user = UserModel(name="A", login="find_me", email="a@a.com", password="pw")
    db_session.add(user)
    await db_session.commit()

    # Act
    dto = FindUserDTO(login="find_me")
    found_user = await repo.find(dto)

    assert found_user is not None
    assert found_user.login == "find_me"

async def test_update_user_not_found(db_session):
    """
    Verifies that updating a non-existent user raises UserNotFound.
    """
    repo = UserRepository(db_session)
    update_dto = UpdateUserDTO(name="New Name")

    with pytest.raises(UserNotFound):
        await repo.update(update_dto, pk=9999)