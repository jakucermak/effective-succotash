from compose.utils import Compose, ComposeSet
import requests

def mock_requests_get(url):
    class MockResponse:
        def __init__(self, text, status_code):
            self.text = text
            self.status_code = status_code

    mock_html = """
    <html>
        <body>
            <a href="Fedora-41-20241011.n.0/">Fedora-41-20241011.n.0</a>
            <a href="Fedora-41-20241012.n.0/">Fedora-41-20241012.n.0</a>
            <a href="README">README</a>
        </body>
    </html>
    """
    return MockResponse(mock_html, 200)

def test_extract_versions(monkeypatch):
    monkeypatch.setattr(requests, "get", mock_requests_get)

    versions = ComposeSet.fetch()

    expected_versions = ["Fedora-41-20241011.n.0", "Fedora-41-20241012.n.0"]
    for i in range(2):
        assert versions.available_composes[i].build_name == expected_versions[i]
