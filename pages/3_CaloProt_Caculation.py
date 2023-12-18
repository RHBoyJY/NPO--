import streamlit as st

# 設置網頁標題
st.title('熱量與蛋白質需求計算器')

# 輸入使用者數據
weight = st.number_input('請輸入您的體重（公斤）', min_value=0.0, step=0.1, format='%.1f')

# 定義選項清單
calories_options = [20, 25, 30, 35, 40]
protein_options = [1.2, 1.5, 1.8, 2.0, 2.2]

# 使用者選擇或輸入每公斤體重所需大卡
calories_per_kg = st.select_slider('選擇或輸入每公斤體重所需的大卡', options=calories_options, value=25)
protein_per_kg = st.select_slider('選擇或輸入每公斤體重所需的蛋白質（公克）', options=protein_options, value=1.8)

# 計算總熱量需求並進行四捨五入
total_calories = round(weight * calories_per_kg, -2)  # 四捨五入到最接近的100大卡
# 計算總蛋白質需求並進行四捨五入
total_protein = round(weight * protein_per_kg)

# 顯示結果
st.write(f'根據體重 {weight} 公斤，您的總熱量需求為：{total_calories} 大卡')
st.write(f'您的總蛋白質需求為：{total_protein} 公克')