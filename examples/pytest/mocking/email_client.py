from examples.pytest.mocking import database


def send_email(recipient, subject, body):
    """
    Simulates sending an email.
    In a real application, this might connect to
    an SMTP server or another email API.
    """
    print(f"Sending email to {recipient}")
    print(f"Subject: {subject}")
    print(f"Body: {body}")


def notify_all_customers(db_path):
    """
    Retrieves a list of customers from the specified database
    and sends each of them an email notification.
    """
    customers = database.get_customers(db_path)
    for customer in customers:
        subject = "New Music Release"
        body = (
            f"Hello {customer['FirstName']} {customer['LastName']},\n"
            "We have new music for you to enjoy!"
        )
        send_email(
            recipient=customer['Email'],
            subject=subject,
            body=body
        )
