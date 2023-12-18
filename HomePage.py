import time

import streamlit as st

import numpy as np
import pandas as pd
import re
from io import StringIO, BytesIO
st.set_page_config(
    page_title="Excel tool box",
    page_icon="👋",
)
def find_header_location(df):
    # 尋找標題所在的位置，這裡簡單示範在每行每列中找到第一個不為空的單元格作為標題位置
    for index, row in df.iterrows():
        for col_index, value in enumerate(row):
            if pd.notna(value):
                return index, col_index
    return None, None

def process_excel_data(byte_data):
    # 將二進制數據轉換為BytesIO對象
    excel_data = BytesIO(byte_data)

    # 讀取 Excel 檔案
    df = pd.read_excel(excel_data, engine='openpyxl')

    # 分析最後一欄的資料
    last_column_name = df.columns[-1]
    df['New_Column'] = df[last_column_name].apply(lambda x: extract_bullet_points(x))

    # 假設 your_custom_function 是你用來處理最後一欄資料的自訂函數
    # 你可以在這裡自行定義 your_custom_function

    # 將處理後的數據轉換為新的 Excel 檔案
    output_excel = BytesIO()
    df.to_excel(output_excel, index=False, engine='openpyxl')

    # 取得最終的二進制數據
    output_excel_data = output_excel.getvalue()

    return output_excel_data


def extract_bullet_points(text):
    # 利用正則表達式找到以"A："為開頭的句子，並將其分割成要點
    points = re.split(r'目的：', text)[1:]

    # 清理要點中的空格和換行符號
    points = [point.strip() for point in points]

    return points

st.title('這是測試用的網頁')

st.markdown(
        """
        This is an open-source program for NGO/NPO project 
        **👈 Select a function from the sidebar** to process the Excel by Click the mouse!
        ### Function Explanation for understanding
        - Function 1: ExcelCompare - Compare the second excel columns with the first excel columns, 
                         to list the difference cloumns number and items. 
                         YOu can also download excel file to have the excel format for following processing.
        - Function 2: KeywordFinding - under development. 
    """
)

