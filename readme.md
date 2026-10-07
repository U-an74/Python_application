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
KAKAO_REST_API_KEY=your_kakao_api_key_here
```
프로젝트 루트 폴더에 .env 파일을 생성하고, 본인의 API 키 포함하는 핵심 코드를 작성하세요.
.env(example) 파일의 형식을 참조하면 편리합니다. 

🔒 **보안 주의 사항**

.env 파일은 API 키와 같은 민감한 정보를 담고 있습니다.
이 파일이 GitHub과 같은 공용 저장소에 업로드되지 않도록 .gitignore 파일에 .env가 포함되어 있는지 반드시 확인하세요.
실수로 키가 유출되었다면 즉시 해당 서비스 사이트에서 키를 삭제하고 재발급받으세요.

### 4. 프로그램 실행(Usage)

이 프로그램은 명령행 인터페이스(CLI)를 통해 실행됩니다. `-d` 또는 `--date` 옵션을 사용하여 여행 날짜를 지정해야 합니다.


```bash
# 기본 실행 형식
python main.py --date YYYY-MM-DD

# 실행 예시-1(기본)
python main.py --date 2026-11-10

# 실행 예시-2(짧은 별칭 옵션)
python main.py -d 2026-11-10
```

❔**자동 안내 기능** 

옵션이 기억나지 않는 경우, 아래 명령어를 통해 도움말을 확인할 수 있습니다. 

```bash
python main.py --help
```


## 📂 프로젝트 구조
- main.py: 프로그램 실행 메인 로직
- llm_handler.py: OpenAI API 연동 및 프롬프트 관리
- kakao_handler.py: 카카오 검색 API 연동 및 데이터 처리
- requirements.txt: 필수 라이브러리 목록
- results/: 생성된 여행 추천 리포트가 저장되는 폴더
- .env: API 키 보안 관리
- .gitignore: GitHub에 올리지 않을 파일 목록 설정


## 📄 결과물 예시
- 실행이 완료되면 results/ 폴더 내에 여행추천_YYYYMMDD_HHMMSS.md 형태로 결과가 저장됩니다.(results/sample_result.md 참조)

- 결과물 구조
  1. 추천 지역 요약(지역명, 추천 이유)
  2. 날씨 정보
  3. 행사 / 축제
  4. 맛집 리스트
  5. 1일 일정 제안
  6. 추천 포인트

- 결과물 화면 캡처 (입력/요청: --date 2026-11-10)  
<img width="1220" height="515" alt="image" src="https://github.com/user-attachments/assets/66f258af-fa46-46d8-9421-eb21922b802d" />
<img width="1116" height="457" alt="image (1)" src="https://github.com/user-attachments/assets/49a4c594-845e-40fd-b89c-ba4c5c106064" />
<img width="1092" height="770" alt="image (2)" src="https://github.com/user-attachments/assets/15753043-afad-41d5-bdd8-eb8bbf6a3e82" />



## 🧠 Technical Insights
- 1. HTTP 메서드 활용 및 설계 이유 (GET vs POST)
각 API의 특성에 맞춰 적절한 HTTP 메서드를 선택하여 설계했습니다.

| API 종류 | 메서드 | 엔드포인트 (Example) | 설계 이유 |
| :--- | :---: | :--- | :--- |
| **Kakao Local** | **GET** | `/v2/local/search/keyword.json` | 특정 키워드를 기반으로 장소 정보를 **조회(Retrieve)**하는 것이 목적이며, 검색 파라미터를 URL에 포함하여 전달하는 RESTful 원칙을 준수합니다. |
| **OpenAI** | **POST** | `/v1/chat/completions` | 프롬프트와 같은 **대량의 데이터**를 전송하여 새로운 응답을 **생성(Create)**해야 하며, 보안이 필요한 데이터와 설정을 Body에 담아 안전하게 전달합니다. |

- 2. 데이터 구조화 및 파이프라인 구축
비정형 텍스트를 출력하는 LLM의 결과를 JSON 형식으로 구조화하도록 프롬프트를 설계했습니다.

이점: json.loads()를 통해 즉시 파이썬 객체로 변환할 수 있어 데이터 처리가 용이합니다.
자동화: 추출된 place_name을 카카오 검색 API의 입력값으로 즉시 연결하는 데이터 파이프라인을 구현하여 사용자 개입 없는 자동화 흐름을 완성했습니다.

- 3. 예외 처리 및 디버깅 가이드
프로그램의 안정성을 높이기 위해 단계별 예외 처리 전략을 수립했습니다.

보안 및 인증: .env 파일로 API 키를 관리하여 유출을 방지합니다.
데이터 파싱: LLM 응답이 유효한 JSON 형식이 아닐 경우를 대비해 try-except 문으로 예외를 처리하고 사용자에게 재시도를 안내합니다.
네트워크 및 쿼터 (401/403/429 에러 대응):
401 (Unauthorized): API 키가 유효한지, .env 파일에 오타가 없는지 점검합니다.
403 (Forbidden): Kakao Developers 설정에서 'Web 플랫폼 도메인(http://localhost)' 등록 여부를 확인합니다.
429 (Too Many Requests): API 호출 할당량(Quota) 초과 여부를 대시보드에서 확인합니다.
디버깅 절차: 에러 발생 시 response.status_code와 에러 메시지를 로그로 출력하여 원인을 즉시 파악할 수 있도록 구현했습니다.


## ## 🚀 운영 및 고도화 전략

### 1. 운영 환경 비밀관리
- **CI/CD 연동**: GitHub Actions 사용 시 `Settings > Secrets and variables`에 API 키를 등록하여 소스코드 노출 없이 빌드 및 배포를 수행합니다.
- **Cloud Secrets Manager**: 실제 운영 환경(AWS, GCP 등)에서는 AWS Secrets Manager나 HashiCorp Vault를 연동하여 런타임에 안전하게 키를 주입받는 방식을 권장합니다.

### 2. LLM 재요청 및 프롬프트 보강
- **보강 전략**: 1차 응답 파싱 실패 시, 재요청 프롬프트에 **"이전 응답에서 JSON 형식이 누락되었습니다. 반드시 { ... } 외의 텍스트는 제외하고 출력하세요."**라는 강제 문구를 추가하여 응답의 정확도를 높입니다.
- **파싱 보정**: 정규표현식을 사용하여 JSON 블록(` ```json ... ``` `)만 추출하는 전처리 로직을 강화했습니다.

### 3. 검색 결과 0건 발생 시 대체
- **대체 검색**: 특정 맛집 검색 결과가 0건일 경우, 검색 범위를 넓혀 해당 도시의 '랜드마크'나 '대표 관광지'로 자동 재검색을 수행합니다.
- **통계 로깅**: 0건 발생 빈도를 `logs/zero_results.log`에 기록하여 향후 LLM의 추천 키워드 적절성을 분석하는 지표로 활용합니다.

### 4. 날짜 기반 캐싱 정책
- **캐싱 메커니즘**: 동일 날짜(`--date`)에 대한 요청은 `results/cache_{date}.json` 파일 존재 여부를 먼저 확인하여 API 호출 없이 결과를 재사용합니다.
- **만료 정책**: 여행 정보의 특성을 고려하여 **7일**간 유효한 캐시 정책을 유지하며, 이후에는 새로운 데이터를 갱신하도록 설계합니다.

### 5. 도시명 정규화 로직
- **표준화**: 사용자가 입력한 '서울시', '서울역 근처', '부산광역시' 등을 '서울', '부산' 등 표준 지명으로 매핑하는 정규화 과정을 거칩니다.
- **키워드 정제**: 불필요한 수식어나 오타를 제거하여 카카오 API 검색 성공률을 극대화합니다.