import pytest

# takes advantage of the fixture
# pass in as a higher order function
def test_get_all_breakfast_with_empty_db_return_empty_list(client):
    # ARRANGE / ACT
    response = client.get("/breakfast")
    response_body = response.get_json() # returns data in a dictionary format

    # ASSERT
    assert response_body == []
    assert response.status_code == 200


def test_get_one_breakfast_with_empty_db_return_404_error(client):
    # ARRANGE / ACT
    response = client.get("/breakfast/1")
    response_body = response.get_json() # returns data in a dictionary format

    # ASSERT
    assert response_body == {"msg": "Could not find breakfast item with id: 1"}
    assert response.status_code == 404


def test_get_one_breakfast_from_db_with_three_breakfasts_return_breakfast_json(client, three_breakfasts):
    # ARRANGE / ACT
    response = client.get("/breakfast/1", json=three_breakfasts)
    response_body = response.get_json() # returns data in a dictionary format

    # ASSERT
    assert response_body == {"id":1, "name":"cereal", "rating":5.0, "prep_time":1}
    assert response.status_code == 200


def test_post_new_breakfast_creates_new_bf_in_db(client, three_breakfasts):
    # ARRANGE / ACT
    response = client.post("/breakfast", json={
        "name": "hashbrowns",
        "rating": 4.5,
        "prep_time": 10
    })
    response_body = response.get_json()

    # ASSERT
    assert "msg" in response_body
    assert response_body == {"msg": "Breakfast hashbrowns successfully created"}
    assert response.status_code == 201

