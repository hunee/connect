#include <iostream>
#include <boost/asio.hpp>
#include <boost/smart_ptr.hpp>
#include <boost/bind.hpp>
#include <boost/thread.hpp>
#include <boost/chrono.hpp>
#include <boost/thread/scoped_thread.hpp>
 
class CTest
{
public :
    CTest() : service(), pThread()
    {
        std::cout << __FUNCTION__ << std::endl;
        operation = true;
    }
 
    virtual ~CTest()
    {
        std::cout << __FUNCTION__ << std::endl;
    }
 
    void do_print(int x)
    {
        std::cout << __FUNCTION__ << std::endl;
 
        boost::function<void(int)> printerHandler = [&](int x) {
            for(int i = 1; i <= x; i++)
            {
                if(operation == false)
                {
                    std::cout << "... forcibly finish handler ..." << std::endl;
                    break;
                }
 
                std::cout << __FUNCTION__ << " : called and loop : " << i << std::endl;
                 boost::this_thread::sleep_for(boost::chrono::seconds(1));
            }
        };
 
        service.post(boost::bind(printerHandler, x));
    }
 
    void start(void)
    {
        if(pThread) return;
 
        // io_service를 main thread로부터 분리하기 위해서 별도의 thread 생성
        pThread.reset(new boost::thread(boost::bind(&boost::asio::io_service::run, boost::ref(service))));
    }
 
    void stop(void)
    {
        if(!pThread) return;
 
        operation = false;
        service.stop();
        pThread->join();
 
        // io_service 재시작을 위해서 reset를 건다.
        service.reset();
        pThread.reset();
    }
private :
    boost::asio::io_service service;
    boost::scoped_ptr<boost::thread> pThread;
    bool operation;
};
 
int main(int argc, char* argv[])
{
    CTest test;
    test.do_print(10);
    test.start();
 
    while(1)
    {
        char option;
        std::cout << "... in while loop ..." << std::endl;
        std::cin.get(option);
 
        if(option == 'x')
            break;
    }
 
    test.stop();
 
    std::cout << "... end of main ..." << std::endl;
 
    return 0;
}


