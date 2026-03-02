import requests

def handle_success(access_token: str) -> dict | None:
    try:
        url = "https://www.googleapis.com/oauth2/v3/userinfo"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # raises error if status != 200
        
        data = response.json()
        print("User Authenticated:", data)
        return data

    except requests.exceptions.RequestException as error:
        print("Profile fetch failed:", error)
        return None
    
