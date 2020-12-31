from count_substring import application as apps
from count_substring import get_value
import json


def test_home_route():
    client = apps.test_client()
    url = '/'
    response = client.get(url)
    assert response.status_code == 200 and response.get_data() == b'hello'


def test_count_route():
    client = apps.test_client()
    url = '/count/?substring=a'
    json_input = {"string": ["ans"]}
    response = client.post(url, data=json.dumps(json_input))
    assert response.status_code == 200


def test_result_route():
    client = apps.test_client()
    url = '/result/abc'
    response = client.get(url)
    assert response.status_code == 200


def test_post_route_success():
    ans = get_value(["ans"], 'a')
    assert "percent" and "occurrence" in ans and ans.get("occurrence") == [1]


def test_post_route_failure():
    try:
        get_value(["bbb"], 'a')
    except Exception as e:
        assert str(e) == "count in one or more string is 0"


def test_post_route_progress():
    ans = get_value(["aaa", "abc", "aaaa", "abca"], "a")
    assert "percent" in ans


def test_for_independent_celery_task():
    res = get_value(["abc"], 'a')
    assert {'occurrence': [1], 'percent': 100, 'string': ['abc']} == res

