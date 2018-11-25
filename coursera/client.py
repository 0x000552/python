"""
First of two final projects. (Coursera Diving In Python)
Client Metrics.

21.11.2018 by 0x000552
"""
import socket
import time


class ClientError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Client:

    DBS_CORRECT_BEG_ANSWER = {   # Dict of Binary String (Correct Beginning of Answer)
        'OK':  b"ok\n",
        'ERR': b"error\n"
    }
    BS_END_OF_RESPONSE = b"\n\n"
    NL_BS_EOR = -len(BS_END_OF_RESPONSE)  # Negative Len
    BS_END_OF_LINE = b"\n"

    MAX_ITER_RESP = 100  # Maximum iteration which we can do while waiting for response

    def __init__(self, srv_ip, srv_port, timeout=None):
        self.sock = socket.create_connection((srv_ip, srv_port), timeout)

    def server_shutdown(self):
        self.sock.close()
        print("Socket has been closed")

    def get(self, request):
        #try:
        self.sock.sendall(f"get {request}\n".encode())
        msg = self._rcv_msg_response()
        #except Exception:
        #   self.server_shutdown()

        metric_dict = dict()
        if msg:
            msgs = msg.decode().split('\n')
            for metrics in msgs:
                metric = metrics.split(' ')
                if not metric_dict.get(metric[0]):
                    metric_dict[metric[0]] = list()
                metric_dict[metric[0]].append((int(metric[2]), float(metric[1])))
        return metric_dict


    def put(self, key, value, timestamp=None):
        if not timestamp:
            timestamp = str(int(time.time()))
        self.sock.sendall(f"put {key} {value} {timestamp}\n".encode())

        self._rcv_msg_response()



    def _rcv_msg_response(self):
        """ Receive part of response from socket

        If received successfully (correct, without error flag):
            response str without DBS_CORRECT_BEG_ANSWER and BS_END_OF_RESPONSE
        else:
            raise

        # TODO I think I should rename variables :D
        """
        buff = list()

        # Test if begin of response is correct
        buff.append(self.sock.recv(1024))
        if buff[0]:
            for _, cb_answer in self.DBS_CORRECT_BEG_ANSWER.items():
                lcb_answer = len(cb_answer)
                chk_cb = buff[0].find(cb_answer, None, lcb_answer)  # Check the Correctness of the Beginning
                if chk_cb >= 0:
                    # Check fullness of response
                    for i in range(self.MAX_ITER_RESP):
                        #  if last (len of end of response) symbols == end of response:
                        #      we've been reached End Of Response
                        if buff[i].find(self.BS_END_OF_RESPONSE, self.NL_BS_EOR) >= 0:
                            # join and strip response (remove service info from begin and end)
                            buff = b"".join(buff)[lcb_answer: self.NL_BS_EOR]  # !!! NOW buff is str (not list) !!!

                            # Error handling
                            if cb_answer == self.DBS_CORRECT_BEG_ANSWER['ERR']:
                                raise ClientError(buff)

                            return buff

                        # response is not fullness, get next part
                        buff.append(self.sock.recv(1024))
                        if not buff[i+1]:
                            raise ClientError("Unexpected EOF")  # TODO should I change ClientError, add dict in it?
                    raise ClientError("Incorrect response! Maximum iteration has been reached!")
        raise ClientError(f"Incorrect response: {'None' if buf[0] is None else buf[0]}")  # TODO Should I catch it here?

"""
if __name__ == "__main__":  # DEBUG
    try:
        client = Client("localhost", 10_342)
        client.get("*")
    except KeyboardInterrupt:
        print("KeyboardInterrupt was caught")
        client.server_shutdown()
"""