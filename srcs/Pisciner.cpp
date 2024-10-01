
#include "../libs/Pisciner.hpp"

Pisciner::Pisciner(){}

Pisciner::Pisciner(std::string username) {
	this->_username = username;
}

std::string	Pisciner::getUsername() {
	return this->_username;
}

Pisciner::~Pisciner(){}