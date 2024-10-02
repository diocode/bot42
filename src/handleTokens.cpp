/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   handleTokens.cpp                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: juno <juno@student.42.fr>                  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2024/10/02 12:19:24 by juno              #+#    #+#             */
/*   Updated: 2024/10/02 12:20:33 by juno             ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../inc/Pisciner.hpp"

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
