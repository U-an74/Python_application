import os
import requests
from dotenv import load_dotenv

# 1. .env 파일 로드
load_dotenv()
kakao_api_key = os.getenv("KAKAO_REST_API_KEY") # .env에 저장한 이름을 확인하세요!

def test_kakao_api(query):
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    
    # 2. 헤더에 REST API 키 넣기
    headers = {"Authorization": f"KakaoAK {kakao_api_key}"}
    
    # 3. 검색할 키워드 설정
    params = {"query": query}
    
    # 4. API 요청 보내기
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        return f"오류 발생: {response.status_code}"

# 5. '제주도 맛집'으로 실제 테스트!
print("🔍 카카오 API로 '제주도 맛집' 검색 중...")
result = test_kakao_api("제주도 맛집")

# 6. 결과 출력 (너무 길 수 있으니 첫 번째 장소 이름만 확인)
if isinstance(result, dict) and 'documents' in result:
    if result['documents']:
        first_place = result['documents'][0]
        print(f"\n✅ 연결 성공!")
        print(f"📍 첫 번째 검색 결과: {first_place['place_name']}")
        print(f"📞 전화번호: {first_place['phone']}")
        print(f"🗺️ 주소: {first_place['address_name']}")
    else:
        print("\n⚠️ 검색 결과가 없어요.")
else:
    print(f"\n❌ 연결 실패: {result}")