from tcp.tcp_client import AsyncTCPClient
import asyncio

client = AsyncTCPClient('localhost', 3000)

async def main():
    await client.start()

    # Example send/receive loop
    try:
        while True:
            await client.send("Hello, Server!")
            response = await client.receive()
            print(f"Server Response: {response}")
            client.acknowledge()
    except KeyboardInterrupt:
        print("Stopping client...")
    finally:
        await client.stop()
        
if __name__ == "__main__":
    asyncio.run(main())
