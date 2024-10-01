#ifndef SKYNET_HPP
#define SKYNET_HPP

/*============= LIBRARIES =============*/

#include "Pisciner.hpp"
#include <iostream>
#include <string>
#include <cstring>
#include <cstdlib>
#include <curl/curl.h>


/*============= STRUCTS ===============*/

struct Memory {
    char* response;
    size_t size;
};

#endif