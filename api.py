import requests
import os
from dotenv import load_dotenv


load_dotenv()

api_url = os.getenv("API_URL")


def send_weather():
    if api_url is None:
        print("API URL을 불러오지 못했습니다.")
        return None

    params = {
        "latitude": 37.5665,
        "longitude": 126.9780,
        "current": "weather_code",
        "timezone": "Asia/Seoul"
    }

    try:
        response = requests.get(
            api_url,
            params=params,
            timeout=5
        )

        response.raise_for_status()

        data = response.json()

    except requests.exceptions.ConnectionError:
        print("연결 실패")
        return None

    except requests.exceptions.Timeout:
        print("타임아웃")
        return None

    except requests.exceptions.HTTPError:
        print("HTTP 에러")
        return None

    except requests.exceptions.JSONDecodeError:
        print("JSON 파싱 실패")
        return None

    else:
        weather_code = data["current"]["weather_code"]
        return weather_code