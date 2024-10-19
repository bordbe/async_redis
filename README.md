# Async Redis

![Tests](https://github.com/yourusername/async_redis/workflows/Tests/badge.svg)
[![codecov](https://codecov.io/gh/yourusername/async_redis/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/async_redis)
[![Python Versions](https://img.shields.io/pypi/pyversions/async_redis.svg)](https://pypi.org/project/async_redis/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Async Redis is a powerful, asynchronous Redis client library for Python with built-in connection pooling and namespacing support.

## Features

- Asynchronous API using Python's `asyncio`
- Connection pooling for efficient resource management
- Namespace support to prevent key collisions
- Comprehensive logging system
- Type hints for better code quality and IDE support
- Extensive test coverage

## Installation

You can install Async Redis using pip:

```bash
pip install async_redis
```

Or if you prefer to use Poetry:

```bash
poetry add async_redis
```

## Quick Start

Here's a simple example of how to use Async Redis:

```python
import asyncio
from async_redis import AsyncRedisClient, RedisConnectionManager, configure_logging

# Configure logging (optional)
configure_logging(level="DEBUG")

async def main():
    # Create a connection manager
    connection_manager = RedisConnectionManager(host='localhost', port=6379, db=0)
    
    # Create a Redis client with a namespace
    redis_client = await AsyncRedisClient("my_namespace", connection_manager)
    
    # Set a key
    await redis_client.set("my_key", "Hello, Async Redis!")
    
    # Get the value
    value = await redis_client.get("my_key")
    print(value)  # Output: Hello, Async Redis!
    
    # Close the connection
    await redis_client.close()

# Run the async function
asyncio.run(main())
```

## Configuration

You can configure the Redis connection by passing parameters to the `RedisConnectionManager`:

```python
connection_manager = RedisConnectionManager(
    host='localhost',
    port=6379,
    db=0,
    max_connections=10,
    # Add other redis-py connection parameters as needed
)
```

## Logging

Async Redis uses Python's built-in logging module. You can configure logging using the `configure_logging` function:

```python
from async_redis import configure_logging

configure_logging(
    level="DEBUG",
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='async_redis.log'  # Optional: log to a file
)
```

## Advanced Usage

### Pub/Sub

Async Redis supports Redis Pub/Sub functionality:

```python
async def message_handler(message):
    print(f"Received: {message}")

# Subscribe to a channel
await redis_client.subscribe("my_channel", message_handler)

# Publish a message
await redis_client.publish("my_channel", "Hello, subscribers!")
```

### Transactions

You can use Redis transactions with Async Redis:

```python
async with redis_client.pipeline() as pipe:
    pipe.set("key1", "value1")
    pipe.set("key2", "value2")
    await pipe.execute()
```

### Lua Scripting

Async Redis supports Lua scripting:

```python
lua_script = """
redis.call('set', KEYS[1], ARGV[1])
return redis.call('get', KEYS[1])
"""

result = await redis_client.eval(lua_script, 1, "my_key", "my_value")
print(result)  # Output: my_value
```

## Contributing

We welcome contributions to Async Redis! Here are some ways you can contribute:

1. Report bugs or request features by opening an issue.
2. Improve documentation.
3. Submit pull requests with bug fixes or new features.

Please make sure to update tests as appropriate and adhere to the existing coding style.

### Development Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/async_redis.git
   cd async_redis
   ```

2. Install dependencies using Poetry:
   ```
   poetry install
   ```

3. Run tests:
   ```
   poetry run pytest
   ```

4. Check code formatting and type hints:
   ```
   poetry run black async_redis
   poetry run isort async_redis
   poetry run mypy async_redis
   ```

## License

Async Redis is released under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to all contributors who have helped shape Async Redis.
- This project is built on top of the excellent [redis-py](https://github.com/redis/redis-py) library.

---

For more detailed information, please check our [documentation](https://async-redis.readthedocs.io/).

If you encounter any issues or have questions, please [open an issue](https://github.com/yourusername/async_redis/issues) on GitHub.