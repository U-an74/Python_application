import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# 검증 함수를 클래스 외부에 독립적으로 정의
def validate_response(result):
    """LLM 응답 데이터의 필수 키와 타입을 검증합니다."""
    required_schema = {
        "recommended_city": str,
        "weather": str,
        "events": list,
        "reason": str
    }
    
    for key, expected_type in required_schema.items():
        if key not in result:
            raise ValueError(f"필수 키 누락: {key}")
        if not isinstance(result[key], expected_type):
            raise TypeError(f"데이터 타입 불일치: {key} (기대: {expected_type.__name__})")

load_dotenv()
class LLMHandler:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-5.4" 

    def get_initial_recommendation(self, date, retry_count=0):
        # 1. 기본 시스템 프롬프트
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

        # --- 보안/보강 로직 추가 ---
        if retry_count > 0:
            # 재시도 시 시스템 프롬프트에 강력한 경고 문구 추가
            system_prompt += (
                "\n\n⚠️ 주의: 이전 응답에서 JSON 파싱 오류가 발생했습니다. "
                "절대로 서론이나 결론을 쓰지 마세요. "
                "마크다운 코드 블록(```json)도 사용하지 말고, "
                "오직 중괄호 '{' 로 시작해서 '}' 로 끝나는 JSON 데이터만 보내주세요."
            )
            # 유저 프롬프트도 더 명확하게 보강
            user_prompt = f"{date} 여행지 추천을 '순수 JSON 데이터'로만 다시 응답해줘."
        # ------------------------------------------

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            content = response.choices[0].message.content.strip()
            
            # JSON 정제 로직 (보정 규칙)
            if content.startswith("```"):
                content = content.replace("```json", "").replace("```", "").strip()
            
            # 만약 JSON 앞뒤에 불필요한 문구가 붙어있을 경우를 대비한 최소한의 보정
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            if start_idx != -1 and end_idx != 0:
                content = content[start_idx:end_idx]

            result = json.loads(content)

            # 위에서 정의한 검증 함수 호출
            validate_response(result)
        
            # 스키마 검증 로직 추가
            required_keys = ["recommended_city", "weather", "events", "reason"]
            if not all(key in result for key in required_keys):
                raise ValueError(f"필수 키 누락: {set(required_keys) - set(result.keys())}")

            return result, None

        except Exception as e:
            if retry_count < 1:
                print(f"LLM 파싱 실패. 보강된 프롬프트로 재시도 중... ({e})")
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