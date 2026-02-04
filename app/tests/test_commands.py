from ..utils.command_parser import parse_command

def test_read_command():
    assert parse_command("show my last emails")["action"] == "read"

def test_delete_command():
    assert parse_command("delete the latest email")["action"] == "delete"

def test_reply_command():
    assert parse_command("reply to this email")["action"] == "reply"
