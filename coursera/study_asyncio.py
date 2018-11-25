"""
What? Just a doc string... Without any useful information...
"""
import asyncio

import color_logger
from client_server_asyncio.simple_asyncio_server import SimpleAsyncServer


# main()
async def main():
    srv1 = SimpleAsyncServer(logger=clog)
    await srv1.start()


if __name__ == "__main__":
    clog = color_logger.ColorLogger()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        clog.log_it("KeyboardInterrupt exception caught", 2)
