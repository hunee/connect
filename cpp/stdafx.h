/* -*- Mode: C; indent-tabs-mode: t; c-basic-offset: 2; tab-width: 2 -*- */

/**
 * @file stdafx.h
 * @author your name (you@domain.com)
 * @brief 
 * @version 0.1
 * @date 2020-12-06
 * 
 * @copyright Copyright (c) 2020
 * 
 */

#pragma once


/**
 * DEBUG
 */
#ifdef DEBUG
    #ifndef _DEBUG
        #define _DEBUG
    #endif
#endif


/**
 * Finds the compiler type and version.
 */
#if defined (_MSC_VER)
    #define __CC__                      "Microsoft Visual C++"
    #define __CC_VER__                  _MSC_VER

    #if (__CC_VER__ == 1600) //VC10.0
        #define __CC_MAJOR__            10
        #define __CC_MINOR__            0
        #define __CC_PATCHLEVEL__       0
    #elif (__CC_VER__ == 1500) //VC9.0
    #define __CC_MAJOR__                9
        #define __CC_MINOR__            0
        #define __CC_PATCHLEVEL__       0
  #elif (__CC_VER__ == 1400) //VC8.0
        #define __CC_MAJOR__            8
        #define __CC_MINOR__            0
        #define __CC_PATCHLEVEL__       0
  #elif (__CC_VER__ == 1310) //VC7.1
    #define __CC_MAJOR__                7
        #define __CC_MINOR__            1
        #define __CC_PATCHLEVEL__       0
  #else
    #error Unsupported version of Visual Studio
  #endif

#elif defined (__BORLANDC__)
    #define __CC__                      "Borland C++ Compiler"
    #define __CC_VER__                  __BCPLUSPLUS__

    #define __CC_MAJOR__                (__BCPLUSPLUS__ / 0x100)
    #define __CC_MINOR__                (__BCPLUSPLUS__ % 0x100)
    #define __CC_PATCHLEVEL__           (__BCPLUSPLUS__ % 0x100)

#elif defined (__INTEL_COMPILER)
    #define __CC__                      "Intel C/C++ Compiler"
    #define __CC_VER__                  __ICC

    #define __CC_MAJOR__                (__ICC / 100)
    #define __CC_MINOR__                ((__ICC/10) % 10)
    #define __CC_PATCHLEVEL__           (__ICC % 10)

#elif defined (__GNUC__)
    #if defined (__llvm__)
        #if defined (__clang__)
            #define __CC__              "Apple LLVM Compiler"

            #define __CC_VER__          (((__clang_major__) * 100) + (__clang_minor__ * 10) + __clang_patchlevel__)

            #define __CC_MAJOR__        __clang_major__
            #define __CC_MINOR__        __clang_minor__
            #define __CC_PATCHLEVEL__   __clang_patchlevel__

        #else
            #define __CC__              "GNU LLVM Compiler"
            #define __CC_VER__          (((__GNUC__) * 100) + (__GNUC_MINOR__ * 10) + __GNUC_PATCHLEVEL__)

            #define __CC_MAJOR__        __GNUC__
            #define __CC_MINOR__        __GNUC_MINOR__
            #define __CC_PATCHLEVEL__   __GNUC_PATCHLEVEL__
        #endif

    #elif defined (__MINGW32__)
        #define __CC__                  "MinGW GCC Compiler"
        #define __CC_VER__              __MINGW32_VERSION

        #define __CC_MAJOR__            __MINGW32_MAJOR_VERSION
        #define __CC_MINOR__            __MINGW32_MINOR_VERSION
        #define __CC_PATCHLEVEL__       __MINGW32_PATCHLEVEL

        /** Disable unicode support on MingW at the moment, poorly supported in stdlibc++
         * STLPORT fixes this though so allow if found
         * MinGW C++ Toolkit supports unicode and sets the define __MINGW32_TOOLKIT_UNICODE__ in _mingw.h
         */
        #if !defined (_STLPORT_VERSION)
            #include <_mingw.h>
            #if defined (__MINGW32_TOOLBOX_UNICODE__)
                #define _UNICODE 1
        #endif
    #endif

    #else
        #define __CC__                  "GNU GCC Compiler"
        #define __CC_VER__              (((__GNUC__) * 100) + (__GNUC_MINOR__ * 10) + __GNUC_PATCHLEVEL__)

    #define __CC_MAJOR__                __GNUC__
        #define __CC_MINOR__            __GNUC_MINOR__
        #define __CC_PATCHLEVEL__       __GNUC_PATCHLEVEL__
    #endif

#else
    #pragma error "No known compiler. Abort! Abort!"
#endif


/**
 *
 */
#if defined (__GNUC__)
    #define DECLARE_DEPRECATED(func) func __attribute__((deprecated))
#elif defined (_MSC_VER)
    #define DECLARE_DEPRECATED(func) __declspec(deprecated) func
#else
    #pragma message("WARNING: You need to implement DECLARE_DEPRECATED for this compiler.")
    #define DECLARE_DEPRECATED(func) func
#endif

/**void NEW_AAA(int aaa)
 {
     std::cout << __FUNCTION__ << std::endl;
 }
 DECLARE_DEPRECATED(void AAA(int aaa));
 void AAA(int aaa)
 {
     NEW_AAA(aaa);
 }
 **/



/**
 * For generating compiler warnings - should work on any compiler
 * As a side note, if you start your message with 'Warning: ', the MSVC IDE actually does catch a warning :)
 */
#define QUOTE_INPLACE(x) # x
#define QUOTE(x) QUOTE_INPLACE(x)
#define WARN(x)  message(__FILE__ "(" QUOTE(__LINE__) ") : " x "\n")


/** See if we can use __forceinline or if we need to use __inline instead */
#if (_MSC_VER >= 1200)
	#define FORCEINLINE __forceinline
#elif defined (__MINGW32__)
	#if !defined (FORCEINLINE)
		#define FORCEINLINE __inline
	#endif

#else
	#define FORCEINLINE __inline
#endif



/**
 * Platform depended macros
 */

//#ifdef __TARGRT_GL__
//#ifdef __TARGRT_DX11__
//#ifdef __TARGRT_DX12__

//#ifdef __TARGRT_EGL__
//#ifdef __TARGRT_METAL__
//#ifdef __TARGRT_VULKAN__



// Apple
#if defined (__APPLE__)
    #include <Availability.h>
    #include <TargetConditionals.h>

    // IOS
	#if defined (__IPHONE_OS_VERSION_MAX_ALLOWED)
		#define __TARGET_IOS__
		//#define __TARGET_EGL__
        #define __TARGRT_METAL__

		#if defined (TARGET_IPHONE_SIMULATOR)
			#define __TARGET_SIMULATOR__
		#endif
	
	// Mac
	#elif defined (__MAC_OS_X_VERSION_MAX_ALLOWED)
        #define __TARGET_MACOS__
		#define __TARGET_GL__
        //#define __TARGRT_METAL__

		#if defined (_USRDLL)
			#define SHARED __attribute__((visibility("default")))
		#endif

		#define SHARED_EXPORT extern "C"
	#endif


#endif

// Google Android
#if defined (ANDROID)
#endif

// Linux
#if defined (_LINUX)
    #include <X11/Xlib.h>
    #include <X11/Xutil.h>

    // Headers needed for keys used in the program
    #include <X11/extensions/xf86vmode.h>
    #include <X11/keysym.h>
#endif

// Microsoft Windows
#if defined (WIN32)
    // STRICT is the only supported option (NOSTRICT is no longer supported)
    #ifndef STRICT
        #define STRICT
    #endif //STRICT

    // If app hasn't choosen, set to work with Windows 98, Windows Me, Windows 2000, Windows XP and beyond
    #ifndef WINVER
        #define WINVER         0x0410
    #endif //WINVER

    #ifndef _WIN32_WINDOWS
        #define _WIN32_WINDOWS 0x0410
    #endif //_WIN32_WINDOWS

    #ifndef _WIN32_WINNT
        #define _WIN32_WINNT   0x0500
    #endif //_WIN32_WINNT

    #ifndef NOMINMAX
    #define NOMINMAX
    #endif

    #define WIN32_LEAN_AND_MEAN        // Exclude rarely-used stuff from Windows headers
    #include <windows.h>
    #undef WIN32_LEAN_AND_MEAN

    #include <shellapi.h>
    #include <mmsystem.h>        // timeGetTime()

    #if defined (_MSC_VER)
        #pragma comment(lib, "winmm.lib")
    #endif

    /**
     *
     */
    #if defined (_MSC_VER)
        #if !defined (_CRT_SECURE_NO_DEPRECATE)
            #define _CRT_SECURE_NO_DEPRECATE
        #endif //_CRT_SECURE_NO_DEPRECATE

        #if !defined (_CRT_SECURE_NO_WARNINGS)
            #define _CRT_SECURE_NO_WARNINGS
        #endif

        // disable: deprecation warnings when using CRT calls in VC8
        // These show up on all C runtime lib code in VC8, disable since they clutter
        // the warnings with things we may not be able to do anything about (e.g.
        // generated code from nvparse etc). I doubt very much that these calls
        // will ever be actually removed from VC anyway, it would break too much code.
        #pragma warning( disable: 4996)
    #endif

    // CRT's memory leak detection
	#if defined (_DEBUG)
		#if defined (_MSC_VER)
			#include <crtdbg.h>

			/*#ifndef DBG_NEW
				#define DBG_NEW new (_NORMAL_BLOCK , __FILE__ , __LINE__)
				#define new DBG_NEW
			#endif*/

			#define DBG_BREAK(n) _CrtSetBreakAlloc(n)
		#endif
	#endif //DEBUG
#endif


//
#if !defined (PATH_MAX)
    #define PATH_MAX    MAX_PATH
#endif //PATH_MAX

//
#if !defined (NAME_MAX)
    #define NAME_MAX    (80)
#endif //NAME_MAX

#define UNUSED_PARAM(unusedparam)   (void)unusedparam



/*
#include <iostream>
#include <clocale>
#include <cstdlib>
 
int main()
{
    std::setlocale(LC_ALL, "en_US.utf8");
    // UTF-8 narrow multibyte encoding
    const wchar_t* wstr = L"z\u00df\u6c34\U0001d10b"; // or L"zß水𝄋"
    char mbstr[11];
    std::wcstombs(mbstr, wstr, 11);
    std::cout << "multibyte string: " << mbstr << '\n';
}
*/
#include <cstdlib>

#define W2M(m, w) std::wcstombs(m, w, sizeof(m))
#define M2W(w, m) std::mbstowcs(w, m, sizeof(w))



/**
 */
#include <map>
#include <unordered_map>
#include <list>
#include <vector>
#include <deque>

#include <string>
#include <iostream>

#include <memory>
#include <algorithm>

#include <stdexcept>

///
#define PY_SSIZE_T_CLEAN
#include <Python.h>


#include "type_info.h"

///
#include "colors.h"
#include "logger.h"

#include "renderer/math/math.h"
