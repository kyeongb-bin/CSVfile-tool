import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 페이지 설정
st.set_page_config(page_title="CSV 데이터 시각화", layout="wide")

# 제목
st.title("CSV 데이터 시각화 대시보드")

# 파일 업로더
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=['csv'])

if uploaded_file is not None:
    # 데이터 읽기
    df = pd.read_csv(uploaded_file)
    
    # 데이터 미리보기
    st.subheader("데이터 미리보기")
    st.dataframe(df.head())
    
    # 컬럼 선택
    columns = df.columns.tolist()
    x_column = st.selectbox("X축 선택", columns)
    y_column = st.selectbox("Y축 선택", columns)
    
    # 그래프 그리기
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df, x=x_column, y=y_column)
    st.pyplot(fig)