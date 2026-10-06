import requests
import os
from dotenv import load_dotenv

load_dotenv()

class KakaoHandler:
    def __init__(self):
        self.api_key = os.getenv("KAKAO_REST_API_KEY")
        self.base_url = "https://dapi.kakao.com/v2/local/search/keyword.json"

    def search_restaurants(self, city_name):
        """
        도시 이름을 기반으로 맛집 5곳을 검색합니다.
        요구사항: name, address, category, url, x, y 포함
        """
        if not self.api_key:
            return None, "KAKAO_REST_API_KEY가 설정되지 않았습니다."

        headers = {"Authorization": f"KakaoAK {self.api_key}"}
        params = {
            "query": f"{city_name} 맛집",
            "size": 5  # 요구사항: 권장 5곳
        }

        try:
            response = requests.get(self.base_url, headers=headers, params=params)
            
            # 인증/권한 오류(401, 403) 등을 포함한 HTTP 에러 체크
            if response.status_code != 200:
                return [], f"카카오 API 오류: 상태 코드 {response.status_code}"

            data = response.json()
            documents = data.get("documents", [])
            
            # 결과가 0건이어도 프로그램은 중단되지 않음
            results = []
            for doc in documents:
                results.append({
                    "name": doc["place_name"],
                    "address": doc["address_name"],
                    "category": doc["category_name"].split(">")[-1].strip(),
                    "url": doc["place_url"],
                    "x": doc["x"],
                    "y": doc["y"]
                })
            
            return results, None

        except Exception as e:
            # 네트워크 오류 등 예외 발생 시 '데이터 없음' 상태로 진행하기 위해 빈 리스트 반환
            return [], f"카카오 API 호출 중 예외 발생: {str(e)}"

if __name__ == "__main__":
    # 단독 테스트용
    handler = KakaoHandler()
    res, err = handler.search_restaurants("강릉")
    print(f"에러: {err}")
    print(f"결과: {res}")