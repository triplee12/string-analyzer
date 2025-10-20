import os
import sys
import pytest
from fastapi.testclient import TestClient
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import app

client = TestClient(app)


def test_full_flow():
    payload = {"value": "RaceCar"}
    r = client.post("/strings", json=payload)
    assert r.status_code == 201
    body = r.json()
    assert body["value"] == "RaceCar"
    assert body["properties"]["is_palindrome"] is True

    r2 = client.get("/strings/RaceCar")
    assert r2.status_code == 200
    b2 = r2.json()
    assert b2["value"] == "RaceCar"

    r3 = client.delete("/strings/RaceCar")
    assert r3.status_code == 204

    r4 = client.get("/strings/RaceCar")
    assert r4.status_code == 404


def test_conflict_on_duplicate():
    payload = {"value": "hello"}
    r1 = client.post("/strings", json=payload)
    assert r1.status_code == 201
    r2 = client.post("/strings", json=payload)
    assert r2.status_code == 409


def test_list_filters():
    client.post("/strings", json={"value": "aba"})
    client.post("/strings", json={"value": "notpal"})
    r = client.get('/strings?is_palindrome=true')
    assert r.status_code == 200
    data = r.json()
    assert data["count"] >= 1


def test_nl_filter():
    client.post("/strings", json={"value": "level"})
    r = client.get('/strings/filter-by-natural-language', params={"query": "all single word palindromic strings"})
    assert r.status_code == 200
    js = r.json()
    assert js["interpreted_query"]["parsed_filters"]["word_count"] == 1
    assert js["interpreted_query"]["parsed_filters"]["is_palindrome"] == True
