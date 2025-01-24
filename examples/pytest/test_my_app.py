import pytest
import tempfile
import os
import my_app

@pytest.fixture
def temp_file():
    """
    Creates a temporary file and yields its name to the test.
    After the test completes, the file is removed.
    """
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        file_name = tf.name
    yield file_name
    os.remove(file_name)  # Cleanup after test

def test_write_and_read(temp_file):
    """
    Tests that write_message_to_file correctly writes content
    and read_message_from_file accurately reads it back.
    """
    test_message = "Hello from my_app!"
    my_app.write_message_to_file(temp_file, test_message)

    result = my_app.read_message_from_file(temp_file)
    assert result == test_message

def test_overwrite_content(temp_file):
    """
    Demonstrates that writing new content overwrites old content.
    """
    first_message = "First message."
    second_message = "Second message, overwrote the first."

    # Write first message
    my_app.write_message_to_file(temp_file, first_message)

    # Overwrite with second message
    my_app.write_message_to_file(temp_file, second_message)
    result = my_app.read_message_from_file(temp_file)

    assert result == second_message
    assert result != first_message
