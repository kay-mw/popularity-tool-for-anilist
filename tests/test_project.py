def test_home(client):
    client.get('/')
    assert b"<title>How Popular is Your Anime Taste?</title>"