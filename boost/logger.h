/* -*- Mode: C; indent-tabs-mode: t; c-basic-offset: 2; tab-width: 2 -*- */

#pragma once


/**
 * TRACE
 */
//#undef TRACE
//#undef TRACEF

#if defined (_DEBUG)

    #include <cstdarg>
    #include <cstdio>
 
    inline int __std_printf(const char * fmt, ...)
    {
        std::va_list vl;
        va_start(vl, fmt);
        int ret = std::vfprintf(stdout, fmt, vl);
        va_end(vl);
        return ret;
    }

    #if defined (_MSC_VER)
        #define TRACE(fmt, ...) _printf("%s(%d): - " fmt, __FILE__, __LINE__, ##__VA_ARGS__)
        #define TRACEL(fmt, ...) _printf(fmt, ##__VA_ARGS__)
        #define TRACEF() _printf("%s(%d): - %s\n", __FILE__, __LINE__, __FUNCTION__)

    #elif defined (__BORLANDC__)
        #define TRACE(fmt, args...) _printf("%s(%d): - " fmt, __FILE__ __LINE__, ##args)
        #define TRACEL(fmt, args...) _printf(fmt, ##args)
        #define TRACEF() _printf("%s(%d): - %s\n", __FILE__, __LINE__, __FUNC__)

    #else //GCC
        //
        #define LOG(fmt, args...) __std_printf(fmt, ##args);        
        #define LOGF() __std_printf(">> %s%s%s:%d%s: %s- %s%s\n", KCYN, KUNDL, __FILE__, __LINE__, RST, KBLU, __PRETTY_FUNCTION__, RST)

        #define CLOG(fmt, args...) __std_printf(">> %s%s(%p)%s: - " fmt, KGRN, typeid_name(*this), this, RST, ##args); __std_printf("%s\n", RST);
        #define CLOGF() __std_printf(">> %s%s(%p)%s: %s%s%s:%d%s: %s- %s%s\n", KGRN, typeid_name(*this), this, RST, KCYN, KUNDL, __FILE__, __LINE__, RST, KBLU, __PRETTY_FUNCTION__, RST)
        #define YLOGF() __std_printf(">> %s%s(%p)%s: %s%s%s:%d%s: %s- %s%s\n", KGRN, typeid_name(*this), this, RST, KCYN, KUNDL, __FILE__, __LINE__, RST, KYEL, __PRETTY_FUNCTION__, RST)

        // shared_ptr
        #define LOGPTR(p) {if (p) { LOGF(); LOG(">> - %sstd::shared_ptr<%s>() - %s: use_count: %d%s\n", KYEL, typeid_name(*(p)), #p, p.use_count(), RST); }}
        #define CLOGPTR(p) {if (p) { CLOGF(); CLOG("%sstd::shared_ptr<%s>() - %s: use_count: %d%s", KYEL, typeid_name(*(p)), #p, p.use_count(), RST); }}

    #endif //_MSC_VER

/////
    #define COUT std::cout << KMAG << ">> " << RST
    #define THIS KGRN << typeid_name(*this) << "(" << this << ")" << RST << ": "
    #define FUNC KCYN << KUNDL << __FILE__ << ":" << __LINE__ << RST << ":" << KBLU << " - " << __PRETTY_FUNCTION__ << RST
    #define ENDL RST << std::endl

    #define SHARED_PTR(p) KYEL << "shared_ptr<" << typeid_name(*(p)) << "> (" << #p << ", " << p.use_count() << ")" << RST

#else
    #if defined (_MSC_VER)
        #define TRACE(fmt, ...)
        #define TRACEL(fmt, ...)

    #elif defined (__BORLANDC__)
        #define TRACE(fmt, args...)
        #define TRACEL(fmt, args...)

    #else //GCC
        #define TRACE(fmt, args...)
        #define TRACEL(fmt, args...)
        #define TRACEFC()
    #endif //_MSC_VER

    #define TRACEF()

    #define TRACEC()
    #define TRACE0(msg)

    //
    #define CLOG(msg)

    //__FILE__, __LINE__, __PRETTY_FUNCTION__
    #define CLOG_FLF(msg)

#endif //_DEBUG



#define E_str() "%sexception: %s%s%s:%d%s - %s%s%s", KRED, KCYN, KUNDL, __FILE__,__LINE__, RST, KBLU, __PRETTY_FUNCTION__, RST

//throw ...
//char e[255];
//sprintf(e, E());

//throw std::runtime_error(e);

