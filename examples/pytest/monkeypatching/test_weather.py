import requests

from examples.pytest.monkeypatching.weather import get_weather


def test_get_weather(monkeypatch):
    """
    Test get_weather by monkeypatching requests.get
    so it returns a fake response instead of making a real HTTP call.
    """

    # 1. Define a mock function that will replace requests.get
    def mock_get(url, *args, **kwargs):
        # Create a class to mock the requests.Response object
        class MockResponse:
            def __init__(self, json_data, status_code):
                self._json_data = json_data
                self.status_code = status_code

            def json(self):
                return self._json_data

        # We ignore `url` or process it if needed
        # Return a mocked response object
        return MockResponse({"temp": 25}, 200)

    # 2. Use monkeypatch.setattr to replace requests.get with mock_get
    monkeypatch.setattr(requests, "get", mock_get)

    # 3. Call the function under test
    temperature = get_weather("London")

    # 4. Verify the function behaves as expected with the mock
    assert temperature == 25, "Expected temperature to match mocked response"
