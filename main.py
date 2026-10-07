import argparse
import os
import json
from datetime import datetime
from llm_handler import LLMHandler
from kakao_handler import KakaoHandler


def check_cache(date):
    cache_path = f"results/cache_{date}.json"
    if os.path.exists(cache_path):
        print("캐시된 데이터를 사용합니다.")
        return True
    return False

def validate_date(date_str):
    """YYYY-MM-DD 형식 검증"""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y-%m-%d')
    except ValueError:
        return None

def main():
    # 1. CLI 인자 설정
    parser = argparse.ArgumentParser(description="국내 여행지 추천 및 맛집 검색 프로그램")
    # -d와 --date 둘 다 사용할 수 있게 변경
    parser.add_argument("-d", "--date", required=True, help="여행 날짜를 입력하세요 (형식: YYYY-MM-DD)")
    args = parser.parse_args()

    # 2. 날짜 검증
    travel_date = validate_date(args.date)
    if not travel_date:
        print("에러: 날짜 형식이 올바르지 않습니다. (YYYY-MM-DD 형식 필요)")
        return

    print(f"--- {travel_date} 여행 계획 생성을 시작합니다 ---")
    
    errors = []
    llm = LLMHandler()
    kakao = KakaoHandler()

    # 3. LLM 1차 추천 (도시/날씨/행사)
    print("[1/3] LLM에게 도시 추천을 요청 중...")
    plan_data, llm_err = llm.get_initial_recommendation(travel_date)
    
    if llm_err:
        print(f"경고: {llm_err}")
        errors.append(llm_err)
        # LLM 추천 실패 시 더 이상 진행 불가
        return

    # 4. Kakao 맛집 검색
    city = plan_data.get("recommended_city")

    # 기본값 사용 로그 명시
    if not city:
        print("⚠️ [LOG] LLM 응답에 도시명이 없어 기본값 '서울'을 사용합니다.")
        city = "서울"
    else:
        print(f"✅ [LOG] LLM 추천 도시 '{city}'를 기반으로 장소를 검색합니다.")
    
    print(f"[2/3] '{city}' 지역 맛집 검색 중...")
    restaurants, kakao_err = kakao.search_restaurants(city)
    
    if kakao_err:
        print(f"경고: {kakao_err}")
        errors.append(kakao_err)

    # 5. LLM 최종 리포트 생성
    print("[3/3] 최종 여행 리포트 생성 중...")
    report_md, report_err = llm.generate_final_report(plan_data, restaurants)
    
    if report_err:
        errors.append(report_err)
        report_md = "# 리포트 생성 실패\n상세 내용은 JSON 로그를 확인하세요."

    else:
        # 1. 메타데이터 내용 구성
        metadata = f"""> **[Metadata]**
> - 조회 기준 날짜: {travel_date}
> - 리포트 생성 일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
> - 데이터 출처: OpenAI GPT, Kakao Local API
\n\n"""
        # 2. 기존 리포트 내용 앞에 메타데이터를 붙임
        report_md = metadata + report_md

    # 6. 결과 저장 (results/ 폴더)
    os.makedirs("results", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # JSON 저장 (원본 데이터 + 에러 로그)
    json_filename = f"results/result_{timestamp}.json"
    raw_data = {
        "recommendation": plan_data,
        "restaurants": restaurants,
        "errors": errors
    }
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(raw_data, f, ensure_ascii=False, indent=4)

    # 기존:md_filename = f"results/report_{timestamp}.md"
    # 변경: 입력받은 날짜를 활용한 표준 파일명 규약 적용
    date_str = travel_date.replace("-", "") 
    md_filename = f"results/result_{date_str}.md"
    json_filename = f"results/raw_{date_str}.json"

    # 에러 요약 정보 생성
    error_summary = {
        "total_errors": len(errors),
        "error_list": [str(e) for e in errors],
        "status": "SUCCESS" if not errors else "PARTIAL_SUCCESS"
    }

    # 최종 데이터 구조화
    raw_data = {
        "metadata": {
            "target_date": travel_date,
            "generated_at": datetime.now().isoformat()
        },
        "recommendation": plan_data,
        "restaurants": restaurants,
        "error_summary": error_summary  # 요약 필드 추가
    }

    # JSON 저장 (원본 데이터)
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(plan_data, f, ensure_ascii=False, indent=4)

    # Markdown 저장
    with open(md_filename, "w", encoding="utf-8") as f:
        f.write(report_md)

    print("\n" + "="*30)
    print("✅ 작업 완료! (표준 파일명/메타 규약 적용)") # 문구 수정
    print(f"- 원본 데이터: {json_filename}")
    print(f"- 여행 리포트: {md_filename}")
    print("="*30)

if __name__ == "__main__":
    main()