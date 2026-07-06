from app.sql.repo.key import KeyRepository
from app.sql.repo.base import BaseRepository
from app.sql.repo.user import UserRepository


class Repo(BaseRepository):
    def __init__(self, session):
        super().__init__(session)
        self.key = KeyRepository(session)
        self.user = UserRepository(session)
