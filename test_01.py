import streamlit as st
import pandas as pd
import re
import ast

# Define a safe version of ast.literal_eval
def safe_literal_eval(val):
    if pd.isnull(val):
        return []  # Return an empty list if the value is NaN
    if isinstance(val, str):
        try:
            return ast.literal_eval(val)
        except (ValueError, SyntaxError):
            return []  # Return an empty list if parsing fails
    elif isinstance(val, list):
        return val  # If it's already a list, return it as is
    else:
        return []  # For any other type, return an empty list


# Streamlit UI 설정
st.title('Thought 문장유사도평균에 따른 이야기 선택')

# 어떤 데이터를 불러오는지 확인할 드롭다운 메뉴 생성
data_select = st.selectbox('데이터를 선택해주셈', ['c2d2_0924_final.csv', 'annotated_change.csv', 'meta0911.csv'])

# 데이터 불러오기
df = pd.read_csv(f"data/{data_select}")

# 데이터프레임에서 'Distorted part'가 문자열 내 리스트로 저장되어 있는 경우 ex) '[텍스트]' -> 리스트로 변환
# df['Distorted part'] = df['Distorted part'].apply(ast.literal_eval)
df['Distorted part'] = df['Distorted part'].apply(safe_literal_eval)

# 데이터프레임에서 'Thought_문장유사도평균'이 숫자형이 아닌 경우 처리
df['Distorted_문장유사도평균'] = pd.to_numeric(df['Distorted_문장유사도평균'], errors='coerce')

# NaN 값 제거 및 Thought_문장유사도평균 오름차순 정렬
df_sorted = df.dropna(subset=['Distorted_문장유사도평균']).sort_values(by='Distorted_문장유사도평균', ascending=True)

# 드롭다운 메뉴에 표시할 항목 생성 (Distorted part 앞부분 + Thought_문장유사도평균)
# df_sorted['Dropdown_label'] = df_sorted['Distorted part'].apply(lambda x: x[0][:30] + '...' if len(x[0]) > 30 else x[0]) + ' (' + df_sorted['Distorted_문장유사도평균'].astype(str) + ')'
# 드롭다운 메뉴에 표시할 항목 생성 (Distorted part 앞부분 + Thought_문장유사도평균)
df_sorted['Dropdown_label'] = df_sorted['Distorted part'].apply(
    lambda x: (x[0][:30] + '...' if len(x[0]) > 30 else x[0]) if len(x) > 0 else 'No Distortion Part'
) + ' (' + df_sorted['Distorted_문장유사도평균'].astype(str) + ')'


# 드롭다운 메뉴 생성
selected_value = st.selectbox('Select a story based on Distorted part and Distorted_문장유사도평균:', df_sorted['Dropdown_label'].unique())

# 선택한 항목에 해당하는 행 가져오기
selected_row = df_sorted[df_sorted['Dropdown_label'] == selected_value].iloc[0]

# 선택된 이야기 및 세부 정보 표시
st.subheader("Selected Story 정보")
st.write("**Story:**", selected_row['story'])
st.write("**Distorted part:**", selected_row['Distorted part'])
st.write("**Label:**", selected_row['label'])
st.write("**Distorted_문장분리:**", selected_row['Distorted_문장분리'])
st.write("**Distorted_문장유사도:**", selected_row['Distorted_문장유사도'])
st.write("**Distorted_문장유사도평균:**", selected_row['Distorted_문장유사도평균'])
if data_select == 'annotated_change.csv':
    st.write("**기존데이터_SecondaryDistortion:**", selected_row['기존데이터_SecondaryDistortion'])
elif data_select == 'c2d2_0924_final.csv':
    st.write("**기존데이터_scenario:**", selected_row['기존데이터_scenario'])
    st.write("**기존데이터_thought:**", selected_row['기존데이터_thought'])
elif data_select == 'meta0911.csv':
    st.write("**persona:**", selected_row['persona'])

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