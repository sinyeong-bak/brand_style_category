# 🧵 브랜드 무드 기반 유사도 그래프

## 📝 프로젝트 개요  
브랜드별 `main_mood`, `sub_mood_1`, `sub_mood_2` 데이터를 기반으로  
각 브랜드의 스타일 성향을 **가중치 기반 벡터**로 변환하고,  
`cosine similarity`를 활용해 **브랜드 간 유사도**를 계산합니다.  
이를 바탕으로 `networkx`를 사용해 **무드 중심 브랜드 유사도 그래프**를 구성하고 시각화합니다.

---

## 💡 핵심 기능
- 브랜드 무드 정보를 가중치 기반 multi-hot 벡터로 변환
- cosine similarity를 활용한 브랜드 간 유사도 산출
- 유사도 임계값(Threshold)을 기준으로 edge 생성
- 무드 유형에 따라 브랜드를 컬러 노드로 시각화

---

## 🧩 사용 기술

| 패키지 | 역할 |
|--------|------|
| `pandas`, `numpy` | 데이터 처리 및 벡터 생성 |
| `sklearn.metrics.pairwise.cosine_similarity` | 유사도 계산 |
| `networkx` | 그래프 생성 |
| `matplotlib` | 네트워크 시각화 |

## 📁 파일 구성

📦브랜드_무드_유사도_그래프/
 ┣ 📄 brand_mood_graph.py         # 전체 코드
 ┣ 📄 requirements.txt            # 필요한 패키지 목록
 ┗ 📄 README.md                   # 프로젝트 소개 파일 (바로 이 파일!)

## 🔍 주요 코드 예시

```python
# 브랜드 무드 벡터 생성
def create_mood_vector(row, moods):
    vector = np.zeros(len(moods))
    if row['main_mood'] in moods:
        vector[moods.index(row['main_mood'])] = 3
    if row['sub_mood_1'] in moods:
        vector[moods.index(row['sub_mood_1'])] = 2
    if row['sub_mood_2'] in moods:
        vector[moods.index(row['sub_mood_2'])] = 1
    return vector

