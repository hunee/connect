
import sys
import asyncio
import asyncio.streams

HOST = '127.0.0.1'
PORT = 8080

class TCPServer:
    """
    This is just an example of how a TCP server might be potentially
    structured.  This class has basically 3 methods: start the server,
    handle a client, and stop the server.

    Note that you don't have to follow this structure, it is really
    just an example or possible starting point.
    """

    def __init__(self):
        self.socket = None  # encapsulates the server sockets

        # this keeps track of all the clients that connected to our
        # server.  It can be useful in some cases, for instance to
        # kill client connections or to broadcast some data to all
        # clients...
        self.conns = {} # task -> (reader, writer)

    def _accept_handler(self, reader, writer):
        """
        This method accepts a new client connection and creates a Task
        to handle this client.  self.clients is updated to keep track
        of the new client.
        """

        # start a new Task to handle this specific client connection
        task = asyncio.Task(self._request_handler(reader, writer))
        self.conns[task] = (reader, writer)

        def conn_done(task):
            print('connect task done: ', task, file=sys.stderr)
            del self.conns[task]

        task.add_done_callback(conn_done)

    @asyncio.coroutine
    def _request_handler(self, reader, writer):
        """
        This method actually does the work to handle the requests for
        a specific client.  The protocol is line oriented, so there is
        a main loop that reads a line with a request and then sends
        out one or more lines back to the client with the result.
        """
        while True:
            data = (yield from reader.readline()).decode("utf-8")
            if not data:    # an empty string means the client disconnected
                break

            cmd, *args = data.rstrip().split(' ')
            if cmd == 'add':
                arg1 = float(args[0])
                arg2 = float(args[1])
                retval = arg1 + arg2
                writer.write("{!r}\n".format(retval).encode("utf-8"))
            elif cmd == 'repeat':
                times = int(args[0])
                msg = args[1]
                writer.write("begin\n".encode("utf-8"))
                for idx in range(times):
                    writer.write("{}. {}\n".format(idx+1, msg)
                                        .encode("utf-8"))
                writer.write("end\n".encode("utf-8"))
            else:
                print("Bad command {!r}".format(data), file=sys.stderr)

            # This enables us to have flow control in our connection.
            yield from writer.drain()

    def start_server(self, loop):
        """
        Starts the TCP server, so that it listens on port 12345.

        For each client that connects, the accept_client method gets
        called.  This method runs the loop until the server sockets
        are ready to accept connections.
        """
        self.socket = loop.run_until_complete(
            asyncio.streams.start_server(self._accept_handler,
                                         HOST,
                                         PORT,
                                         loop=loop))

    def close(self, loop):
        """
        Stops the TCP server, i.e. closes the listening socket(s).

        This method runs the loop until the server sockets are closed.
        """
        if self.socket is not None:
            self.socket.close()
            loop.run_until_complete(self.socket.wait_closed())
            self.socket = None


def main():
    loop = asyncio.get_event_loop()

    # creates a server and starts listening to TCP connections
    server = TCPServer()
    server.start_server(loop)

    @asyncio.coroutine
    def init():
        reader, writer = yield from asyncio.streams.open_connection(HOST,
                                                                    PORT,
                                                                    loop=loop)

        def send(msg):
            print('> ' + msg)
            writer.write((msg + '\n').encode('utf-8'))

        def recv():
            msgback = (yield from reader.readline()).decode("utf-8").rstrip()
            print('< ' + msgback)
            return msgback

        # send a line
        send('add 1 2')
        msg = yield from recv()

        send('repeat 5 hello')
        msg = yield from recv()
        assert msg == 'begin'
        while True:
            msg = yield from recv()

            if msg == 'end':
                break

        writer.close()
        yield from asyncio.sleep(0.5)

    # creates a client and connects to our server
    try:
        loop.run_until_complete(init())
        server.close(loop)

    finally:
        loop.close()

if __name__ == '__main__':
    main()

