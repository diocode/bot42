/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   Pisciner.cpp                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: juno <juno@student.42.fr>                  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2024/10/02 10:57:42 by juno              #+#    #+#             */
/*   Updated: 2024/10/02 12:07:54 by passunca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */


#include "../inc/Pisciner.hpp"

Pisciner::Pisciner(){}

Pisciner::Pisciner(std::string username) {
	this->_username = username;
}

std::string	Pisciner::getUsername() {
	return this->_username;
}

Pisciner::~Pisciner(){}
