import json

from aiohttp.web_exceptions import HTTPNotFound
from aiohttp_apispec import response_schema

from backend.app.items.schemas import KeyboardSuggestionsListSchema, MouseSuggestionsListSchema, \
    MousepadSuggestionsListSchema, SwitchSuggestionsListSchema, TabletSuggestionsListSchema
from backend.app.web.app import View, Request
from backend.app.web.response import json_response


class GetItemListView(View):
    def __init__(self, request: Request):
        super().__init__(request)
        self.item_schemas = {
            "switches": SwitchSuggestionsListSchema(),
            "keyboards": KeyboardSuggestionsListSchema(),
            "mice": MouseSuggestionsListSchema(),
            "mousepads": MousepadSuggestionsListSchema(),
            "tablets": TabletSuggestionsListSchema(),
        }

    @response_schema(
        schema=TabletSuggestionsListSchema,
        code=200,
        description="""
            Returns tablet list for dropdown suggestions.
            Only admin added items included.
            Sorted by relevance and name."""
    )
    @response_schema(
        schema=SwitchSuggestionsListSchema,
        code=200,
        description="""
            Returns switches list for dropdown suggestions.
            Only admin added items included.
            Sorted by relevance and name.
            Common items like "custom", "rubber dome" and "Cherry MX ****" go first."""
    )
    @response_schema(
        schema=MousepadSuggestionsListSchema,
        code=200,
        description="""
            Returns mousepad list for dropdown suggestions.
            Only admin added items included.
            Sorted by relevance and name.
            Common items like "noname", "none/desk" go first."""
    )
    @response_schema(
        schema=MouseSuggestionsListSchema,
        code=200,
        description="""
        Returns mouse list for dropdown suggestions.
        Only admin added items included.
        Sorted by relevance and name.
        Common items like "noname", "OEM mouse" go first.""",
    )
    @response_schema(
        schema=KeyboardSuggestionsListSchema,
        code=200,
        description="""
        Returns keyboards list for dropdown suggestions. 
        Only admin added items included. 
        Sorted by relevance and name. 
        Common items like "Custom", "laptop keyboard", "noname" go first.""",
    )
    async def get(self):
        item_type = self.request.match_info["items"]
        if item_type not in self.item_schemas:
            raise HTTPNotFound(reason=f"Requested item {item_type} not found")

        items = await self.store.items.get_items(item_type=item_type)
        return json_response(data=self.item_schemas[item_type].dump({item_type: items}))

    async def post(self):  # TODO add items view
        pass
