from aiohttp.web_exceptions import HTTPNotFound, HTTPUnauthorized, HTTPForbidden, HTTPUnprocessableEntity
from aiohttp_apispec import docs, response_schema
from marshmallow import ValidationError

from backend.app.items.schemas import KeyboardSuggestionsListSchema, MouseSuggestionsListSchema, \
    MousepadSuggestionsListSchema, SwitchSuggestionsListSchema, TabletSuggestionsListSchema, AllItemsSchema, \
    PlaystyleSuggestionsListSchema
from backend.app.players.schemas import SwitchSchema, TabletSchema, MousepadSchema, MouseSchema, KeyboardSchema, \
    PlaystyleSchema
from backend.app.store.database.models import SwitchModel, KeyboardModel, MouseModel, MousepadModel, TabletModel, \
    PlaystyleModel
from backend.app.web.app import View
from backend.app.web.response import json_response


item_schemas_models = {
    "switches": [SwitchSuggestionsListSchema(), SwitchModel, SwitchSchema()],
    "keyboards": [KeyboardSuggestionsListSchema(), KeyboardModel, KeyboardSchema()],
    "mice": [MouseSuggestionsListSchema(), MouseModel, MouseSchema()],
    "mousepads": [MousepadSuggestionsListSchema(), MousepadModel, MousepadSchema()],
    "tablets": [TabletSuggestionsListSchema(), TabletModel, TabletSchema()],
    "playstyles": [PlaystyleSuggestionsListSchema(), PlaystyleModel, PlaystyleSchema()],
}


class GetItemListView(View):

    @docs(
        tags=["Items"],
        summary="Returns item lists for dropdown suggestions",
        description="""Returns items list for dropdown suggestions. Only admin added items included.
        Sorted by relevance and name. Common items like "Custom", "laptop keyboard", "noname" go first.
        Available items:

        keyboards

        switches

        tablets

        mice

        mousepads
        
        playstyles
        """,
        responses={
            "200 - 1": {"description": "Ok. Returns list of mice", "schema": MouseSuggestionsListSchema},
            "200 - 2": {"description": "Ok. Returns list of mousepads", "schema": MousepadSuggestionsListSchema},
            "200 - 3": {"description": "Ok. Returns list of keyboards", "schema": KeyboardSuggestionsListSchema},
            "200 - 4": {"description": "Ok. Returns list of switches", "schema": SwitchSuggestionsListSchema},
            "200 - 5": {"description": "Ok. Returns list of tablets", "schema": TabletSuggestionsListSchema},
            "200 - 6": {"description": "Ok. Returns list of playstyles", "schema": PlaystyleSuggestionsListSchema},
            "404": {"description": "Requested item not found"}
        }
    )
    async def get(self):
        item_type = self.request.match_info["item_type"]
        if item_type not in item_schemas_models:
            raise HTTPNotFound(reason=f"Requested item {item_type} not found")
        items = await self.store.items.get_items(item_type=item_type, model=item_schemas_models[item_type][1])
        return json_response(data=item_schemas_models[item_type][0].dump({item_type: items}))

    @docs(
        tags=["Items"],
        summary="Add item [admin]",
        description="""Add item endpoint for admins, all added items are displayed in suggestion lists
        Available items:

        keyboards

        switches

        tablets

        mice

        mousepads
        """,
        responses={
            "200": {"description": "Success"},
            "401": {"description": "User not authorized"},
            "403": {"description": "User is authorized but is not admin"},
            "404": {"description": "Requested item not found"},
        }
    )
    async def post(self):
        if not self.request.player_id:
            raise HTTPUnauthorized()
        if not self.request.is_admin:
            raise HTTPForbidden()

        item_type = self.request.match_info["item_type"]
        if item_type not in item_schemas_models:
            raise HTTPNotFound(reason=f"Requested item {item_type} not found")

        body = await self.request.json()
        try:
            item = item_schemas_models[item_type][2].load(body)
        except ValidationError as e:
            raise HTTPUnprocessableEntity(reason=e.data)

        await self.store.items.add_item(item, item_schemas_models[item_type][1])

        return json_response()


class GetAllItemsView(View):
    @docs(
        tags=["Items"],
        summary="Returns all items list",
        description="""Returns items list for dropdown suggestions. Only admin added items included.
        Sorted by relevance and name. Common items like "Custom", "laptop keyboard", "noname" go first.
        """,
    )
    @response_schema(AllItemsSchema, 200)
    async def get(self):
        mice = await self.store.items.get_items(item_type="mice", model=item_schemas_models["mice"][1])
        mousepads = await self.store.items.get_items(item_type="mousepads", model=item_schemas_models["mousepads"][1])
        keyboards = await self.store.items.get_items(item_type="keyboards", model=item_schemas_models["keyboards"][1])
        switches = await self.store.items.get_items(item_type="switches", model=item_schemas_models["switches"][1])
        tablets = await self.store.items.get_items(item_type="tablets", model=item_schemas_models["tablets"][1])
        playstyles = await self.store.items.get_items("playstyles", item_schemas_models["playstyles"][1])
        return json_response(data=AllItemsSchema().dump({
            "mice": mice,
            "mousepads": mousepads,
            "keyboards": keyboards,
            "switches": switches,
            "tablets": tablets,
            "playstyles": playstyles,
        }))
