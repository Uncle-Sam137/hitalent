import pytest


@pytest.mark.asyncio
async def test_create_chat(client):
    response = await client.post(
        "/chats/",
        json={"title": "Test chat"},
    )

    assert response.status_code == 201

    data = response.json()
    assert data["id"] > 0
    assert data["title"] == "Test chat"
    assert "created_at" in data


@pytest.mark.asyncio
async def test_create_message(client):
    chat_response = await client.post(
        "/chats/",
        json={"title": "Chat for messages"},
    )
    chat_id = chat_response.json()["id"]

    message_response = await client.post(
        f"/chats/{chat_id}/messages/",
        json={"text": "Hello"},
    )

    assert message_response.status_code == 201

    data = message_response.json()
    assert data["chat_id"] == chat_id
    assert data["text"] == "Hello"
    assert "created_at" in data


@pytest.mark.asyncio
async def test_get_chat_with_messages(client):
    chat_response = await client.post(
        "/chats/",
        json={"title": "Chat with history"},
    )
    chat_id = chat_response.json()["id"]

    await client.post(
        f"/chats/{chat_id}/messages/",
        json={"text": "First"},
    )
    await client.post(
        f"/chats/{chat_id}/messages/",
        json={"text": "Second"},
    )

    response = await client.get(f"/chats/{chat_id}?limit=10")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == chat_id
    assert len(data["messages"]) == 2
    assert data["messages"][0]["text"] == "First"
    assert data["messages"][1]["text"] == "Second"


@pytest.mark.asyncio
async def test_send_message_to_missing_chat(client):
    response = await client.post(
        "/chats/999999/messages/",
        json={"text": "Hello"},
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_chat(client):
    chat_response = await client.post(
        "/chats/",
        json={"title": "Chat to delete"},
    )
    chat_id = chat_response.json()["id"]

    response = await client.delete(f"/chats/{chat_id}")
    assert response.status_code == 204

    response = await client.get(f"/chats/{chat_id}")
    assert response.status_code == 404
