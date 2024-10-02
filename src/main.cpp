/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.cpp                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: juno <juno@student.42.fr>                  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2024/10/02 10:57:28 by juno              #+#    #+#             */
/*   Updated: 2024/10/02 12:07:36 by passunca         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../inc/Pisciner.hpp"

// Callback to handle data received by libcurl
static size_t WriteCallback(void* contents, size_t size, size_t nmemb, void* userp) {
    size_t totalSize = size * nmemb;
    struct Memory* mem = (struct Memory*)userp;
    char* ptr = (char*)realloc(mem->response, mem->size + totalSize + 1);
    if (ptr == NULL) {
        std::cerr << "Error: realloc error\n";
        return 0;
    }
    mem->response = ptr;
    memcpy(&(mem->response[mem->size]), contents, totalSize);
    mem->size += totalSize;
    mem->response[mem->size] = 0;
    return totalSize;
}

// Simple function to extract "access_token" from the JSON response
std::string extractAccessToken(const std::string& jsonResponse) {
    std::string tokenKey = "\"access_token\":\"";
    size_t startPos = jsonResponse.find(tokenKey);
    if (startPos == std::string::npos) {
        return "";
    }
    startPos += tokenKey.length();
    size_t endPos = jsonResponse.find("\"", startPos);
    if (endPos == std::string::npos) {
        return "";
    }
    return jsonResponse.substr(startPos, endPos - startPos);
}

std::string getAccessToken() {
    CURL* curl;
    CURLcode res;
    struct Memory tokenResponse = {NULL, 0};
    std::string accessToken = "";

    curl = curl_easy_init();
    if (curl) {
        std::string postFields = "grant_type=client_credentials&client_id=u-s4t2af-cb4317c54cd61ab3228de498de225bee0d82dea159be598d0cb84fcbbfdf8958&client_secret=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";
        curl_easy_setopt(curl, CURLOPT_URL, "https://api.intra.42.fr/oauth/token");
        curl_easy_setopt(curl, CURLOPT_POST, 1L);
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, postFields.c_str());

        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void*)&tokenResponse);

        res = curl_easy_perform(curl);
        if (res != CURLE_OK) {
            std::cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res) << std::endl;
        } else {
            // Extract the access token from the JSON response
            std::string jsonResponse(tokenResponse.response);
            accessToken = extractAccessToken(jsonResponse);
        }

        free(tokenResponse.response);
        curl_easy_cleanup(curl);
    }

    return accessToken;
}

bool checkUser(const std::string& username, const std::string& accessToken) {
    CURL* curl;
    CURLcode res;
    struct Memory userResponse = {NULL, 0};
    bool userExists = false;

    curl = curl_easy_init();
    if (curl) {
        std::string userUrl = "https://api.intra.42.fr/v2/users/" + username;
        curl_easy_setopt(curl, CURLOPT_URL, userUrl.c_str());

        // Set Authorization header
        struct curl_slist* headers = NULL;
        std::string bearerToken = "Authorization: Bearer " + accessToken;
        headers = curl_slist_append(headers, bearerToken.c_str());
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void*)&userResponse);

        res = curl_easy_perform(curl);
        if (res != CURLE_OK) {
            std::cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res) << std::endl;
        } else {
            long responseCode;
            curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &responseCode);

            if (responseCode == 200) {
                // User found
                userExists = true;
            } else if (responseCode == 404) {
                // User not found
                userExists = false;
            }
        }

        free(userResponse.response);
        curl_slist_free_all(headers);
        curl_easy_cleanup(curl);
    }

    return userExists;
}

int	main(int ac, char **av) {
	if (ac != 2)
	{
		std::cerr << "Usage: " << av[0] << " <username>" << std::endl;
		return 1;
	}

	std::string accessToken = getAccessToken();
    if (accessToken.empty()) {
        std::cerr << "Error: Failed to get access token\n";
        return 1;
    }

	if (checkUser(username, accessToken))
        std::cout << "User exists in the 42 system.\n";
    else
        std::cout << "User does not exist in the 42 system.\n";
    
}
