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
    //CTest() : service(), strand(service)
    CTest() : service(), strand(service), work(service)
    {
        std::cout << __FUNCTION__ << std::endl;
    }
 
    virtual ~CTest()
    {
        std::cout << __FUNCTION__ << std::endl;
    }
 
    void do_print(int x)
    {
        boost::function<void(int)> handler = [&](int x) {
            std::string curTrId = boost::lexical_cast<std::string>(boost::this_thread::get_id());
 
            for(int i = 0; i < x; i++)
            {
                std::printf("[ %d -> current Thread Id : %s] \n", i, curTrId.c_str());
                boost::this_thread::sleep_for(boost::chrono::milliseconds(100));
            }
        };
 
        service.post(strand.wrap(boost::bind(handler, x)));
    }
 
    void start(void)
    {
        std::cout << __FUNCTION__ << ", " << __LINE__ << std::endl;
 
        for(int i = 0; i < 2; i++)
        {
            print_threads.create_thread(boost::bind(&CTest::do_print, this, 100));
        }
 
        for(int i = 0; i < 2; i++)
        {
            io_threads.create_thread(boost::bind(&boost::asio::io_service::run, &service));
        }
    }
 
    void stop(void)
    {
        service.stop();
        print_threads.join_all();
        io_threads.join_all();
        service.reset();
    }
private :
    boost::asio::io_service service;
    boost::asio::io_service::work work;
    boost::asio::io_service::strand strand;
    boost::thread_group io_threads;
    boost::thread_group print_threads;
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


