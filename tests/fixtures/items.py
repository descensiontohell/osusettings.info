from pytest import fixture


@fixture
def all_items():
    yield dict(
        mice=[
            {
                "width": None,
                "switch": None,
                "sensor": None,
                "weight": None,
                "length": None,
                "id": 193,
                "name": "noname",
                "height": None,
            },
            {
                "width": None,
                "switch": None,
                "sensor": None,
                "weight": None,
                "length": None,
                "id": 115,
                "name": "OEM Mouse",
                "height": None,
            },
            {
                "width": None,
                "switch": None,
                "sensor": None,
                "weight": None,
                "length": None,
                "id": 1,
                "name": "A4Tech Bloody Blazing A70",
                "height": None,
            },
        ],
        mousepads=[
            {
                "id": 89,
                "name": "noname",
            },
            {
                "id": 90,
                "name": "none/desk",
            },
            {
                "id": 1,
                "name": "A4Tech Bloody B-087S",
            },
        ],
        keyboards=[
            {
                "id": 180,
                "name": "noname",
            },
            {
                "id": 136,
                "name": "laptop keyboard",
            },
            {
                "id": 135,
                "name": "keypad",
            },
        ],
        switches=[
            {
                "id": 5,
                "name": "Custom",
            },
            {
                "id": 49,
                "name": "Rubber Dome",
            },
            {
                "id": 2,
                "name": "Cherry MX Black",
            },
        ],
        tablets=[],
    )


@fixture
def item_for_add():
    yield {"name": "add_test_item"}
