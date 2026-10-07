import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# 1. OpenAI 클라이언트 설정
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL") # 코디세이 발급 api 사용 시 필요
)

def test_openai_api(user_input):
    print(f"🤖 AI가 '{user_input}' 분석 중...")
    
    response = client.chat.completions.create(
        model="gpt-5.4", # 사용 가능한 모델명으로 테스트
        messages=[
            {"role": "system", "content": "당신은 여행 전문가입니다. 사용자의 요청에서 카카오 맵에 검색할 키워드 딱 하나만 추출하세요. 예: '제주도 맛집'"},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content

# 2. AI 테스트
keyword = test_openai_api("나 이번 주말에 제주도 가는데 맛있는 거 먹고 싶어!")
print(f"✨ AI가 추출한 키워드: {keyword}")
