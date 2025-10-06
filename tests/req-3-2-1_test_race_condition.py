import asyncio
import httpx

URL = "http://localhost:8000/api/v1/orders/"
HEADERS = {"Content-Type": "application/json"}
PAYLOAD = {
  "customer_id": "43e8ff2f-5d48-498f-a569-ca2cf9f7fae3",
  "product_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef"
}

TOTAL_REQUESTS = 100

# Track results
success_responses = []
failure_responses = []

async def send_request(client, index):
    try:
        response = await client.post(URL, json=PAYLOAD, headers=HEADERS)
        status = response.status_code
        content_type = response.headers.get("Content-Type", "")

        if "application/json" in content_type:
            data = response.json()
        else:
            data = {"raw": response.text}

        print(f"[{index}] Status: {status} | Response: {data}")

        if status == 202 and data.get("status") == "PENDING":
            success_responses.append(data)
        else:
            failure_responses.append(data)

    except Exception as e:
        print(f"[{index}] Error: {e}")
        failure_responses.append({"error": str(e)})
        
async def run_concurrent_requests():
    async with httpx.AsyncClient(timeout=5.0) as client:
        tasks = [send_request(client, i) for i in range(TOTAL_REQUESTS)]
        await asyncio.gather(*tasks)

    print("\nSummary:")
    print(f"  Successes (202 PENDING): {len(success_responses)}")
    print(f"  Failures/Errors:         {len(failure_responses)}")

if __name__ == "__main__":
    asyncio.run(run_concurrent_requests())