from examples.pytest.mocking.email_client import notify_all_customers

def test_notify_all_customers(mocker):
    """
    Demonstrates how to mock both the DB call and the email sending
    using the pytest-mock extension (mocker fixture).
    """
    # Mock the database call to return predictable data
    mock_get_customers = mocker.patch(
        "examples.pytest.mocking.email_client.database.get_customers",
        return_value=[
            {"FirstName": "John", "LastName": "Doe", "Email": "john@example.com"},
            {"FirstName": "Jane", "LastName": "Smith", "Email": "jane@example.com"}
        ]
    )

    # Mock the email sending function
    mock_send_email = mocker.patch("examples.pytest.mocking.email_client.send_email")

    # Call the function that normally reads from DB and sends email
    fake_db_path = "/path/to/fake/music.db"
    notify_all_customers(fake_db_path)

    # Assertions: confirm we called get_customers and send_email properly
    mock_get_customers.assert_called_once_with(fake_db_path)
    assert mock_send_email.call_count == 2

    # (Optional) Check details of the calls
    mock_send_email.assert_any_call(
        recipient="john@example.com",
        subject="New Music Release",
        body="Hello John Doe,\nWe have new music for you to enjoy!"
    )
    mock_send_email.assert_any_call(
        recipient="jane@example.com",
        subject="New Music Release",
        body="Hello Jane Smith,\nWe have new music for you to enjoy!"
    )
