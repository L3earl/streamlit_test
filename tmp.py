import streamlit as st
import pandas as pd
import re
import ast

# Streamlit UI 설정
# st.title('Thought 문장유사도평균에 따른 이야기 선택')

# 어떤 데이터를 불러오는지 확인할 드롭다운 메뉴 생성
# data_select = st.selectbox('데이터를 선택해주셈', ['c2d2_0924_final.csv', 'annotated_change.csv'])

# 데이터 불러오기
df = pd.read_csv(f"data/c2d2_0924_final.csv")

# 데이터프레임에서 'Distorted part'가 문자열 내 리스트로 저장되어 있는 경우 ex) '[텍스트]' -> 리스트로 변환
df['Distorted part'] = df['Distorted part'].apply(ast.literal_eval)

# 데이터프레임에서 'Thought_문장유사도평균'이 숫자형이 아닌 경우 처리
df['Distorted_문장유사도평균'] = pd.to_numeric(df['Distorted_문장유사도평균'], errors='coerce')


empty_list_rows = df[df['Distorted part'].apply(lambda x: isinstance(x, list) and len(x) == 0)]
empty_list_rows