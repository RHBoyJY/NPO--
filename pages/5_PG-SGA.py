import streamlit as st

# 標題
st.title('PG-SGA營養狀態評估表')

# 表單開始
with st.form(key='pgsga_form'):
    # 使用者輸入目前體重
    current_weight = st.number_input('請輸入您目前的體重（公斤）', min_value=0.0, step=0.1, format='%.1f')
    
    st.subheader('1. 體重變化')
    weight_one_month_ago = st.number_input('請輸入一個月前的體重（公斤，若無則留空）', min_value=0.0, step=0.1, format='%.1f', value=0.0)
    weight_six_months_ago = st.number_input('請輸入六個月前的體重（公斤，僅在無一個月前體重時填寫）', min_value=0.0, step=0.1, format='%.1f', value=0.0)
    weight_change_2_week = st.radio('過去2週體重變化', ['增加', '減少', '未變'])

    
    st.subheader('2. 食物攝入')
    food_intake_past_month = st.radio('過去一個月食物攝入', ['正常', '減少', '增加'])
    food_type_intake = st.radio('實際食物攝入類型', ['正常但少於平常', '少量固體食物', '只攝入液體', '只攝入營養補充品', '非常少', '只有管餵或靜脈注射'])
    
    st.subheader('3. 影響進食的症狀 在過去兩周內，我有以下問題，這些問題讓我無法吃足夠的食物（請選所有適用的選項）')
    symptoms = {
        '沒有飲食方面的問題': 0,
        '沒有食欲，就是不想吃':3,
        '嘔吐':3,
        '噁心':1,
        '腹瀉':3,
        '便祕':1,
        '口乾':1,
        '口腔潰瘍':2,
        '有怪味困擾我':1,
        '吃起來感覺沒有味道，或味道覺得奇怪':1,
        '感覺比較快飽':1,
        '吞嚥困難':2,
        '疲倦':1,
        '疼痛':3,
        '其他(抑鬱、金錢或牙齒問題)':1,
        # 其他症狀按照圖片中的分數添加
    }
    symptoms_selected = st.multiselect('選擇過去兩週內的症狀', list(symptoms.keys()))
    
    st.subheader('4. 活動與功能')
    activity_level = st.radio('過去一個月的活動水平', ['正常無限制', '不如平常', '大部分時間躺或坐', '幾乎整天都在床或椅子上', '幾乎一直臥床'])

    # 提交按鈕
    submit_button = st.form_submit_button(label='計算PG-SGA分數')

# 計算分數
if submit_button:
    # 體重變化百分比計算
    weight_change_percentage = 0
    weight_change_percentage_in_sixmonth = 0
    if weight_one_month_ago > 0:
        weight_change_percentage = ((current_weight - weight_one_month_ago) / weight_one_month_ago) * 100
    elif weight_six_months_ago > 0:
        weight_change_percentage_in_sixmonth = ((current_weight - weight_six_months_ago) / weight_six_months_ago) * 100
    # 根據百分比決定分數
    weight_score = 0
    
    if weight_change_percentage >= 10:
        weight_score = 4
    elif weight_change_percentage >= 5.0:
        weight_score = 3
    elif weight_change_percentage >= 3.0:
        weight_score = 2
    elif weight_change_percentage >= 2.0:
        weight_score = 1
    elif weight_change_percentage == 0:
        if weight_change_percentage_in_sixmonth >= 20:
            weight_score = 4    
        elif weight_change_percentage_in_sixmonth >= 10.0:
            weight_score = 3    
        elif weight_change_percentage_in_sixmonth >= 6.0:
            weight_score = 2
        elif weight_change_percentage_in_sixmonth >= 2.0:
            weight_score = 1

    weight_score += 1 if weight_change_2_week == '減少' else 0
    # 食物攝入分數計算
    food_intake_score = 0
    if food_intake_past_month == '減少':
        food_intake_score = 1
    elif food_intake_past_month == '增加':
        food_intake_score = 0
    else: # '正常'
        food_intake_score = 0
    # 根据食物类型给分
    food_type_score = 0
    if food_type_intake == '正常但少於平常':
        food_type_score = 1
    elif food_type_intake == '少量固體食物':
        food_type_score = 2
    elif food_type_intake == '只攝入液體':
        food_type_score = 3
    elif food_type_intake == '只攝入營養補充品':
        food_type_score = 3
    elif food_type_intake == '非常少':
        food_type_score = 4
    elif food_type_intake == '只有管餵或靜脈注射':
        food_type_score = 0
    # 取最高分
    food_intake_total_score = max(food_intake_score, food_type_score)

    # 症狀分數計算
    symptoms_score = sum(symptoms[symptom] for symptom in symptoms_selected)

    # 活動與功能分數計算
    activity_scores = {
        '正常無限制': 0,
        '不如平常': 1,
        '大部分時間躺或坐': 2,
        '幾乎整天都在床或椅子上': 3,
        '幾乎一直臥床': 3,
    }
    activity_score = activity_scores[activity_level]

    # 總分計算
    total_score = weight_score + food_intake_total_score + symptoms_score + activity_score

    # 顯示結果
    st.subheader('PG-SGA總分')
    st.write(f'您的PG-SGA總分是: {total_score}')