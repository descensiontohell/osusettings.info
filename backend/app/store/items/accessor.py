import typing
import _pickle as pickle
from typing import Union

from aiohttp.web_exceptions import HTTPNotFound
from sqlalchemy import select, desc

from backend.app.store.base.base_accessor import BaseAccessor
from backend.app.store.database.models import KeyboardModel, MouseModel, MousepadModel, SwitchModel, TabletModel
from backend.app.store.players.dataclasses import Keyboard, Mouse, Mousepad, Tablet, Switch

if typing.TYPE_CHECKING:
    from backend.app.web.app import Application


class ItemsAccessor(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, "Items", *args, **kwargs)
        self.app = app
        self.item_types = {
            "keyboards": KeyboardModel,
            "mice": MouseModel,
            "mousepads": MousepadModel,
            "switches": SwitchModel,
            "tablets": TabletModel,
        }

    async def get_items(self, item_type: str) -> list[Union[Keyboard, Mouse, Mousepad, Switch, Tablet]]:
        try:
            model = self.item_types[item_type]
        except KeyError:
            raise HTTPNotFound(reason=f"Requested item {item_type} not found")

        # Checks cached
        if self.app.const.ENABLE_CACHING:
            pickled_items = await self.app.store.redis.get(item_type)
            if pickled_items:
                items_list = pickle.loads(pickled_items)
                return items_list

        # Does CRUD if not cached
        query = select(model)
        model_query = query.where(model.relevance > 0).order_by(desc(model.relevance)).order_by(model.name)
        result = await self.app.database.db.execute(model_query)
        models = result.scalars().all()

        items_list = [m.to_dc() for m in models if m]

        # Puts into cache
        if self.app.const.ENABLE_CACHING:
            pickled_items = pickle.dumps(items_list)
            await self.app.store.redis.set(item_type, pickled_items, ex=self.app.const.CACHE_EX)

        return items_list

