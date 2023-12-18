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
    #df = pd.read_excel(excel_data, engine='openpyxl')
    meta_data_df = pd.read_excel(excel_data, sheet_name="Meta Data")
    data_df = pd.read_excel(excel_data, sheet_name="Data")
    st.write ("嘗試解析Excel的格式要求....請稍等....")
    progress_bar = st.sidebar.progress(0)
    # 假設 your_custom_function 是你用來處理最後一欄資料的自訂函數
    # 你可以在這裡自行定義 your_custom_function

    # 遍歷 Meta Data 中的每一列，根據類型生成對應的輸入元件
    for index, row in meta_data_df.iterrows():
        column_name = row['欄位名稱']
        input_type = row['類型']

        if input_type == 'Checkbox':
            default_value = data_df[column_name].iloc[0]
            data_df[column_name] = st.checkbox(column_name, default=default_value)
        elif input_type == 'Dropdown':
            options = data_df[column_name].unique()
            default_value = data_df[column_name].iloc[0]
            data_df[column_name] = st.selectbox(column_name, options=options,
                                                index=options.tolist().index(default_value))
        elif input_type == 'NumericInput':
            default_value = data_df[column_name].iloc[0]
            data_df[column_name] = st.number_input(column_name, value=default_value)
        elif input_type == 'TextInput':
            default_value = data_df[column_name].iloc[0]
            data_df[column_name] = st.text_input(column_name, value=default_value)

    # 顯示動態生成的數據
    st.write("Generated Data:")
    st.write(data_df)
    progress_bar.progress(i)
    # 將處理後的數據轉換為新的 Excel 檔案
    output_excel = BytesIO()
    df.to_excel(output_excel, index=False, engine='openpyxl')

    # 取得最終的二進制數據
    output_excel_data = output_excel.getvalue()

    return output_excel_data

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
    st.download_button(
        label="Download data as Excel",
        data=result_byte_data,
        file_name='large_df.xlsx',
        mime='Excel/xlsx',
    )