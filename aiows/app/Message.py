from pprint import pprint

"""
C++

Message.h

#include <iostream>

struct Header {
    int id;
};

template <typename T>
struct Message {
    Header header;
    T body;

    Message() {
        body.req();
    }
};

struct reqBody {
    int id;

    reqBody() {
        this->id = 100;
    }

    void req()
    {
        std::cout << this->id << std::endl;
    }
};

int main(int argc, const char * argv[]) {

    auto req = Message<reqBody>();
    req.header.id = 1;

    std::cout << req.body.id;

    return 0;
}

"""


class Header:
    def __init__(self):
        self.id = 'header.id'

class reqBody:
    def __init__(self):
        self.id = 'body.id'
        self.data = ''

class Message:
    def __init__(self, T):
        self.header = Header()
        self.body = T()

        r = type(T)
        print(r)


req = Message(reqBody)
print(req.header.id)
print(req.body.id)



