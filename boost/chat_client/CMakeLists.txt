cmake_minimum_required(VERSION 3.0.0)
project(chat_server VERSION 0.1.0)

#
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


#
# CMAKE_CXX_FLAGS
#
#[[
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(CMAKE_CXX_STANDARD 11) 
set(CMAKE_CXX_FLAGS "-O1 -Wall") 
set(CMAKE_CXX_FLAGS_DEBUG "-O0 -g") 
set(CMAKE_CXX_FLAGS_RELEASE "-O2") 
set(CMAKE_CXX_FLAGS_MINSIZEREL "-Os") 
set(CMAKE_CXX_FLAGS_RELWITHDEBINFO "-Og -g") 
]]


#
# CMAKE_BUILD_TYPE
#
# set(CMAKE_BUILD_TYPE Debug)
#[[
message(STATUS "CMAKE_BUILD_TYPE: ${CMAKE_BUILD_TYPE}")

if (CMAKE_BUILD_TYPE MATCHES "Debug")
    set(CMAKE_CXX_FLAGS "-O2 -std=c++2a -Wall -framework Cocoa -DDEBUG")
else()
    set(CMAKE_CXX_FLAGS "-O2 -std=c++2a -Wall -framework Cocoa")
endif()

message(STATUS "CMAKE_CXX_FLAGS: ${CMAKE_CXX_FLAGS}")
]]

#
# include_directories
#
include_directories(include)
include_directories(/usr/local/include)

#
# add_executable
#
set(SOURCE_DIR src)
set(INCLUDE_DIR include)


set(SOURCES #${SOURCE_DIR}/chat_server.cpp
#                ${SOURCE_DIR}/test_basic.c
${SOURCE_DIR}/chat_client.cpp
)

#set(SOURCES src/http-server.cpp)

add_executable(${PROJECT_NAME} ${SOURCES})



#
# target_compile_options
#
if(MSVC)
    target_compile_options(${PROJECT_NAME} 
    PUBLIC
        /std:c++latest 
        /W4
    )
else() # Clang + GCC
    target_compile_options(${PROJECT_NAME}
    PUBLIC
        -std=c++2a
        -Wall
        -Wimplicit-function-declaration
        -Wint-conversion          
    PRIVATE
        -fPIC 
#        -fno-rtti 
        -fvisibility=hidden
        #-fvisibility=default
    )
endif()



#
# target_compile_definitions
#
if(MSVC)
    target_compile_definitions(${PROJECT_NAME}
    PRIVATE
        WIN32_LEAN_AND_MEAN
        NOMINMAX
        _CRT_SECURE_NO_WARNINGS 
    )
endif()


#
# ASIO STANDALONE
#
find_path(Asio_INCLUDE_DIRS asio)
if(Asio_INCLUDE_DIRS)
    set(Asio_FOUND TRUE)
endif()

message(STATUS "Asio_FOUND: ${Asio_FOUND}")
if(Asio_FOUND)
    message(STATUS "Asio_INCLUDE_DIRS: ${Asio_INCLUDE_DIRS}")

    include_directories(${Asio_INCLUDE_DIRS})

    add_definitions(-DASIO_STANDALONE)
endif()

#
# BOOST
#
#set(BOOST_ROOT /usr/local/Cellar/boost_1_73_0)

set(Boost_USE_STATIC_LIBS        ON)  # only find static libs
set(Boost_USE_DEBUG_LIBS         OFF) # ignore debug libs and 
set(Boost_USE_RELEASE_LIBS       ON)  # only find release libs 
set(Boost_USE_MULTITHREADED      ON)
set(Boost_USE_STATIC_RUNTIME    OFF) 

find_package(Boost REQUIRED COMPONENTS atomic chrono regex date_time system filesystem thread graph program_options)
message(STATUS "Boost_FOUND: ${Boost_FOUND}")

if(Boost_FOUND)
    message(STATUS "Boost_VERSION: ${Boost_VERSION}")
    message(STATUS "Boost_LIB_VERSION: ${Boost_LIB_VERSION}")
    message(STATUS "Boost_MAJOR_VERSION: ${Boost_MAJOR_VERSION}")
    message(STATUS "Boost_MINOR_VERSION: ${Boost_MINOR_VERSION}")

    message(STATUS "Boost_INCLUDE_DIRS: ${Boost_INCLUDE_DIRS}")
    message(STATUS "Boost_LIBRARY_DIRS: ${Boost_LIBRARY_DIRS}")
    message(STATUS "Boost_LIBRARIES: ${Boost_LIBRARIES}")

    include_directories(${Boost_INCLUDE_DIRS})
    link_directories(${Boost_LIBRARY_DIRS})

    add_definitions(${Boost_DEFINITIONS})
    #add_definitions( -DBOOST_ALL_NO_LIB )
    add_definitions(${Boost_LIB_DIAGNOSTIC_DEFINITIONS})

    add_definitions(-DBoost_ASIO_STANDALONE)
    add_definitions(-DBOOST_ASIO_NO_DEPRECATED)

    target_link_libraries(${PROJECT_NAME} ${Boost_LIBRARIES} pthread) 

endif()


#
# PYTHON
#
find_package(Python COMPONENTS Interpreter Development)
message(STATUS "Python_FOUND: ${Python_FOUND}")

if (Python_FOUND)
    message(STATUS "Python_VERSION: ${Python_VERSION}")
    message(STATUS "Python_VERSION_MAJOR: ${Python_VERSION_MAJOR}")
    message(STATUS "Python_VERSION_MINOR: ${Python_VERSION_MINOR}")
    message(STATUS "Python_VERSION_PATCH: ${Python_VERSION_PATCH}")

    message(STATUS "Python_INCLUDE_DIRS: ${Python_INCLUDE_DIRS}")
    message(STATUS "Python_LIBRARIES: ${Python_LIBRARIES}")
    message(STATUS "Python_LIBRARY_DIRS: ${Python_LIBRARY_DIRS}")
    message(STATUS "Python_RUNTIME_LIBRARY_DIRS: ${Python_RUNTIME_LIBRARY_DIRS}")

    include_directories(${Python_INCLUDE_DIRS})
    link_directories(${Python_RUNTIME_LIBRARY_DIRS})

    target_link_libraries(${PROJECT_NAME} ${Python_LIBRARIES})
endif()



#
# COPY
#
#[[
message(${CMAKE_CURRENT_SOURCE_DIR})

file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/Resources/ 
     DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/build/Resources/
)
]]

