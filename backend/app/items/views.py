import json

from aiohttp.web_exceptions import HTTPNotFound
from aiohttp_apispec import response_schema, docs

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
        """,
        responses={
            "200 - 1": {"description": "Ok. Returns list of mice", "schema": MouseSuggestionsListSchema},
            "200 - 2": {"description": "Ok. Returns list of mousepads", "schema": MousepadSuggestionsListSchema},
            "200 - 3": {"description": "Ok. Returns list of keyboards", "schema": KeyboardSuggestionsListSchema},
            "200 - 4": {"description": "Ok. Returns list of switches", "schema": SwitchSuggestionsListSchema},
            "200 - 5": {"description": "Ok. Returns list of tablets", "schema": TabletSuggestionsListSchema},
            "404": {"description": "Requested item not found"}
        }
    )
    async def get(self):
        item_type = self.request.match_info["item_type"]
        if item_type not in self.item_schemas:
            raise HTTPNotFound(reason=f"Requested item {item_type} not found")

        items = await self.store.items.get_items(item_type=item_type)

        return json_response(data=self.item_schemas[item_type].dump({item_type: items}))

    async def post(self):  # TODO add items view
        pass
