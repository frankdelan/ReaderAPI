from sqlalchemy.exc import IntegrityError


class BaseRepository:
    def __init__(self, session, model):
        self.session = session
        self.model = model

    async def add(self, obj):
        self.session.add(obj)
        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise ValueError('Object already exists')
        await self.session.refresh(obj)
        return obj

    async def update(self, obj):
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj):
        await self.session.delete(obj)
        await self.session.commit()
        return obj.id
