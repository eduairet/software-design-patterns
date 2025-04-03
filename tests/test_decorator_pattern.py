from software_design_patterns.structural.decorator_pattern import *
import re


def test_decorator_api_request():
    ENDPOINT = "https://api.thecatapi.com/v1/images/search?mime_types=jpg"
    data = {}
    method = RequestMethod.GET
    api_request = ApiRequest(ENDPOINT, data, method)
    logged_request = LoggerDecorator(api_request)
    print("\n")
    response = logged_request.send()

    assert response.status_code == 200

    data = response.json()
    assert "id" in data[0]
    assert "url" in data[0]
    assert "width" in data[0]
    assert "height" in data[0]
    assert re.match(
        r"^https://cdn2.thecatapi.com/images/[^\.]+\.jpe?g$", data[0]["url"]
    )
    assert isinstance(data[0]["id"], str)
    assert isinstance(data[0]["url"], str)
    assert isinstance(data[0]["width"], int)
    assert isinstance(data[0]["height"], int)
