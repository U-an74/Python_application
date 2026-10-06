# ✈️ 국내 여행지 추천 프로그램 (Travel Recommendation System)

OpenAI의 GPT5.4 모델과 카카오 로컬 rest API를 결합하여, 사용자가 원하는 지역의 여행 계획과 실시간 맛집/명소 정보를 제공하는 파이썬 애플리케이션입니다.

## 🚀 주요 기능
- **LLM 기반 여행 일정 생성**: OpenAI API를 사용하여 사용자의 목적지에 맞는 맞춤형 여행 코스를 제안합니다.
- **실시간 장소 검색**: 카카오 로컬 API를 통해 제안된 장소의 정확한 명칭과 정보를 확인합니다.
- **결과 리포트 저장**: 생성된 여행 일정과 검색 결과를 `results/` 폴더에 마크다운(.md) 및 제이슨(.json) 파일로 자동 저장합니다.
- **CLI 인터페이스**: 터미널에서 날짜와 목적지를 입력받아 간편하게 실행할 수 있습니다. (입력/요청: -date "YYYY-MM-DD")

## 🛠 기술 스택
- **Language**: Python 3.14.7
- **APIs**: OpenAI API, Kakao Local API
- **Libraries**: `python-dotenv`, `requests`, `openai`

## 📦 기본 환경 설정 및 실행 방법

### 1. 저장소 복제
```bash
git clone https://github.com/U-an74/Python_application.git
cd travel-api-project
```

### 2. 필수 라이브러리 설치
```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정
```bash
OPENAI_API_KEY=your_openai_api_key_here
KAKAO_API_KEY=your_kakao_api_key_here
```
프로젝트 루트 폴더에 .env 파일을 생성하고, 본인의 API 키 포함하여 상기 핵심 코드를 작성하세요.
.env(example) 파일의 형식을 참조하면 편리합니다. 

🔒 **보안 주의 사항**
.env 파일은 API 키와 같은 민감한 정보를 담고 있습니다.
이 파일이 GitHub과 같은 공용 저장소에 업로드되지 않도록 .gitignore 파일에 .env가 포함되어 있는지 반드시 확인하세요.
실수로 키가 유출되었다면 즉시 해당 서비스 사이트에서 키를 삭제하고 재발급받으세요.

### 4. 프로그램 실행
```bash
# 기본 실행
python main.py

# 특정 날짜 지정 실행 (옵션)
python main.py --date 2026-11-10
```
## 📂 프로젝트 구조
- main.py: 프로그램 실행 메인 로직
- llm_handler.py: OpenAI API 연동 및 프롬프트 관리
- kakao_handler.py: 카카오 검색 API 연동 및 데이터 처리
- requirements.txt: 필수 라이브러리 목록
- results/: 생성된 여행 추천 리포트가 저장되는 폴더
- .env: API 키 보안 관리
- .gitignore: GitHub에 올리지 않을 파일 목록 설정

### 📄 결과물 예시
실행이 완료되면 results/ 폴더 내에 여행추천_YYYYMMDD_HHMMSS.md 형태로 결과가 저장됩니다.
상세 샘플은 results/sample_result.md 를 참조하세요.
