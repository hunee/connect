//
// server.cpp
// ~~~~~~~~~~
//
// Copyright (c) 2003-2020 Christopher M. Kohlhoff (chris at kohlhoff dot com)
//
// Distributed under the Boost Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
//

#include <array>
#include <cstdlib>
#include <iostream>
#include <memory>
#include <type_traits>
#include <utility>
#include <boost/asio.hpp>
#include <boost/thread.hpp>

using boost::asio::ip::tcp;

#define USE_MULTITHREADED 1

// Class to manage the memory to be used for handler-based custom allocation.
// It contains a single block of memory which may be returned for allocation
// requests. If the memory is in use when an allocation request is made, the
// allocator delegates allocation to the global heap.
class handler_memory
{
public:
  handler_memory()
    : in_use_(false)
  {
  }

  handler_memory(const handler_memory&) = delete;
  handler_memory& operator=(const handler_memory&) = delete;

  void* allocate(std::size_t size)
  {
    if (!in_use_ && size < sizeof(storage_))
    {
      in_use_ = true;
      return &storage_;
    }
    else
    {
      return ::operator new(size);
    }
  }

  void deallocate(void* pointer)
  {
    if (pointer == &storage_)
    {
      in_use_ = false;
    }
    else
    {
      ::operator delete(pointer);
    }
  }

private:
  // Storage space used for handler-based custom memory allocation.
  typename std::aligned_storage<1024>::type storage_;

  // Whether the handler-based custom allocation storage has been used.
  bool in_use_;
};

// The allocator to be associated with the handler objects. This allocator only
// needs to satisfy the C++11 minimal allocator requirements.
template <typename T>
class handler_allocator
{
public:
  using value_type = T;

  explicit handler_allocator(handler_memory& mem)
    : memory_(mem)
  {
  }

  template <typename U>
  handler_allocator(const handler_allocator<U>& other) noexcept
    : memory_(other.memory_)
  {
  }

  bool operator==(const handler_allocator& other) const noexcept
  {
    return &memory_ == &other.memory_;
  }

  bool operator!=(const handler_allocator& other) const noexcept
  {
    return &memory_ != &other.memory_;
  }

  T* allocate(std::size_t n) const
  {
    return static_cast<T*>(memory_.allocate(sizeof(T) * n));
  }

  void deallocate(T* p, std::size_t /*n*/) const
  {
    return memory_.deallocate(p);
  }

private:
  template <typename> friend class handler_allocator;

  // The underlying memory.
  handler_memory& memory_;
};

// Wrapper class template for handler objects to allow handler memory
// allocation to be customised. The allocator_type type and get_allocator()
// member function are used by the asynchronous operations to obtain the
// allocator. Calls to operator() are forwarded to the encapsulated handler.
template <typename Handler>
class custom_alloc_handler
{
public:
  using allocator_type = handler_allocator<Handler>;

  custom_alloc_handler(handler_memory& m, Handler h)
    : memory_(m),
      handler_(h)
  {
  }

  allocator_type get_allocator() const noexcept
  {
    return allocator_type(memory_);
  }

  template <typename ...Args>
  void operator()(Args&&... args)
  {
    handler_(std::forward<Args>(args)...);
  }

private:
  handler_memory& memory_;
  Handler handler_;
};

// Helper function to wrap a handler object to add custom allocation.
template <typename Handler>
inline custom_alloc_handler<Handler> make_custom_alloc_handler(
    handler_memory& m, Handler h)
{
  return custom_alloc_handler<Handler>(m, h);
}

class session
  : public std::enable_shared_from_this<session>
{
public:
  session(tcp::socket socket,
            boost::asio::strand<boost::asio::io_context::executor_type>& strand)
    : socket_(std::move(socket)),
      strand_(strand)
  {
    std::cout << __PRETTY_FUNCTION__ << std::endl;

  }

  void start()
  {
    std::cout << __PRETTY_FUNCTION__ << std::endl;
    std::cout << "socket_.native_handle(): " << socket_.native_handle() << std::endl;

    do_read();
  }

private:
  void do_read()
  {
    std::cout << __PRETTY_FUNCTION__ << std::endl;

    auto self(shared_from_this());
    socket_.async_read_some(boost::asio::buffer(data_),
        make_custom_alloc_handler(handler_memory_,
        boost::asio::bind_executor(strand_,
          [this, self](boost::system::error_code ec, std::size_t length)
          {
            std::cout << __PRETTY_FUNCTION__ << std::endl;

            std::cout <<data_.data() << std::endl;

            if (!ec)
            {
              do_write(length);
            }
          })));
  }

  void do_write(std::size_t length)
  {
    std::cout << __PRETTY_FUNCTION__ << std::endl;

    auto self(shared_from_this());
    boost::asio::async_write(socket_, boost::asio::buffer(data_, length),
        make_custom_alloc_handler(handler_memory_,
        boost::asio::bind_executor(strand_,
          [this, self](boost::system::error_code ec, std::size_t /*length*/)
          {
            std::cout << __PRETTY_FUNCTION__ << std::endl;

            std::cout <<data_.data() << std::endl;

            if (!ec)
            {
              do_read();
            }
          })));
  }

  // The socket used to communicate with the client.
  tcp::socket socket_;
  boost::asio::strand<boost::asio::io_context::executor_type>& strand_;

  // Buffer used to store data received from the client.
  std::array<char, 1024> data_;

  // The memory to use for handler-based custom memory allocation.
  handler_memory handler_memory_;
};


class server
{
public:
  server(short port)
    : io_context_(),
      signals_(io_context_),
      strand_(boost::asio::make_strand(io_context_)),
      acceptor_(io_context_)//, tcp::endpoint(tcp::v4(), port))
  {
    std::cout << __PRETTY_FUNCTION__ << std::endl;

#if 1
  // Register to handle the signals that indicate when the server should exit.
  // It is safe to register for the same signal multiple times in a program,
  // provided all registration for the specified signal is made through Asio.
  signals_.add(SIGINT);
  signals_.add(SIGTERM);
#if defined(SIGQUIT)
  signals_.add(SIGQUIT);
#endif // defined(SIGQUIT)
#endif

  do_await_stop();

  // Open the acceptor with the option to reuse the address (i.e. SO_REUSEADDR).
  boost::asio::ip::tcp::resolver resolver(io_context_);
  boost::asio::ip::tcp::endpoint endpoint = tcp::endpoint(tcp::v4(), port);
  acceptor_.open(endpoint.protocol());
  acceptor_.set_option(boost::asio::ip::tcp::acceptor::reuse_address(true));
  acceptor_.bind(endpoint);
  acceptor_.listen();

#if 0
  //boost::asio::ip::tcp::resolver resolver(io_service);
	boost::asio::ip::tcp::resolver::query query(boost::asio::ip::host_name(),"");
	boost::asio::ip::tcp::resolver::iterator it=resolver.resolve(query);
 
  while(it!=boost::asio::ip::tcp::resolver::iterator())
	{
		boost::asio::ip::address addr=(it++)->endpoint().address();
		if(addr.is_v6())
		{
			std::cout<<"ipv6 address: ";
		}
		else
    {
			std::cout<<"ipv4 address: ";
    }

		std::cout << addr.to_string() << std::endl;
	}
#endif

    do_accept();
  }

  void run()
  {
    std::cout << __PRETTY_FUNCTION__ << std::endl;

  // The io_context::run() call will block until all asynchronous operations
  // have finished. While the server is running, there is always at least one
  // asynchronous operation outstanding: the asynchronous accept call waiting
  // for new incoming connections.
  
#if USE_MULTITHREADED
    for(int i = 0; i < 2; i++)
    {
      io_threads_.create_thread(
        boost::bind(&boost::asio::io_context::run, &io_context_));
    }
    //io_threads_.join_all();
#else
#endif //USE_MULTITHREADED

    io_context_.run();    
  }
  
  void stop()
  {
    std::cout << __PRETTY_FUNCTION__ << std::endl;

    io_context_.stop();
  }

private:
  void do_accept()
  {
    std::cout << __PRETTY_FUNCTION__ << std::endl;
    std::cout << "[" << std::this_thread::get_id() << "] Thread starts" << std::endl;

    acceptor_.async_accept(
      boost::asio::bind_executor(strand_,
        [this](boost::system::error_code ec, tcp::socket socket)
        {
          std::cout << __PRETTY_FUNCTION__ << std::endl;

          // Check whether the server was stopped by a signal before this
          // completion handler had a chance to run.
          if (!acceptor_.is_open())
          {
            return;
          }

          if (!ec)
          {
            std::make_shared<session>(std::move(socket), strand_)->start();
          }

          do_accept();
        }));
  }

void do_await_stop()
{
  signals_.async_wait(
    boost::asio::bind_executor(strand_,
      [this](boost::system::error_code /*ec*/, int /*signo*/)
      {
        std::cout << __PRETTY_FUNCTION__ << std::endl;

        // The server is stopped by cancelling all outstanding asynchronous
        // operations. Once all operations have finished the io_context::run()
        // call will exit.
        acceptor_.close();
        ///session_manager_.stop_all();

        stop();
      }));
}

  boost::asio::io_context io_context_;

  /// The signal_set is used to register for process termination notifications.
  boost::asio::signal_set signals_;

  boost::asio::strand<boost::asio::io_context::executor_type> strand_;

#if USE_MULTITHREADED    
  boost::thread_group io_threads_;
#endif

  tcp::acceptor acceptor_;
};

int main(int argc, char* argv[])
{
  try
  {
    /*if (argc != 2)
    {
      std::cerr << "Usage: server <port>\n";
      return 1;
    }*/

    server s(8080);
    s.run();
  }
  catch (std::exception& e)
  {
    std::cerr << "Exception: " << e.what() << std::endl;
  }


  return 0;
}
