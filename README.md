# Async TCP Client (Python)

A small asyncio-based TCP client with:

- automatic reconnect (keep-alive loop)
- background read/write loops
- send/receive queues
- optional read timeout (to force reconnect if the server goes silent)
- simple send/receive “one-at-a-time” gating via `acknowledge()`

## Requirements

- Python 3.10+ (3.8+ likely works, but this repo is written with modern asyncio patterns)
- Dependency: `loguru`

## Setup

If you already have the provided `.venv/`, you can use it. Otherwise:

```bash
python -m venv .venv
source .venv/bin/activate
pip install loguru
```

## Run

`main.py` connects to `localhost:3000` and repeatedly sends a message, waits for a response, then unlocks the next send.

```bash
source .venv/bin/activate
python main.py
```

Make sure you have a TCP server listening on `localhost:3000`.

## How it works

- `AsyncTCPClient.start()` starts three background tasks:
  - `_keep_alive_loop()` connects (and reconnects) when disconnected
  - `_write_loop()` sends messages from `send_queue`
  - `_read_loop()` reads from the socket and pushes messages into `receive_queue`

- Sending is gated:
  - After a send, the client blocks further sends until you call `client.acknowledge()`.
  - This is useful for request/response protocols where you only want one in-flight request.

## Public API

- `AsyncTCPClient(host, port, read_timeout=None)`
  - `read_timeout=None` means “wait forever” on reads.
  - If set to a number of seconds, a read timeout triggers a reconnect.

- `await client.start()`
- `await client.send(str_message)`
- `response = await client.receive()`
- `client.acknowledge()`
- `await client.stop()`

## Notes

- Messages are sent as UTF-8 bytes with no delimiter. If your server expects line-delimited messages, add a trailing `\n` when sending.
- The read loop uses `reader.read(4096)`; depending on your protocol, you may need framing (newline, length-prefix, etc.) to reliably separate messages.
