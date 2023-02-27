from typing import TYPE_CHECKING, Optional

from hashlib import sha256

from sqlalchemy import select

from app.admin.models import AdminModel
from app.base.base_accessor import BaseAccessor

if TYPE_CHECKING:
    from app.web.app import Application
    from app.admin.models import Admin


class AdminAccessor(BaseAccessor):

    async def get_by_email(self, email: str) -> Optional["Admin"]:
        async with self.app.database.session() as session:
            query = select(AdminModel).where(AdminModel.email == email)
            result = await session.execute(query)
            admin = result.scalars().first()
            if admin:
                return admin.create_dataclass()

    async def create_admin(self, email: str, password: str) -> "Admin":
        async with self.app.database.session() as session:
            admin = AdminModel(email=email, password=sha256(password.encode()).hexdigest())
            session.add(admin)
            await session.commit()
            return admin.create_dataclass()
        
    async def connect(self, app: "Application"):
        admin = await self.get_by_email(self.app.config.admin.email)
        if admin and admin.is_password_valid(self.app.config.admin.password):
            return
        else:
            await self.create_admin(email=self.app.config.admin.email, password=self.app.config.admin.password)
