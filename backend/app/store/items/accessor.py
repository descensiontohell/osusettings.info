import typing
import _pickle as pickle
from typing import Union, Optional

from sqlalchemy import select, desc

from backend.app.store.base.base_accessor import BaseAccessor
from backend.app.store.players.dataclasses import Keyboard, Mouse, Mousepad, Tablet, Switch

if typing.TYPE_CHECKING:
    from backend.app.web.app import Application


class ItemsAccessor(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, "Items", *args, **kwargs)
        self.app = app

    async def connect(self, app: "Application"):
        self.session_factory = self.app.database.db

    async def get_items(self, item_type: str, model) -> list[Union[Keyboard, Mouse, Mousepad, Switch, Tablet]]:
        """
        If cached: returns from cache
        Else: requests database and caches the result
        :param item_type:
        :param model:
        :return:
        """
        items_list = await self.get_from_cache(item_type)
        if items_list:
            return items_list

        query = select(model)
        model_query = query.where(model.relevance > 0).order_by(desc(model.relevance)).order_by(model.name)

        async with self.session_factory() as session:
            result = await session.execute(model_query)

        models = result.scalars().all()
        items_list = [m.to_dc() for m in models if m]
        await self.set_cache(items_list, item_type)

        return items_list

    async def get_from_cache(self, item_type) -> Optional[list[Union[Keyboard, Mouse, Mousepad, Switch, Tablet]]]:
        if self.app.const.ENABLE_CACHING:
            pickled_items = await self.app.store.redis.get(item_type)
            if pickled_items:
                self.logger.info("CACHED")
                items_list = pickle.loads(pickled_items)
                return items_list
        return None

    async def set_cache(self, items_list, item_type) -> None:
        if self.app.const.ENABLE_CACHING:
            pickled_items = pickle.dumps(items_list)
            await self.app.store.redis.set(item_type, pickled_items, ex=self.app.const.CACHE_EX)
