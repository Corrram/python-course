def write_message_to_file(filename, message):
    """
    Writes the provided message to the specified file.
    Overwrites any existing content in the file.
    """
    with open(filename, 'w') as f:
        f.write(message)

def read_message_from_file(filename):
    """
    Reads and returns the content from the specified file.
    """
    with open(filename, 'r') as f:
        return f.read()
