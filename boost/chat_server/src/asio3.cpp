#include <iostream>
#include <boost/asio.hpp>
#include <boost/smart_ptr.hpp>
#include <boost/bind.hpp>
#include <boost/thread.hpp>
#include <boost/chrono.hpp>
#include <boost/thread/scoped_thread.hpp>
#include <boost/lexical_cast.hpp>
 
class CTest
{
public :
    CTest() : service()
    {
        std::cout << __FUNCTION__ << std::endl;
    }
 
    virtual ~CTest()
    {
        std::cout << __FUNCTION__ << std::endl;
    }
 
    void do_print(int x)
    {
        std::string curTrId = boost::lexical_cast<std::string>(boost::this_thread::get_id());
 
        for(int i = 0; i < x; i++)
        {
            std::printf("[ %d -> current Thread Id : %s] \n", i, curTrId.c_str());
            boost::this_thread::sleep_for(boost::chrono::milliseconds(100));
        }
    }
 
    void start(void)
    {
        std::cout << __FUNCTION__ << ", " << __LINE__ << std::endl;
 
        for(int i = 0; i < 2; i++)
        {
            service.post(boost::bind(&CTest::do_print, this, 100));
        }
 
        for(int i = 0; i < 2; i++)
        {
            io_threads.create_thread(boost::bind(&boost::asio::io_service::run, &service));
        }
    }
 
    void stop(void)
    {
        service.stop();
        io_threads.join_all();
        service.reset();
    }
private :
    boost::asio::io_service service;
    boost::thread_group io_threads;
};
 
int main(int argc, char* argv[])
{
    CTest test;
 
    test.start();
 
    while(1)
    {
        char option;
        std::cout << "... in while loop ..." << std::endl;
        std::cin.get(option);
 
        if(option == 'x')
        {
            break;
        }
    }
 
    test.stop();
 
    std::cout << "... end of main ..." << std::endl;
    return 0;
}


