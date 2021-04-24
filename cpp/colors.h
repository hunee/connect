#ifndef _COLORS_
#define _COLORS_

/* FOREGROUND */
#define RST  "\x1B[0m"
#define KRED  "\x1B[31m"
#define KGRN  "\x1B[32m"
#define KYEL  "\x1B[33m"
#define KBLU  "\x1B[34m"
#define KMAG  "\x1B[35m"
#define KCYN  "\x1B[36m"
#define KWHT  "\x1B[37m"

#define KBOLD	"\x1B[1m"
#define KUNDL	"\x1B[4m"

#define KCLR    "\x1B[2Jm\x1B[1;1H"

#define FRED(x) KRED x RST
#define FGRN(x) KGRN x RST
#define FYEL(x) KYEL x RST
#define FBLU(x) KBLU x RST
#define FMAG(x) KMAG x RST
#define FCYN(x) KCYN x RST
#define FWHT(x) KWHT x RST

#define BOLD(x)	"\x1B[1m" x RST
#define UNDL(x)	"\x1B[4m" x RST

/*
#include <iostream>
#include "colors.h"
using namespace std;

int main()
{
    cout << FBLU("I'm blue.") << endl;
    cout << BOLD(FBLU("I'm blue-bold.")) << endl;
    return 0;
}
*/


#if 0

////
#include <unordered_map>
#include <string>

namespace color
{

    const static std::unordered_map<std::string, std::string> color_foreground =
    {
        { "Default", "39" },
        { "Black", "30" },
        { "Red", "31" },
        { "Green", "32" },
        { "Yellow", "33" },
        { "Blue", "34" },
        { "Magenta", "35" },
        { "Cyan", "36" },
        { "Light Gray", "37" },
        { "Dark Gray", "90" },
        { "Light Red", "91" },
        { "Light Green", "92" },
        { "Light Yellow", "93" },
        { "Light Blue", "94" },
        { "Light Magenta", "95" },
        { "Light Cyan", "96" },
        { "White", "97" }
    };

    const static std::unordered_map<std::string, std::string> color_background =
    {
        { "Default", "49" },
        { "Black", "40" },
        { "Red", "41" },
        { "Green", "42" },
        { "Yellow", "43" },
        { "Blue", "44" },
        { "Megenta", "45" },
        { "Cyan", "46" },
        { "Light Gray", "47" },
        { "Dark Gray", "100" },
        { "Light Red", "101" },
        { "Light Green", "102" },
        { "Light Yellow", "103" },
        { "Light Blue", "104" },
        { "Light Magenta", "105" },
        { "Light Cyan", "106" },
        { "White", "107" }
    };


    const static std::unordered_map<std::string, std::string> formatting_set =
    {
        { "Default", "0" },
        { "Bold", "1" },
        { "Dim", "2" },
        { "Underlined", "4" },
        { "Blink", "5" },
        { "Reverse", "7" },
        { "Hidden", "8" }
    };

    const static std::unordered_map<std::string, std::string> formatting_reset =
    {
        { "All", "0" },
        { "Bold", "21" },
        { "Dim", "22" },
        { "Underlined", "24" },
        { "Blink", "25" },
        { "Reverse", "27" },
        { "Hidden", "28" }
    };

    // Usage:
    //
    //      auto new_message = color::rize( "I am a banana!", "Yellow", "Green" );
    //      std::cout << new_message << std::endl;
    //
    inline std::string rize( std::string const& source,
                             std::string foreground_color = "Default",
                             std::string background_color = "Default",
                             std::string set_formatting = "Default",
                             std::string reset_formatting = "All"
                           )
    {
        std::string const control = "\033";

        if ( color_foreground.find( foreground_color ) == color_foreground.end() )
            foreground_color = "Default";

        if ( color_background.find( background_color ) == color_background.end() )
            background_color = "Default";

        if ( formatting_set.find( set_formatting ) == formatting_set.end() )
            set_formatting = "Default";

        if ( formatting_reset.find( reset_formatting ) == formatting_reset.end() )
            reset_formatting = "All";

        std::string ans =   control  + std::string{"["} +
                            formatting_set.at( set_formatting ) + std::string{";"} +
                            color_background.at( background_color ) + std::string{";"} +
                            color_foreground.at( foreground_color ) + std::string{"m"} +
                            source +
                            control + std::string{"["} +
                            formatting_reset.at( reset_formatting ) + std::string{"m"};
        return ans;
    }

}//namespace color
#endif

/*
//example.cpp
std::string message{"I am a Banana!"};
// Output message with
//              foreground color -- Yellow
//              background color -- Green
std::cout   << color::rize( message, "Yellow", "Green" )
            << std::endl;
*/

#include <iostream>
#define __function__ std::cout << KYEL << ">> " << __PRETTY_FUNCTION__ << RST << std::endl;


#endif	/* _COLORS_ */