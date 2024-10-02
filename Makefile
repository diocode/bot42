# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: juno <juno@student.42.fr>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/10/02 10:57:44 by juno              #+#    #+#              #
#    Updated: 2024/10/02 10:57:45 by juno             ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME = skynet
SRCS_DIR = srcs
OBJ_DIR = bin
SRCS = $(wildcard $(SRCS_DIR)/*.cpp)
OBJ	= $(patsubst $(SRCS_DIR)/%.cpp, $(OBJ_DIR)/%.o, $(SRCS))
RM = rm -rf
CXX = c++
CXXFLAGS = -Wall -Wextra -Werror -std=c++98
INC = libs/

all: $(NAME)

$(OBJ_DIR):
	@mkdir -p $(OBJ_DIR)

$(OBJ_DIR)/%.o: $(SRCS_DIR)/%.cpp | $(OBJ_DIR)
	@$(CXX) $(CXXFLAGS) -I $(INC) -c $< -o $@
	
$(NAME): $(OBJ)
		@ $(CXX) $(OBJ) $(CXXFLAGS) -o $(NAME)

clean:
		@$(RM) $(OBJ)
		
fclean: clean
		@$(RM) $(NAME)
		@$(RM) $(OBJ_DIR)

re: fclean all