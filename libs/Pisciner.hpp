#ifndef CLIENT_HPP
#define CLIENT_HPP

#include "skynet.hpp"

class Pisciner
{
	private:
			std::string _username;

	public:
			Pisciner();
			Pisciner(std::string username);
			~Pisciner();

			std::string	getUsername();
};

#endif