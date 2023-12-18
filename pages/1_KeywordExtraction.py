import time

import streamlit as st

import numpy as np
import pandas as pd
import re
from io import BytesIO
def extract_chinese_from_pattern(input_string):
    # 使用正規表達式擷取中文+空白+中文的格式
    pattern = r'[\u4e00-\u9fa5]+[^ \t\n\r\f\v]+$'
    match = re.search(pattern, input_string)
    # 如果符合格式，返回最後的中文部分；否則返回原字串
    if match:
         return match.group(0)
    else:
        return input_string

def extract_last_letter_portion(input_string):
    # 使用正規表達式擷取最後的字母部分
    pattern = r'[a-zA-Z\s]+$'
    match = re.search(pattern, input_string)

    # 如果符合格式，返回最後的字母部分；否則返回空字串
    if match:
        return match.group(0)
    else:
        return input_string
        
def extract_key_points(data):
    # 使用正規表達式擷取要點
    pattern = r'(?<!\s)[\u4e00-\u9fa5a-zA-Z\s]+[:：]'
    key_points_match = re.findall(pattern, data)

    # 去除符號，保留純文字要點
    key_points = [re.sub(r'[:：]', '', match) for match in key_points_match]

    # 進一步處理要點，根據最後一個字是中文還是英文，去除前面的中文或英文及空白
    processed_key_points = []
    for key_point in key_points:
        last_char = key_point[-1]
        if last_char.isalpha() and last_char.isascii():  # 最後一個字是英文
            #if key_point == "Glutamine補助 P":
            #     print("最後一個字是英文")
            processed_key_point = extract_last_letter_portion(key_point)
        else:  # 最後一個字是中文
            #if key_point == "Glutamine補助 P":
            #    print("最後一個字是中文")
            processed_key_point = extract_chinese_from_pattern(key_point)
            # processed_key_point = re.sub(r'^[\u4e00-\u9fa5\s]+', '', processed_key_point, count=1)
        processed_key_point=processed_key_point.strip()
        processed_key_points.append(processed_key_point)

    return processed_key_points


def clean_columns(columns):
    # 去除包含 "Unnamed" 的欄位
    cleaned_columns = [col for col in columns if 'Unnamed' not in col]
    return cleaned_columns

def find_header_location(df):
    # 尋找標題所在的位置，這裡簡單示範在每行每列中找到第一個不為空的單元格作為標題位置
    for index, row in df.iterrows():
        for col_index, value in enumerate(row):
            if pd.notna(value):
                return index, col_index
    return None, None

def combine_headers(df1, df2):
    # 獲取第一個檔案的所有 columns
    columns1 = df1.columns.tolist()

    # 獲取第二個檔案的所有 columns
    columns2 = df2.columns.tolist()

    # 組合兩個檔案的 columns，確保沒有重複的標頭內容
    combined_columns = list(set(columns1 + columns2))

    return combined_columns

def find_column_differences(df1, df2):
    # 獲取第一個檔案的所有 columns
    columns1 = set(clean_columns(df1.columns))

    # 獲取第二個檔案的所有 columns
    columns2 = set(clean_columns(df2.columns))

    # 找出兩個檔案的 columns 中的差異
    differences = columns2 - columns1

    return list(differences)
    
def extract_information(row, key_points):
    result_list = []
    for key_point in key_points:
        #pattern = re.escape(key_point)+r'[:：]' + r'[\s\S]+?(?=\d+\.\s*|$)'
        pattern = re.escape(key_point)+r'[:：]' + r'[\s\S]+?(?=\d+\.\s*|$)'
        extracted_info = re.search(pattern, row['紀錄'])
        extracted_info
        if extracted_info != None :
            result_list.append(extracted_info.group(0).strip())
        else:
            result_list.append(None)  # 如果没有匹配到，填入 None
    return pd.Series(result_list, index=key_points)

def split_record(row):
    record = row['紀錄']
    key_points = row['Extracted_Key_Points']
    result = []

    for i in range(len(key_points)):
        current_key_point = key_points[i]
        next_key_point = key_points[i + 1] if i + 1 < len(key_points) else None

        # 使用正則表達式進行匹配
        if next_key_point is not None:
            pattern = re.escape(current_key_point) +r'[:：]' + r'(?:(?!' + re.escape(next_key_point) +r'[:：]' + r').)+'
        else:
            pattern = re.escape(current_key_point) + r'[\s\S]+'

        match = re.search(pattern, record)

        if match:
            result.append(match.group().strip())
        else:
            result.append(None)  # 如果没有匹配到，填入 None

    return pd.Series(result, index=key_points)


def process_excel_data(byte_data):
    # 讀取 Excel 檔案
    df= pd.read_excel(BytesIO(byte_data), engine='openpyxl')
   
    # 提取最後一欄的資料
    last_column = df.iloc[:, -1]
    # 針對每個要點進行擷取，並插入新的欄位
    extracted_key_points = last_column.apply(extract_key_points)
    df['Extracted_Key_Points'] = extracted_key_points
    #df[extracted_key_points] = df.apply(extract_information, axis=1, key_points=extracted_key_points)

    # 在這裡，你可以繼續進行其他操作，例如合併兩個檔案，執行相應的分析等
    # 針對每個要點進行擷取，並彙整成一個 list
    last_Keycolumn = df['Extracted_Key_Points']
    all_key_points = []
    for data in last_Keycolumn:
        all_key_points.extend(data)

    # 對 list 進行排序並去除重複的要點
    # 去除每个字符串两端的空格，但保留字符串中间的空格
    # sorted_unique_key_points = sorted(set(all_key_points))
    cleaned_list = [s.strip() for s in all_key_points]
    sorted_unique_key_points = sorted(set(cleaned_list))
    # 新增提取信息的列
    df['Extracted_Data'] = None
    for index, row in df.iterrows():
        # 在這裡處理每一行的數據
        #row
        # row['Extracted_Key_Points']
        extracted_information = split_record(row)
        # 將 Series 轉換為字典
        df.at[index,'Extracted_Data'] = extracted_information.to_string()
        #extracted_information_dict = extracted_information.to_dict()
        # 遍歷 extracted_information_dict 中的每一項
        #extracted_information_dict
        #for key, value in extracted_information_dict.items():
            # 檢查 key 是否存在於 row 的索引中
            #key
            #if key=='S' :
            #    row.index
            #if key in row.index:
                # 如果存在，將 value 放入對應的索引
            #    key
                #value
            #    row.at[index, key] = value
            #else:
                # 如果不存在，新增 key 的列
                #index
                #key
            #    value
            #    row[key] = None  # 或者使用其他預設值
            #    row.at[index, key] = value
    #extracted_information
    # sorted_unique_key_points
    # 在這裡，你可以進一步處理新的 list 或進行其他操作
    # 使用 assign 函數將 List 插入到 DataFrame 中，並賦予新的欄位名稱
    # for key_point in sorted_unique_key_points:
    #    df[key_point] = ""
    # 創建包含要點的新 DataFrame
    result_df = pd.DataFrame({'Sorted_Unique_Key_Points': sorted_unique_key_points})

    # 將結果保存為新的 Excel 檔案
    result_excel = BytesIO()
    result_df.to_excel(result_excel, index=False, engine='openpyxl')
    result_excel_data=result_excel.getvalue()
    # 範例：將組合後的標題寫入新的 Excel 檔案
    
    # 在這裡，你可以繼續進行其他操作，例如將兩個檔案的數據合併等

    # 去除重複的標題項目
    # output_df = output_df.loc[:, ~output_df.columns.duplicated()]

    output_excel = BytesIO()
    df.to_excel(output_excel, index=False, engine='openpyxl')

    # 取得最終的二進制數據
    output_excel_data = output_excel.getvalue()

    # 處理完成後返回處理後的數據
    return output_excel_data,result_excel_data


st.title('進行Excel要點分析與整理')

if st.checkbox('找出要點'):
    uploaded_file = st.file_uploader("請上傳Excel檔案")
    if uploaded_file is not None:
        # To read file as bytes:        
        bytes_data = uploaded_file.getvalue()
        result_byte_data1, result_byte_data2= process_excel_data(bytes_data)
        st.download_button(
            label="Download Full Result as Excel",
            data=result_byte_data1,
            file_name='Full_Result.xlsx',
            mime='Excel/xlsx',
        )       
        st.download_button(
            label="Download Key items as Excel",
            data=result_byte_data2,
            file_name='Key_items_List.xlsx',
            mime='Excel/xlsx',
        )

