import time

import streamlit as st

import numpy as np
import pandas as pd
import re
from io import StringIO, BytesIO

def process_excel_data(byte_data):
    # 將二進制數據轉換為BytesIO對象
    excel_data = BytesIO(byte_data)

    # 讀取 Excel 檔案
    df = pd.read_excel(excel_data, engine='openpyxl')
    # 取得所有欄位名稱
    all_columns = df.columns
    st.write ("嘗試解析Excel的內容初始化網頁....請稍等....")
    #progress_bar = st.sidebar.progress(0)
    # 用於存放使用者設置的數據
    user_settings = {}

    # 遍歷每個欄位，讓使用者設置
    for column in all_columns:
        st.header(f"設置 {column}")

        # 為每個 selectbox 提供唯一的 key
        selectbox_key = f"{column}_selectbox"
        input_type = st.selectbox(f"選擇輸入元件類型 - {column}",
                                  ["Checkbox", "Radio", "Selectbox", "Multiselect", "Slider", "Number Input",
                                   "Text Input","Date Input","Time Input","File Uploader"], key=selectbox_key)

        # 取得每個欄位的前5個非空值作為範例參考
        example_values = df[column].dropna().head(5).tolist()
        example_values_str = ", ".join(map(str, example_values))

        # 為每個 text_input 提供唯一的 key
        text_input_key = f"{column}_text_input"
        default_value = st.text_input(f"輸入初始值 - {column}", key=text_input_key, help=f"範例：{example_values_str}")
        st.write(example_values_str)
        # 存入使用者設置的數據
        user_settings[column] = {"輸入元件類型": input_type, "初始值": default_value}


    #progress_bar.progress(i)
    # 將處理後的數據轉換為新的 Excel 檔案
    #user_settings
    return user_settings

st.set_page_config(page_title="Excel Input Validation", page_icon="🌍")
st.markdown("# Excel Input Demo")
st.sidebar.header("Excel 轉換輸入展示")
st.write(
    """這是個展示如何透過excel格式輸入來產生輸入介面的範例。\n"""
    """**👈 請放入要讀取的Excel檔案。**"""
)

uploaded_file = st.sidebar.file_uploader("請上傳Excel格式檔案")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    result_byte_data = process_excel_data(bytes_data)
    all_inputs_selected = all(value["輸入元件類型"] and value["初始值"] for value in result_byte_data.values())
    if st.button("確認", disabled=not all_inputs_selected):
        output_excel = BytesIO()
        output_df = pd.DataFrame(result_byte_data).T
        output_df.to_excel(output_excel, index=False, engine='openpyxl')
        # 取得最終的二進制數據
        output_excel_data = output_excel.getvalue()
        st.download_button(
            label="Download data as Excel",
            data=output_excel_data,
            file_name='Web_Input_設定檔案.xlsx',
            mime='Excel/xlsx',
        )