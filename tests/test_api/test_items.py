from tests.client import client


class TestAllItems:
    def test_get_items(self, all_items):
        resp = client.request("/items", method="GET")
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert data
        assert data["keyboards"][0:3] == all_items["keyboards"]
        assert data["mice"][0:3] == all_items["mice"]
        assert data["mousepads"][0:3] == all_items["mousepads"]
        assert data["switches"][0:3] == all_items["switches"]
        assert data["tablets"] == []

    # def test_add_item(self, item_for_add):
    #     resp = client.request("/items/keyboards", method="POST", json=item_for_add)
    #     assert resp.status_code == 200
    #     check_resp = client.request("/items/keyboards", method="GET")
    #     data = check_resp.json()["data"]["keyboards"]
    #     items_names = [d["name"] for d in data]
    #     assert item_for_add["name"] in items_names

    def test_unauthorized_add_item(self):
        resp = client.unauthorized_request("/items/mice", method="POST", json={"name": "placeholder"})
        assert resp.status_code == 401
