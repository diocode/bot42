import os
import requests
import logging
from pprint import pprint

piscine_data = {}

def get_42_api_token():
    client_id = os.getenv("INTRA_UID")
    client_secret = os.getenv("INTRA_SECRET")
    token_url = "https://api.intra.42.fr/oauth/token"

    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }

    response = requests.request("POST", token_url, data=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception("Failed to obtain 42 API token")


def validate_student(user):
    token = get_42_api_token()
    url = f"https://api.intra.42.fr/v2/users/{user}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.status_code == 200


def get_student_data(user):
    try:
        token = get_42_api_token()
        url = f"https://api.intra.42.fr/v2/users/{user}"
        headers = {"Authorization": f"Bearer {token}"}

        response = None
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            if response.status_code == 200:
                return response.json()
            else:
                logging.error(f"Unexpected status code: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching student data for user {user}: {str(e)}")
            if response:
                logging.error(f"Response content: {response.text}")
            else:
                logging.error("No response received")
            return None

    except Exception as e:
        logging.error(f"Error in get_student_data for user {user}: {str(e)}")
        return None


def get_piscine_data(campus, year, month):
    try:
        token = get_42_api_token()
        url = f"https://api.intra.42.fr/v2/campus/{campus}/users"
        headers = {
            "Authorization": f"Bearer {token}"
        }

        params = {
            "filter[pool_year]": year,
            "filter[pool_month]": month,
            "page[size]": 100
        }
        piscine_data = []
        page = 1

        while True:
            params["page[number]"] = page
            response = None
            try:
                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()  # Raises an HTTPError for bad responses
                data = response.json()
                piscine_data.extend(data)
                pprint(data)
                if len(data) < params["page[size]"]:
                    break
                page += 1
            except requests.exceptions.RequestException as e:
                logging.error(f"Error fetching page {page}: {str(e)}")
                if response:
                    logging.error(f"Response content: {response.text}")
                else:
                    logging.error("No response received")
                return None

        return piscine_data

    except Exception as e:
        logging.error(f"Error in get_piscine_data: {str(e)}")
        return None

def get_student_location(identifier, campus):
    try:
        if identifier:
            if identifier.startswith('c'):
                data = get_user_at_location(identifier)
                if isinstance(data, list) and len(data) > 0:
                    location = data[0].get('location')
                    user = data[0].get('login', {}).get('login')
                else:
                    return None, None
            else:
                data = get_student_data(identifier)
                if data is None:
                    return None, None
                location = data.get('location')
                user = data.get('login')
            
            return user, location
        else:
            return None, None

    except Exception as e:
        logging.error(f"Unexpected error in get_student_location: {str(e)}")
        return None, None


def get_user_at_location(identifier, campus):
    try:
        token = get_42_api_token()
        url = f"https://api.intra.42.fr/v2/locations/{campus}"
        headers = {"Authorization": f"Bearer {token}"}
        # Assuming there's an API endpoint to fetch location data
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if data:
            # Format the data as expected by get_student_location
            return [{
                'location': entry['host'],
                'login': {'login': entry['user']['login']}
            } for entry in data if entry['host'] == identifier]
        else:
            return []

    except requests.exceptions.RequestException as e:
        logging.error(f"Error in get_user_at_location: {str(e)}")
        if 'response' in locals():
            logging.error(f"Response content: {response.text}")
        else:
            logging.error("No response received")
        return []
    except Exception as e:
        logging.error(f"Unexpected error in get_user_at_location: {str(e)}")
        return []
