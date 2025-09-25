import pandas as pd
import argparse

def load_and_explore_data(file_path):
    """任務一：讀取 CSV 並初步探索資料"""
    try:
        df = pd.read_csv(file_path, encoding='utf-8-sig')
    except FileNotFoundError:
        print(f"錯誤：檔案 {file_path} 找不到")
        return None
    except Exception as e:
        print(f"讀取檔案時發生錯誤: {e}")
        return None

    # 顯示前 5 筆資料
    print(df.head())

    # 查看資料結構（欄位、型態、缺失值）
    print(df.info())
    return df

def feature_engineering(df):
    """任務二：計算總分、平均分數與是否及格"""

    # 計算總分，考慮缺失值
    df['總分'] = df[['數學', '英文', '國文', '自然', '社會']].sum(axis=1, skipna=True)

    # 計算平均分數，考慮缺失值
    df['平均分數'] = df[['數學', '英文', '國文', '自然', '社會']].mean(axis=1, skipna=True)

    # 新增是否及格欄位（平均 >= 60 為及格）
    df['是否及格'] = df['平均分數'] >= 60

    return df

def filter_and_analyze_data(df):
    """任務三與四：篩選資料與統計"""

    # 找出數學成績 < 60 的學生
    math_failed = df[df['數學'] < 60]

    # 找出班級為 'A' 且英文 > 90 的學生
    high_A = df[(df['班級'] == 'A') & (df['英文'] > 90)]

    # 統計摘要
    score_columns = ['數學', '英文', '國文', '自然', '社會', '平均分數']
    summary = df[score_columns].describe()

    # 找出總分最高的學生
    top_student = df.loc[df['總分'].idxmax()]  # 只返回最高分的那一行資料

    # 回傳 dict，方便 pytest 檢查每個任務
    return {
        "processed_df": df,
        "math_failed": math_failed,
        "high_A": high_A,
        "summary": summary,
        "top_student": top_student
    }

def save_results(df, output_file_path):
    """任務五：儲存為 CSV"""
    try:
        df.to_csv(output_file_path, encoding='utf-8-sig', index=False)
    except IOError as e:
        print(f"寫入檔案時發生錯誤: {e}")

def main():
    # 使用 argparse 來處理檔案路徑的輸入
    parser = argparse.ArgumentParser(description="學生期中成績分析")
    parser.add_argument('input_csv', help="輸入的 CSV 檔案路徑")
    parser.add_argument('output_csv', help="輸出的 CSV 檔案路徑")

    args = parser.parse_args()

    # 讀取資料
    df = load_and_explore_data(args.input_csv)
    if df is not None:
        df = feature_engineering(df)
        result = filter_and_analyze_data(df)
        save_results(result["processed_df"], args.output_csv)

        print("完成所有分析任務")

if __name__ == "__main__":
    main()
