cmake_minimum_required(VERSION 3.11)
project(server VERSION 0.1.0)

#
message(STATUS "CMAKE_CURRENT_SOURCE_DIR: ${CMAKE_CURRENT_SOURCE_DIR}")

#
# include_directories
#

#
include_directories(/usr/local/include)

#
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/deps)

#
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/src)

#
# deps src
#
set(DEPS_SRC_DIRS ${CMAKE_CURRENT_SOURCE_DIR}/deps)

#set(DEPS_SRCS
#${DEPS_SRC_DIRS}/tinyxml2/tinyxml2.cpp
#)

#
# src
#
set(SRC_DIR src)

set(SRCS

#osver
${SRC_DIR}/server.cpp


)


# Icon
if (WIN32)
    set(ICON glfw.rc)
elseif (APPLE)
    set(ICON glfw.icns)
endif()


#
# add_executable
#
#add_executable(boing WIN32 MACOSX_BUNDLE boing.c ${ICON} ${GLAD_GL})
add_executable(${PROJECT_NAME}
    WIN32 MACOSX_BUNDLE
    ${DEPS_SRCS}
    ${SRCS}
    ${ICON}
)



#
# CMAKE_CXX_STANDARD
#[[
set(CMAKE_CXX_STANDARD 20 CACHE STRING "C++ standard version to use (default is 11)")

message(STATUS "Require C++${CMAKE_CXX_STANDARD}")
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
]]

#
# CMAKE_BUILD_TYPE
#
message(STATUS "CMAKE_BUILD_TYPE: ${CMAKE_BUILD_TYPE}")
message(STATUS "CMAKE_CXX_COMPILER_ID: ${CMAKE_CXX_COMPILER_ID}")

#
# CMAKE_CXX_FLAGS
#
if(MSVC)
    #message(STATUS "MSVC")

elseif(${CMAKE_CXX_COMPILER_ID} MATCHES AppleClang)
    #message(STATUS "AppleClang")
    
    set(CMAKE_CXX_FLAGS "-std=c++2a -frtti -fvisibility-inlines-hidden -fvisibility=hidden")
    set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS} -O0 -g -DDEBUG") 
    set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS} -O2") 
    set(CMAKE_CXX_FLAGS_MINSIZEREL "${CMAKE_CXX_FLAGS} -Os") 
    set(CMAKE_CXX_FLAGS_RELWITHDEBINFO "${CMAKE_CXX_FLAGS} -Og -g") 

elseif(${CMAKE_CXX_COMPILER_ID} MATCHES GNU)
    #message(STATUS "GNU")
    #set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=gnu++2a")

else()
message(STATUS "OTHER")    

endif()

message(STATUS "CMAKE_CXX_FLAGS: ${CMAKE_CXX_FLAGS}")

#
# target_link_libraries
#
target_link_libraries(${PROJECT_NAME} stdc++) 


# MacOS
if (APPLE)
    target_link_libraries(${PROJECT_NAME} objc) 
    target_link_libraries(${PROJECT_NAME} "-framework Foundation" "-framework Cocoa" "-framework IOKit" "-framework OpenGL") 
endif()

#target_link_libraries(program "-framework your_frame_work_name")
#set_target_properties(program PROPERTIES LINK_FLAGS "-Wl,-F/Library/Frameworks")


#
# deps
#
set(DEPS_DIRS ${CMAKE_CURRENT_SOURCE_DIR}/deps)



#
# jsoncpp
#
# mkdir jsoncpp-build; cd jsoncpp-build; cmake ../
# make
# make install

set(JSONCPP_NAME jsoncpp)
find_path(
    JSONCPP_DIRS 
    NAMES ${JSONCPP_NAME}
    HINTS ${DEPS_DIRS}
    NO_DEFAULT_PATH
)

if (JSONCPP_DIRS)
    set(JSONCPP_DIRS ${JSONCPP_DIRS}/${JSONCPP_NAME})
    
    set(JSONCPP_INCLUDE_DIRS ${JSONCPP_DIRS}/include)
    set(JSONCPP_LIBRARY_DIRS ${JSONCPP_DIRS}/jsoncpp-build/lib)

    message(STATUS "JSONCPP_DIRS: ${JSONCPP_DIRS}")

    message(STATUS "JSONCPP_INCLUDE_DIRS: ${JSONCPP_INCLUDE_DIRS}")
    message(STATUS "JSONCPP_LIBRARY_DIRS: ${JSONCPP_LIBRARY_DIRS}")    

    find_library(
        JSONCPP_LIBRARIES
        NAMES libjsoncpp_static.a
        HINTS ${JSONCPP_LIBRARY_DIRS}
        REQUIRED
        NO_DEFAULT_PATH
    )

    if(JSONCPP_LIBRARIES)
        message(STATUS "JSONCPP_LIBRARIES: ${JSONCPP_LIBRARIES}")        

        include_directories(${JSONCPP_INCLUDE_DIRS})

        link_directories(${JSONCPP_LIBRARY_DIRS})
        target_link_libraries(${PROJECT_NAME} ${JSONCPP_LIBRARIES})    
    endif() #JSONCPP_LIBRARIES
endif() #JSONCPP_DIRS




#
# zlib
#
# mkdir build; cd build; cmake ../
# make
# make install

set(ZLIB_NAME zlib-1.2.11)
find_path(
    ZLIB_DIRS 
    NAMES ${ZLIB_NAME}
    HINTS ${DEPS_DIRS}
    NO_DEFAULT_PATH
)

if (ZLIB_DIRS)
    set(ZLIB_DIRS ${ZLIB_DIRS}/${ZLIB_NAME})
    
    set(ZLIB_INCLUDE_DIRS ${ZLIB_DIRS})
    set(ZLIB_LIBRARY_DIRS ${ZLIB_DIRS}/build)

    message(STATUS "ZLIB_DIRS: ${ZLIB_DIRS}")

    message(STATUS "ZLIB_INCLUDE_DIRS: ${ZLIB_INCLUDE_DIRS}")
    message(STATUS "ZLIB_LIBRARY_DIRS: ${ZLIB_LIBRARY_DIRS}")    

    find_library(
        ZLIB_LIBRARIES
        NAMES libz.a
        HINTS ${ZLIB_LIBRARY_DIRS}
        REQUIRED
        NO_DEFAULT_PATH
    )

    if(ZLIB_LIBRARIES)
        message(STATUS "ZLIB_LIBRARIES: ${ZLIB_LIBRARIES}")        

        include_directories(${ZLIB_INCLUDE_DIRS})

        link_directories(${ZLIB_LIBRARY_DIRS})
        target_link_libraries(${PROJECT_NAME} ${ZLIB_LIBRARIES})    
    endif() #ZLIB_LIBRARIES
endif() #ZLIB_DIRS


#
# LUA
#
# cmake . 
# make

set(LUA_NAME lua-5.4.1)
find_path(
    LUA_DIRS 
    NAMES ${LUA_NAME}
    HINTS ${DEPS_DIRS}
    NO_DEFAULT_PATH
)

if (LUA_DIRS)
    set(LUA_DIRS ${LUA_DIRS}/${LUA_NAME})
    
    set(LUA_INCLUDE_DIRS ${LUA_DIRS}/src)
    set(LUA_LIBRARY_DIRS ${LUA_DIRS}/src)

    message(STATUS "LUA_DIRS: ${LUA_DIRS}")

    message(STATUS "LUA_INCLUDE_DIRS: ${LUA_INCLUDE_DIRS}")
    message(STATUS "LUA_LIBRARY_DIRS: ${LUA_LIBRARY_DIRS}")    

    find_library(
        LUA_LIBRARIES
        NAMES liblua.a
        HINTS ${LUA_LIBRARY_DIRS}
        REQUIRED
        NO_DEFAULT_PATH
    )

    if(LUA_LIBRARIES)
        message(STATUS "LUA_LIBRARIES: ${LUA_LIBRARIES}")        

        include_directories(${LUA_INCLUDE_DIRS})

        link_directories(${LUA_LIBRARY_DIRS})
        target_link_libraries(${PROJECT_NAME} ${LUA_LIBRARIES})    
    endif() #LUA_LIBRARIES
endif() #LUA_DIRS


#
# PYTHON
#
find_package(Python REQUIRED COMPONENTS Interpreter Development)
if (Python_FOUND)
    message(STATUS "Python_VERSION: ${Python_VERSION}")

    message(STATUS "Python_INCLUDE_DIRS: ${Python_INCLUDE_DIRS}")
    message(STATUS "Python_LIBRARY_DIRS: ${Python_LIBRARY_DIRS}")
    #message(STATUS "Python_RUNTIME_LIBRARY_DIRS: ${Python_RUNTIME_LIBRARY_DIRS}")
    message(STATUS "Python_LIBRARIES: ${Python_LIBRARIES}")

    include_directories(${Python_INCLUDE_DIRS})
    link_directories(${Python_LIBRARY_DIRS})

    target_link_libraries(${PROJECT_NAME} ${Python_LIBRARIES})
endif()



#
# /usr/local/
#

#
# ASIO STANDALONE
#
find_path(Asio_INCLUDE_DIRS
    asio
)

if(Asio_INCLUDE_DIRS)
    message(STATUS "Asio_INCLUDE_DIRS: ${Asio_INCLUDE_DIRS}")

    include_directories(${Asio_INCLUDE_DIRS})

    add_definitions(-DASIO_STANDALONE)
endif()


#
# BOOST
#
#set(BOOST_ROOT /usr/local/Cellar/boost_1_73_0)

set(Boost_USE_STATIC_LIBS       ON)  # only find static libs
set(Boost_USE_DEBUG_LIBS        OFF) # ignore debug libs and 
set(Boost_USE_RELEASE_LIBS      ON)  # only find release libs 
set(Boost_USE_MULTITHREADED     ON)
set(Boost_USE_STATIC_RUNTIME    OFF) 

find_package(Boost REQUIRED COMPONENTS atomic chrono regex date_time system filesystem thread graph program_options)
if(Boost_FOUND)
    message(STATUS "Boost_VERSION: ${Boost_VERSION}")

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
# COPY
#
#
#message(${CMAKE_CURRENT_SOURCE_DIR})

#file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/Resources/ 
#     DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/build/${PROJECT_NAME}.app/Contents/Resources/
#)

