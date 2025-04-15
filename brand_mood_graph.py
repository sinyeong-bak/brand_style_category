import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity

# 데이터 준비
data = {
    "브랜드명": ["라무스튜디오", "니즈르", "올리브 데 올리브", "아틀리에 나인",
                "프리터", "플라스크", "준준스페이스", "던드롬",
                "페이탈고스트", "제뉴즈", "비나이스", "논플로어",
                "타일레", "아이언스탠드", "론트", "롤링스튜디오",
                "스토리요가", "발리안트", "디터민드", "테일러메이드 어패럴"],
    "main_mood": ["클래식", "걸리시", "클래식", "미니멀",
                 "캐주얼", "시크", "걸리시", "로맨틱",
                 "스트릿", "캐주얼", "캐주얼", "캐주얼",
                 "미니멀", "시크", "클래식", "캐주얼",
                 "스포티", "스포티", "스포티", "스포티"],
    "sub_mood_1": ["캐주얼", "캐주얼", "로맨틱", "클래식",
                  "걸리시", "캐주얼", "캐주얼", "걸리시",
                  "캐주얼", "걸리시", "", "스트릿",
                  "시크", "캐주얼", "미니멀", "미니멀",
                  "에스닉", "캐주얼", "캐주얼얼", "클래식"],
    "sub_mood_2": ["", "로맨틱", "미니멀", "로맨틱",
                  "스트릿", "미니멀", "로맨틱", "",
                  "", "워크웨어", "", "",
                  "캐주얼", "", "캐주얼", "클래식",
                  "", "스트릿", "", ""]
}

# DataFrame 생성
df = pd.DataFrame(data)

# 모든 무드 목록 추출 및 정리
all_moods = set()
for col in ['main_mood', 'sub_mood_1', 'sub_mood_2']:
    all_moods.update(df[col].unique())
all_moods = sorted([mood for mood in all_moods if mood != ''])  # 빈 문자열 제거

# Multi-hot 벡터화 함수 정의
def create_mood_vector(row, moods):
    vector = np.zeros(len(moods))

    # main_mood는 가중치 2 부여
    if row['main_mood'] in moods:
        vector[moods.index(row['main_mood'])] = 3

    # sub_mood_1은 가중치 1 부여
    if row['sub_mood_1'] in moods and row['sub_mood_1'] != '':
        vector[moods.index(row['sub_mood_1'])] = 2

    # sub_mood_2는 가중치 1 부여
    if row['sub_mood_2'] in moods and row['sub_mood_2'] != '':
        vector[moods.index(row['sub_mood_2'])] = 1

    return vector

# 각 브랜드를 벡터로 변환
brand_vectors = np.array([create_mood_vector(row, all_moods) for _, row in df.iterrows()])

# 코사인 유사도 계산
similarity_matrix = cosine_similarity(brand_vectors)

# 네트워크 그래프 생성
G = nx.Graph()

# 노드 추가
for i, brand in enumerate(df['브랜드명']):
    G.add_node(brand, mood=df.iloc[i]['main_mood'])

# 에지 추가 (유사도 임계값 설정)
threshold = 0.3  # 유사도 임계값
for i in range(len(df)):
    for j in range(i+1, len(df)):
        if similarity_matrix[i][j] > threshold:
            G.add_edge(df.iloc[i]['브랜드명'], df.iloc[j]['브랜드명'],
                       weight=similarity_matrix[i][j])

# 무드별 색상 매핑
mood_colors = {
    "클래식": "#e74c3c",  # 빨강
    "캐주얼": "#3498db",  # 파랑
    "걸리시": "#2ecc71",  # 초록
    "로맨틱": "#f39c12",  # 주황
    "미니멀": "#9b59b6",  # 보라
    "시크": "#e84393",    # 핑크
    "스트릿": "#6c5ce7",  # 남색
    "스포티": "#00cec9",  # 청록
    "에스닉": "#fdcb6e",  # 노랑
    "워크웨어": "#d35400", # 갈색
    "캐주얼얼": "#3498db"  # 캐주얼과 동일한 색상 사용
}

# 노드 색상 지정
node_colors = [mood_colors[G.nodes[node]['mood']] for node in G.nodes()]

# 커뮤니티 감지 (그룹화를 위해)
communities = nx.community.louvain_communities(G)
pos = nx.spring_layout(G, k=0.6, seed=42)  # 레이아웃 생성

# 그래프 시각화
plt.figure(figsize=(14, 10))

# 모든 에지 그리기
edge_weights = [G[u][v]['weight'] * 3 for u, v in G.edges()]
nx.draw_networkx_edges(G, pos, width=edge_weights, alpha=0.6, edge_color='gray')

# 노드 그리기
nx.draw_networkx_nodes(G, pos, node_size=700, node_color=node_colors, alpha=0.8)

# 노드 레이블 그리기
nx.draw_networkx_labels(G, pos, font_size=10, font_family='NanumGothic', font_weight='bold')

# 무드별 색상 범례 추가
legend_elements = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color,
                              markersize=10, label=mood)
                   for mood, color in mood_colors.items() if mood in df['main_mood'].unique()]
plt.legend(handles=legend_elements, loc='upper right')

plt.title("브랜드 무드 유사도 네트워크", fontsize=18)
plt.axis('off')
plt.tight_layout()
plt.show()

# 유사도 분석 결과 출력
print("브랜드 간 유사도 분석:")
for i in range(len(df)):
    for j in range(i+1, len(df)):
        if similarity_matrix[i][j] > threshold:
            print(f"{df.iloc[i]['브랜드명']} ↔ {df.iloc[j]['브랜드명']}: {similarity_matrix[i][j]:.2f}")