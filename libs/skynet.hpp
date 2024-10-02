/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   skynet.hpp                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: juno <juno@student.42.fr>                  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2024/10/02 10:57:33 by juno              #+#    #+#             */
/*   Updated: 2024/10/02 10:57:34 by juno             ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

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