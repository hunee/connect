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
    void do_print(int x)
    {
        boost::function<void(int)> printerHandler = [](int x) {
            for(int i = 1; i <= x; i++)
            {
                std::cout << __FUNCTION__ << " : called and loop : " << i << std::endl;
                 boost::this_thread::sleep_for(boost::chrono::seconds(1));
            }
        };
 
        service.post(boost::bind(printerHandler, x));
    }
 
    void start(void)
    {
        service.run();
        //service.poll();
    }
 
    void stop(void)
    {
        service.stop();
    }
private :
    boost::asio::io_service service;
    //boost::scoped_ptr<boost::thread> pThredd;
};
 
int main(int argc, char* argv[])
{
    CTest test;
    test.do_print(10);
    test.start();
 
    std::cin.get();
    test.stop();
 
    std::cout << "... end of main ..." << std::endl;
 
    return 0;
}