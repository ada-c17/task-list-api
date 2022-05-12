# for code coverage purpose
from app.routes.helpers import post_slack_message
import pytest

@pytest.mark.skip(reason="No way to test this feature yet")
def test_post_message_return_True():
    assert post_slack_message("Hello World!") == True

def test_post_empty_message_return_false():
    assert post_slack_message("") == False