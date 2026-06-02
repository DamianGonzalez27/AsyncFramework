from src.modules.clients.services.client_service import ClientService


def test_create_client_returns_payload_with_default_id():
    service = ClientService()
    result = service.create_client({"name": "Test Client"})

    assert result["id"].startswith("client-")
    assert result["name"] == "Test Client"
    assert result["metadata"] == {}
