"""
Simple async server written on asyncio

It's using my own logger, send

21.11.2018 by 0x000552
"""
import asyncio
from color_logger import ColorLogger


class SimpleAsyncServer:
    _srv_id = 0
    _client_log_ident = 0
    _CLIENT_TIMEOUT = 15

    def __init__(self, srv_ip="0.0.0.0", srv_port=10_342, logger=None):
        self.srv_ip = srv_ip
        self.srv_port = srv_port

        self.srv_id = self._srv_id
        self._srv_id += 1

        if not logger:
            logger = ColorLogger()
        self.logger = logger
        # set logging func
        self.log_it = logger.log_it

    async def _server_start(self):
        try:
            self.log_it(f"Server '{self.srv_id}' start ({self.srv_ip} : {self.srv_port:,})", 0)
            # Coursera Client Handler!
            srv = await asyncio.start_server(self._coursera_client_handler, self.srv_ip, self.srv_port)
            async with srv:
                await srv.serve_forever()
                self.log_it("main() exit", 4)  # DEBUG

        finally:
            self.log_it(f"Server '{self.srv_id}' shutdown ({self.srv_ip} : {self.srv_port:,})", 1)
            self._srv_id -= 1

    def start(self):
        return asyncio.create_task(self._server_start())

    async def _coursera_client_handler(self, reader, writer):
        iclient_color = self.logger.inext_regular_color
        self._client_log_ident += 2
        client_log_ident = self._client_log_ident

        response_dict = {
            'palm.cpu': [
                (0.5, 1150864247),
                (0.5, 1150864248)
            ],
            'eardrum.cpu': [
                (3.0, 1150864250),
                (4.0, 1150864251)
            ],
            'eardrum.memory': [
                (4200000.0, 1503320872)
            ]
        }

        try:
            client_addr = writer.get_extra_info("peername")
            client_addr = f"({client_addr[0]}: {client_addr[1]:,})"

            self.log_it(f"!!! New client: {client_addr}", iclient_color, client_log_ident)
            while True:
                data = await asyncio.wait_for(reader.readline(), timeout=self._CLIENT_TIMEOUT)

                if not data:
                    self.log_it(f"!!! Connection closed by client {client_addr}", iclient_color, client_log_ident)
                    break

                self.log_it(f"Get message {client_addr}: {data!r}", iclient_color, client_log_ident)
                if data == b"exit\n":
                    return
                if data == b"get *\n":
                    resp_list = list("ok", )
                    for k_resp, v_resp in response_dict.items():
                        for metrics in v_resp:
                            resp_list.append(f"\n{k_resp}")
                            for metric in metrics:
                                resp_list.append(f" {metric}")
                    resp_list.append("\n\n")
                    resp = "".join(resp_list)
                    self.log_it(f"!! Send to {client_addr}: {resp}", iclient_color, client_log_ident)
                    writer.write(resp.encode())
                    # writer.write(b"error\nlol\n\n")
                    await writer.drain()
        except asyncio.TimeoutError:
            self.log_it(f"!!! TimeOut {client_addr}", iclient_color, client_log_ident)
        finally:
            self.log_it(f"!!! Closing stream {client_addr}", iclient_color, client_log_ident)
            writer.close()
            await writer.wait_closed()


# main()
async def main():
    srv1 = SimpleAsyncServer(logger=clog)
    await srv1.start()


if __name__ == "__main__":
    clog = ColorLogger()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        clog.log_it("KeyboardInterrupt exception caught", 2)
