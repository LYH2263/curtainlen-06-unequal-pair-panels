from fastapi.testclient import TestClient


def _runs(client: TestClient):
    return client.get("/api/runs").json()["items"]


def test_dry_run_returns_split_without_history(client):
    r = client.get("/api/estimate?window_id=1&fabric_id=1&left_ratio=0.4")
    assert r.status_code == 200
    body = r.json()
    assert body["panels"] == 5
    assert body["left_panels"] == 2
    assert body["right_panels"] == 3
    assert body["left_ratio"] == 0.4
    assert body["run_id"] is None
    assert _runs(client) == []


def test_save_pins_ratio_and_split(client):
    r = client.post("/api/estimate", json={
        "window_id": 1, "fabric_id": 1, "save": True, "left_ratio": 0.4,
    })
    assert r.status_code == 200
    run_id = r.json()["run_id"]
    saved = _runs(client)[0]["result"]
    assert saved["left_ratio"] == 0.4
    assert saved["left_panels"] == 2
    assert saved["right_panels"] == 3
    assert saved["meters"] == r.json()["meters"]
    assert run_id == _runs(client)[0]["id"]


def test_invalid_ratio_fails_and_writes_nothing(client):
    before = _runs(client)
    r = client.get("/api/estimate?window_id=1&fabric_id=1&save=true&left_ratio=1.5")
    assert r.status_code == 422
    assert _runs(client) == before


def test_saved_run_immutable_when_ratio_changes_later(client):
    first = client.post("/api/estimate", json={
        "window_id": 1, "fabric_id": 1, "save": True, "left_ratio": 0.4,
    }).json()
    run_id = first["run_id"]

    # 之后再用别的占比试算/保存，旧单按编号回看仍是写入时的左右幅
    client.post("/api/estimate", json={
        "window_id": 1, "fabric_id": 1, "save": False, "left_ratio": 0.9,
    })
    pinned = next(x for x in _runs(client) if x["id"] == run_id)["result"]
    assert pinned["left_ratio"] == 0.4
    assert (pinned["left_panels"], pinned["right_panels"]) == (2, 3)


def test_window_runs_filter(client):
    client.post("/api/estimate", json={"window_id": 1, "fabric_id": 1, "save": True})
    client.post("/api/estimate", json={"window_id": 2, "fabric_id": 1, "save": True})
    ids = [x["window_id"] for x in _runs(client)]
    assert set(ids) == {1, 2}
    only1 = client.get("/api/runs?window_id=1").json()["items"]
    assert [x["window_id"] for x in only1] == [1]
