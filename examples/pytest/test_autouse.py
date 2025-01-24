# test_autouse.py

import pytest
import os

@pytest.fixture(autouse=True, scope="session")
def set_test_mode_env():
    """
    This fixture automatically runs before and after every test in this file.
    It sets an environment variable before the test, then cleans up afterwards.
    """
    print("\n[autouse fixture] Setting environment variable for test mode.")
    os.environ["MY_APP_TEST_MODE"] = "1"

    yield

    print("[autouse fixture] Cleaning up environment variable.")
    os.environ.pop("MY_APP_TEST_MODE", None)

def test_first():
    # The environment variable is set automatically by set_test_mode_env
    assert os.getenv("MY_APP_TEST_MODE") == "1"
    print("Running test_first...")

def test_second():
    # The environment variable is still set for this test
    assert os.getenv("MY_APP_TEST_MODE") == "1"
    print("Running test_second...")
