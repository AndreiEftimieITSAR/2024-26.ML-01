import pytest
from app import app as flask_app

@pytest.fixture()
def client():
    flask_app.config.update({"TESTING": True})
    with flask_app.test_client() as client:
        yield client

def test_infer(client):
    test_data = {
        "symboling": 0,
        "fueltype": "gas",
        "aspiration": "std",
        "doornumber": "four",
        "carbody": "sedan",
        "drivewheel": "fwd",
        "enginelocation": "front",
        "wheelbase": 88.6,
        "carlength": 168.8,
        "carwidth": 64.1,
        "carheight": 48.8,
        "curbweight": 2548,
        "enginetype": "ohc",
        "cylindernumber": "four",
        "enginesize": 130,
        "fuelsystem": "mpfi",
        "boreratio": 3.47,
        "stroke": 2.68,
        "compressionratio": 9.0,
        "horsepower": 111,
        "peakrpm": 5000,
        "citympg": 21,
        "highwaympg": 27
    }

    response = client.post("/infer", json=test_data)
    assert response.status_code == 200
    data = response.get_json()
    assert "prediction" in data
    assert isinstance(data["prediction"], float)