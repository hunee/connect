cmake_minimum_required(VERSION 3.10)

project(chat_client)


#
set(SOURCE_DIR src)
#set(SOURCE_DIR ${PROJECT_SOURCE_DIR}/examples/cpp14/iostreams)


#
#set(SOURCES ${SOURCE_DIR}/chat_server.cpp)
set(SOURCES ${SOURCE_DIR}/chat_client.cpp)
#set(SOURCES ${SOURCE_DIR}/http_client.cpp)

#
add_executable(${PROJECT_NAME} ${SOURCES})



# test-cxx-flags.cmake
#
# `include(cmake/check-compiler-flags.cmake)` from the root CMakeList
#
include(CheckCXXCompilerFlag)

# Test latest C++ Standard and High warning level to prevent mistakes
if(MSVC)
    check_cxx_compiler_flag(/std:c++latest  cxx_latest          )
    check_cxx_compiler_flag(/W4             high_warning_level  )
elseif(${CMAKE_CXX_COMPILER_ID} MATCHES Clang)
    check_cxx_compiler_flag(-std=c++2a      cxx_latest          )
    check_cxx_compiler_flag(-Wall           high_warning_level  )
elseif(${CMAKE_CXX_COMPILER_ID} MATCHES GNU)
    check_cxx_compiler_flag(-std=gnu++2a    cxx_latest          )
    check_cxx_compiler_flag(-Wextra         high_warning_level  )
endif()


# target_compile_options
if(MSVC)
    target_compile_options(${PROJECT_NAME} 
    PUBLIC
        /std:c++latest /W4  # MSVC 가 식별 가능한 옵션을 지정
    )
else() # Clang + GCC
    target_compile_options(${PROJECT_NAME}
    PUBLIC
        -std=c++2a -Wall    # GCC/Clang이 식별 가능한 옵션을 지정
    PRIVATE
        -fPIC 
#        -fno-rtti 
    )
endif()


# target_compile_definitions
if(MSVC)
    # 묵시적으로 #define을 추가합니다 (컴파일 시간에 적용)
    target_compile_definitions(${PROJECT_NAME}
    PRIVATE
        WIN32_LEAN_AND_MEAN
        NOMINMAX    # numeric_limits를 사용할때 방해가 되는
                    # max(), min() Macro를 제거합니다
        _CRT_SECURE_NO_WARNINGS 
                    # Visual Studio로 C++에 입문했다면 한번쯤 만나본 녀석일 겁니다
                    # 오래된 코드를 위한 프로젝트라면 선택의 여지가 없을 수도 있겠죠...
    )
endif()


###############################################################################

## ASIO STANDALONE
#set(ASIO_INCLUDE_DIRS /usr/local/Cellar/asio-1.16.1/include)
set(ASIO_INCLUDE_DIRS /usr/local/Cellar/asio-1.17.0/include)

include_directories(${ASIO_INCLUDE_DIRS})

add_definitions(-DASIO_STANDALONE)

## BOOST
set(BOOST_ROOT /usr/local/Cellar/boost_1_73_0)

#add_definitions( -DBOOST_ALL_NO_LIB )
add_definitions(${Boost_LIB_DIAGNOSTIC_DEFINITIONS})

set(Boost_USE_STATIC_LIBS        ON) # only find static libs
set(Boost_USE_MULTITHREADED      ON)
set(Boost_USE_STATIC_RUNTIME    OFF)

find_package(Boost REQUIRED COMPONENTS)
if(Boost_FOUND)
    include_directories(${Boost_INCLUDE_DIRS})

    add_definitions(-DBOOST_ASIO_STANDALONE)
endif()


