import pandas as pd

weather_data = pd.read_csv('WeatherDataset.csv')    # 기상데이터 csv 파일 읽어오기
mosquito_data = pd.read_csv('MosquitoDataset.csv', encoding="euc-kr")  # 모기데이터 csv 파일 읽어오기

merge_data = pd.merge(weather_data, mosquito_data, how='inner', on='Date')   # 데이터프레임 합치기

merge_data = merge_data.sort_values(['Location', 'Date'])  # Location과 Date값을 기준으로 정렬하기
merge_data = merge_data.set_index('Location')  # key값을 Location로 바꾸기

merge_data.to_csv('MergeDataset.csv')