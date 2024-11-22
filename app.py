import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
import os
from openai import OpenAI

# 환경변수 로드
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_visualization_recommendation(df):
    # 데이터셋 정보 생성
    data_info = f"""
    데이터셋 정보:
    - 컬럼 목록: {df.columns.tolist()}
    - 데이터 타입: {df.dtypes.to_dict()}
    - 수치형 컬럼 통계: {df.describe().to_dict()}
    
    이 데이터를 시각화하기 위한 최적의 그래프 유형과 사용할 컬럼을 추천해주세요.
    답변 형식:
    1. 추천 그래프:
    2. X축 추천:
    3. Y축 추천:
    4. 추천 이유:
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 데이터 시각화 전문가입니다."},
                {"role": "user", "content": data_info}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"API 호출 중 오류 발생: {str(e)}"

# 페이지 설정
st.set_page_config(page_title="CSV 데이터 시각화", layout="wide")

# 제목
st.title("CSV 데이터 시각화 대시보드")

# 파일 업로더
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=['csv'])

if uploaded_file is not None:
    # 데이터 읽기
    df = pd.read_csv(uploaded_file)
    
    # AI 추천 받기
    if st.button("AI 시각화 추천 받기"):
        recommendation = get_visualization_recommendation(df)
        st.subheader("AI 추천 시각화")
        st.write(recommendation)
    
    # 데이터 미리보기
    st.subheader("데이터 미리보기")
    st.dataframe(df.head())
    
    # 시각화 옵션
    chart_type = st.selectbox("그래프 종류 선택", 
        ["산점도", "선 그래프", "막대 그래프", "히스토그램", "박스플롯", "히트맵"])
    
    # 컬럼 선택
    columns = df.columns.tolist()
    x_column = st.selectbox("X축 선택", columns)
    y_column = st.selectbox("Y축 선택", columns)
    
    # 그래프 그리기
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if chart_type == "산점도":
        sns.scatterplot(data=df, x=x_column, y=y_column)
    elif chart_type == "선 그래프":
        plt.plot(df[x_column], df[y_column])
    elif chart_type == "막대 그래프":
        sns.barplot(data=df, x=x_column, y=y_column)
    elif chart_type == "히스토그램":
        plt.hist(df[x_column])
    elif chart_type == "박스플롯":
        sns.boxplot(data=df, x=x_column, y=y_column)
    elif chart_type == "히트맵":
        sns.heatmap(df.corr(), annot=True)
    
    plt.title(f"{chart_type}: {x_column} vs {y_column}")
    st.pyplot(fig)