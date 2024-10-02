/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   Pisciner.hpp                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: juno <juno@student.42.fr>                  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2024/10/02 10:57:39 by juno              #+#    #+#             */
/*   Updated: 2024/10/02 10:57:40 by juno             ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

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