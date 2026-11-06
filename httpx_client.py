from typing import cast

import time

import httpx

client = httpx.Client(
    base_url="http://localhost:8003",
    timeout=100,
    headers={"Authorization": "Bearer ..."}
 )


payload = {
    "email": f"user.{time.time()}@example.com",
    "lastName": "string",
    "firstName": "string",
    "middleName": "string",
    "phoneNumber": "string"
}

response = client.post("/api/v1/users", json=payload)

print(response.text)