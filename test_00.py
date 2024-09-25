import streamlit as st
import pandas as pd
import re
import ast

# 데이터 불러오기
df = pd.read_csv("data/c2d2_0924_final.csv")
df['Distorted part'] = df['Distorted part'].apply(ast.literal_eval)

# Streamlit UI 설정
st.title('Thought 문장유사도평균에 따른 이야기 선택')

# 데이터프레임에서 'Thought_문장유사도평균'이 숫자형이 아닌 경우 처리
df['Thought_문장유사도평균'] = pd.to_numeric(df['Thought_문장유사도평균'], errors='coerce')

# NaN 값 제거 및 Thought_문장유사도평균 오름차순 정렬
df_sorted = df.dropna(subset=['Thought_문장유사도평균']).sort_values(by='Thought_문장유사도평균', ascending=True)

# Thought_문장유사도평균을 기준으로 드롭다운 메뉴 생성
selected_value = st.selectbox('Select a story based on Thought_문장유사도평균:', df_sorted['Thought_문장유사도평균'].unique())

# 선택한 평균 유사도에 해당하는 행 가져오기
selected_row = df_sorted[df_sorted['Thought_문장유사도평균'] == selected_value].iloc[0]

# 선택된 이야기 및 세부 정보 표시
st.subheader("Selected Story 정보")
st.write("**Story:**", selected_row['story'])
st.write("**Distorted part:**", selected_row['Distorted part'])
st.write("**Label:**", selected_row['label'])
st.write("**원데이터_scenario:**", selected_row['원데이터_scenario'])
st.write("**원데이터_thought:**", selected_row['원데이터_thought'])
st.write("**Thought_문장분리:**", selected_row['Thought_문장분리'])
st.write("**Thought_문장유사도:**", selected_row['Thought_문장유사도'])
st.write("**Thought_문장유사도평균:**", selected_row['Thought_문장유사도평균'])

# 하이라이트
st.subheader("Selected Story 하이라이트")

# 하이라이트할 텍스트와 story를 연결하는 함수
def highlight_text(story, find_list, highlight_color):
    highlighted_story = story
    if isinstance(find_list, str):
        find_list = [find_list]  # 문자열을 리스트로 변환
    for long_text in find_list:
        if long_text in story:
            # 하이라이트 처리를 위해 HTML로 감싸기 (색상 지정)
            highlighted_story = re.sub(re.escape(long_text), f'<mark style="background-color: {highlight_color};">{long_text}</mark>', highlighted_story, flags=re.IGNORECASE)
    return highlighted_story

# 하이라이트 색상 지정
highlight_color = st.color_picker('Pick a highlight color for this story', '#ffcc00')  # 기본 색상은 노란색

# 하이라이트된 story 표시
highlighted_story = highlight_text(selected_row['story'], selected_row['Distorted part'], highlight_color)
st.markdown(highlighted_story, unsafe_allow_html=True)

