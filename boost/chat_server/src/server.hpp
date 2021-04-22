server.hpp
#pragma once

#include <vector>
#include <set>
#include <boost/asio.hpp>
#include <boost/function.hpp>
#include <boost/enable_shared_from_this.hpp>
#include <boost/shared_ptr.hpp>
#include <boost/logic/tribool.hpp>
#include <boost/tuple/tuple.hpp>
#include <boost/bind.hpp>
#include <boost/thread.hpp>
using boost::asio::ip::tcp;

class connection_manager;

// 클라이언트의 커넥션         
class connection
        :       public boost::enable_shared_from_this<connection>,
        private boost::noncopyable
{
public:
        // 커넥션 생성자
        explicit connection(boost::asio::io_service& io_service);

        // 소켓 구함
        boost::asio::ip::tcp::socket& socket();

        // 커넥션의 첫번째 async operation을 시작시킨다.
        void start();

        // 모든 async operation를 중지 한다.( 취소 )
        void stop();

private:

        // handle read
        void handle_read(const boost::system::error_code& e,
                std::size_t bytes_transferred);

        // handle write
        void handle_write(const boost::system::error_code& e);

        // strand는 커넥션의 post/dispath 가 동시에 실행되지 않도록 보장한다.
        boost::asio::io_service::strand strand_;

        // 소켓
        boost::asio::ip::tcp::socket socket_;

        // read 에 사용할 버퍼
        boost::array<char, 8192> buffer_;
};

typedef boost::shared_ptr<connection> connection_ptr;

// server 
class server
        : private boost::noncopyable
{
public:
        // address와 port를 가지고 listen socket를 만들고 초기화함
        explicit server(const std::string& address, const std::string& port,
                        std::size_t thread_pool_size);

        // io_service 의 run을 수행함
        void run();

        // stop 시킴
        void stop();

private:
        // accept되었음
        void handle_accept(const boost::system::error_code& e);

        // 스레드 사이즈
        std::size_t thread_pool_size_;

        // io core
        boost::asio::io_service io_service_;

        // acceptor
        boost::asio::ip::tcp::acceptor acceptor_;

        // 다음 acceptor이 수행될 connection
        connection_ptr new_connection_;
};
 
server.cpp
#include "server.hpp"

connection::connection(boost::asio::io_service& io_service)
        : strand_(io_service), socket_(io_service)
{
}

boost::asio::ip::tcp::socket& connection::socket()
{
        return socket_;
}

void connection::start()
{
        socket_.async_read_some(boost::asio::buffer(buffer_),
                strand_.wrap(
                boost::bind(&connection::handle_read, shared_from_this(),
                boost::asio::placeholders::error,
                boost::asio::placeholders::bytes_transferred)));
}

void connection::stop()
{
        socket_.close();
}

void connection::handle_read(const boost::system::error_code& e,
        std::size_t bytes_transferred)
{
        if (!e)
        {
                socket_.async_read_some(boost::asio::buffer(buffer_),
                        strand_.wrap(
                        boost::bind(&connection::handle_read, shared_from_this(),
                        boost::asio::placeholders::error,
                        boost::asio::placeholders::bytes_transferred)));
        }
}

void connection::handle_write(const boost::system::error_code& e)
{
        // 종료 시키기
        if (!e)
        {
                // graceful close
                boost::system::error_code ignored_ec;
                socket_.shutdown(boost::asio::ip::tcp::socket::shutdown_both, ignored_ec);
        }
}


server::server(const std::string& address, const std::string& port,
                           std::size_t thread_pool_size)
                           :    thread_pool_size_(thread_pool_size),
                                   acceptor_(io_service_)

{
        // resolving
        boost::asio::ip::tcp::resolver resolver(io_service_);
        boost::asio::ip::tcp::resolver::query query(address, port);
        boost::asio::ip::tcp::endpoint endpoint = *resolver.resolve(query);

        acceptor_.open(endpoint.protocol());
        // reuse_address 옵션을 설정한다.
        acceptor_.set_option(boost::asio::ip::tcp::acceptor::reuse_address(true));
        acceptor_.bind(endpoint);
        acceptor_.listen();

        new_connection_.reset( new connection( io_service_ ) );
        acceptor_.async_accept(new_connection_->socket(),
                boost::bind(&server::handle_accept, this,
                boost::asio::placeholders::error));
}

void server::run()
{
        // Create a pool of threads to run all of the io_services.
        std::vector<boost::shared_ptr<boost::thread> > threads;
        for (std::size_t i = 0; i < thread_pool_size_; ++i)
        {
                boost::shared_ptr<boost::thread> thread(new boost::thread(
                        boost::bind(&boost::asio::io_service::run, &io_service_)));
                threads.push_back(thread);
        }

        // Wait for all threads in the pool to exit.
        for (std::size_t i = 0; i < threads.size(); ++i)
                threads[i]->join();

}

void server::stop()
{
        io_service_.stop();
}

void server::handle_accept(const boost::system::error_code& e)
{
        if (!e)
        {
                new_connection_->start();
                new_connection_.reset(new connection( io_service_));
                acceptor_.async_accept(new_connection_->socket(),
                        boost::bind(&server::handle_accept, this,
                        boost::asio::placeholders::error));

        }
}


// 콘솔 컨트롤 핸들러가 호출할 함수
boost::function0<void> console_ctrl_function;

// 콘솔의 컨트롤 헨들러
BOOL WINAPI console_ctrl_handler(DWORD ctrl_type)
{
        switch (ctrl_type)
        {
        case CTRL_C_EVENT:
        case CTRL_BREAK_EVENT:
        case CTRL_CLOSE_EVENT:
        case CTRL_SHUTDOWN_EVENT:
                // 콘솔에서 다음 컨트롤 타입 이벤트가 생기면 호출된다.
                console_ctrl_function();
                return TRUE;
        default:
                return FALSE;
        }
}

int main(int argc, char* argv[])
{
        try
        {
                if (argc != 4)
                {
                        std::cerr << "Usage: server <address> <port> <threads>\n";
                        return 1;
                }

                // 서버 초기화
                std::size_t num_threads = boost::lexical_cast<std::size_t>(argv[3]);
                server s(argv[1], argv[2], num_threads);

                console_ctrl_function = boost::bind(&server::stop, &s);

                SetConsoleCtrlHandler(console_ctrl_handler, TRUE);

                // 서버 동작
                s.run();
        }
        catch (std::exception& e)
        {
                std::cerr << "exception: " << e.what() << "\n";
        }

        return 0;
}

