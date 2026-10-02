import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class LLMHandler:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        # JSON 모드 없이 진행
        self.model = "gpt-5.4"

    def get_initial_recommendation(self, date, retry_count=0):
        system_prompt = (
            "당신은 한국 여행 전문가입니다. 반드시 다음 JSON 형식을 지켜서 답변하세요. "
            "다른 설명은 하지 말고 오직 JSON 데이터만 출력하세요.\n"
            "{\n"
            '  "recommended_city": "도시이름",\n'
            '  "weather": "날씨 요약",\n'
            '  "events": ["행사1", "행사2"],\n'
            '  "reason": "추천 근거 2~4문장"\n'
            "}"
        )
        
        user_prompt = f"{date}에 한국에서 여행하기 좋은 도시를 하나 추천해줘."

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
                # response_format 옵션을 제거하여 호환성을 높였습니다.
            )
            
            content = response.choices[0].message.content.strip()
            
            # LLM이 만약 ```json ... ``` 형태로 답했을 경우를 대비해 정제합니다.
            if content.startswith("```"):
                content = content.replace("```json", "").replace("```", "").strip()
            
            result = json.loads(content)
            return result, None

        except Exception as e:
            if retry_count < 1:
                print(f"LLM 파싱 실패. 재시도 중... ({e})")
                return self.get_initial_recommendation(date, retry_count + 1)
            else:
                return None, f"LLM 추천 생성 실패: {str(e)}"

    def generate_final_report(self, plan_data, restaurants):
        system_prompt = "제공된 정보를 바탕으로 깔끔하고 친절한 여행 리포트를 Markdown 형식으로 작성하세요."
        
        restaurant_info = ""
        if not restaurants:
            restaurant_info = "데이터 없음"
        else:
            for res in restaurants:
                restaurant_info += f"- {res['name']} ({res.get('category', '식당')}): {res['address']} [카카오맵]({res.get('url', '#')})\n"

        user_prompt = f"""
        아래 정보를 바탕으로 여행 리포트를 작성해줘.
        
        1. 추천 지역 및 이유: {plan_data['recommended_city']} - {plan_data['reason']}
        2. 날씨: {plan_data['weather']}
        3. 행사/축제: {', '.join(plan_data['events'])}
        4. 맛집 리스트:
        {restaurant_info}
        
        [요구사항]
        - 추천 지역 + 추천 이유 요약 포함
        - 날씨 및 행사 목록 포함
        - 맛집 리스트 포함 (없으면 '데이터 없음' 표기)
        - 1일 일정 제안 (오전/오후/저녁)
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response.choices[0].message.content, None
        except Exception as e:
            return None, f"최종 리포트 생성 실패: {str(e)}"

if __name__ == "__main__":
    handler = LLMHandler()
    print("=== 1차 추천 테스트 시작 ===")
    test_date = "2024-12-25"
    plan, error = handler.get_initial_recommendation(test_date)
    
    if error:
        print(f"에러 발생: {error}")
    else:
        print(f"결과: {plan}")
        print("\n=== 최종 리포트 테스트 시작 ===")
        fake_restaurants = [
            {"name": "맛있는 식당", "category": "한식", "address": "서울시 어딘가", "url": "https://map.kakao.com/123"},
            {"name": "분위기 카페", "category": "카페", "address": "서울시 건너편", "url": "https://map.kakao.com/456"}
        ]
        report, report_error = handler.generate_final_report(plan, fake_restaurants)
        if report_error:
            print(f"리포트 에러: {report_error}")
        else:
            print("--- 생성된 리포트 ---")
            print(report)