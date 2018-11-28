"""
Simple async server written on asyncio (python 3.6)
Coursera Final project

It's using my own logger, send

28.11.2018 by 0x000552
"""
import asyncio
from color_logger import ColorLogger


class Server:
    """
    Written for coursera final project.
    Read _client_handler doc str for more info
    """
    _BS_END_OF_RESP = b"\n\n"
    _BS_BEG_ERR = b"error\n"
    _BS_RESP_SUCCESS = b"ok"

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.dict_metrics = dict()
        self.loop = asyncio.get_event_loop()

        self._start_srv()

    def _start_srv(self):
        print(f"Starting server {self.host}: {self.port}")
        cor = asyncio.start_server(self._client_handler,
                                   self.host,
                                   self.port,
                                   loop=self.loop)
        self.srv = self.loop.run_until_complete(cor)


    def stop(self):
        print("Stopping server")
        self.srv.close()
        asyncio.wait(self.srv.wait_closed())



    async def _client_handler(self, reader, writer):
        """
        Expected data:
            get <key>/*\n
            put <key> <value> <timestamp>\n

        In dict we swap <value> and <timestamp>:
        {
            <key>: [
                    (<timestamp>, <value>),
                    ...
                   ],
            ...
        }
        :param reader:
        :param writer:
        :return:
        """
        try:
            while True:
                buff = await reader.readline()
                if not buff:
                    break
                buff = buff.strip().split(b' ')
                print(f"Received: {buff}")
                len_buff = len(buff)

                if len_buff == 2 and buff[0] == b"get":
                    # GET ITEMS

                    # We always should response as success
                    list_resp = [self._BS_RESP_SUCCESS, ]

                    if buff[1] == b"*":
                        for key, list_metrics in self.dict_metrics.items():
                            for tuple_metric in list_metrics:
                                list_resp.append(b"\n%s %s %s" % (key, tuple_metric[0], tuple_metric[1]))
                    else:
                        list_metrics = self.dict_metrics.get(buff[1])
                        for tuple_metric in list_metrics:
                            list_resp.append(b"\n%s %s %s" % (buff[1], tuple_metric[0], tuple_metric[1]))

                    list_resp.append(self._BS_END_OF_RESP)

                    # Protocol said: Not found -> SUCCESS RESPONSE
                    print(f"Sending: {list_resp}")
                    writer.write(b"".join(list_resp))

                elif len_buff == 4 and buff[0] == b"put":
                    # PUT ITEM
                    # Create list in dict if it's not existing
                    if not self.dict_metrics.get(buff[1]):
                        self.dict_metrics[ buff[1] ] = list()

                    # Check if metric already exists (check by timestamp)
                    metric_not_exist = True
                    for list_metrics in self.dict_metrics[ buff[1] ]:
                        for tuple_metric in list_metrics:
                            if tuple_metric[0] == buff[3]:
                                metric_not_exist = False

                    if metric_not_exist:
                        self.dict_metrics[ buff[1] ].append( (buff[3], buff[2]) )
                        print(f"Chaotic: {self.dict_metrics})")
                        self._sort_dict_metrics()
                        print(f"Sorted:  {self.dict_metrics}")
                    writer.write(b"%s%s" % (self._BS_RESP_SUCCESS, self._BS_END_OF_RESP))

                else:
                    writer.write(b"%swrong command%s" % (self._BS_BEG_ERR, self._BS_END_OF_RESP))

                await writer.drain()
        except asyncio.CancelledError:
            pass
        finally:
            print("Closing connection")
            writer.close()

    def _sort_dict_metrics(self):  # sync?
        """
        For each dict element (list of tuples)
            Sort it by timestamp (second element in tuple)
        """

        for k in self.dict_metrics:
            self.dict_metrics[k].sort(key=lambda metric_list: metric_list[0])


def run_server(host, port):
    loop = asyncio.get_event_loop()
    s = Server(host, port)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        for task in asyncio.Task.all_tasks():
            task.cancel()
            loop.run_until_complete(task)

        s.stop()
        loop.close()



if __name__  == "__main__":
    run_server('localhost', 8_888)
