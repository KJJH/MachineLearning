from pandas import DataFrame
import pandas as pd
import math
import os

path = './MosquitoData/'

# MosquitoData 폴더에 있는 csv 파일 리스트에 저장하기
datafile_list = []
for root, dirs, files in os.walk(path):
    for file in files:
        datafile_list.append(file)


location_part = {'국회의원회관':2, '대림동 유수지':3, '당산 중학교':2, '동아에코빌 아파트':1, '두암어린이공원':1, 'KBS':2, '김안과 병원':1, '문래근린공원':1, '문래동빗물펌프장':3, '살레시오':1,
                 '신길근린공원':1, '신일어린이집':1, '양평동 생태공원':3, '양평동노인복지회관':1, '양평1동 유수지':3, '양평빗물펌프장':3, '여의도고등학교':1, '영등포공원':1, '윤중초등학교':1}



# csv 파일 하나씩 불러와서 데이터 처리하기
concat_data = DataFrame(columns=('Location', 'Date', 'Mosq', 'LandUse', 'Level'))  # 컬럼만 있는 데이터프레임 생성

for datafile in datafile_list:
    mosquito_data = pd.read_csv(path + datafile, names=['Date', 'Mosq'])  # csv 파일 읽어오기
    mosquito_data['Date'] = pd.to_datetime(mosquito_data['Date'])  # 2011-05-05 00:00:00 → 2011-05-05 변환
    mosquito_data = mosquito_data.set_index('Date')  # key를 index에서 Date로 바꾸기
    mosquito_data = mosquito_data.resample('D').sum()  # 날짜를 기준으로 날짜 사이의 빈 값을 채워준다
    mosquito_data['Level'] = ''  # 모기 Level 추가하기

    print(datafile)

    # 모기 수가 10000마리 이상인 경우 오류로 판단 -> -1
    for index, row in mosquito_data.iterrows():
        if 10000 <= row['Mosq']:
            mosquito_data.set_value(index, 'Mosq', -1)

    # 오류가 아닌 정상적인 값에 대한 계산
    comp_year_month = ''
    month_avg = 0
    for index, row in mosquito_data.iterrows():
        year_month = str(index)[:7]

        if comp_year_month != year_month:  # 값을 바꾸기 전에 해당 달의 평균 모기 수를 계산하기 위해
            comp_year_month = year_month
            month_avg = float(mosquito_data[year_month].mean())

        # 비어있는 값을 해당 달의 평균값으로 채우기
        if str(row['Mosq']) == 'nan':
            mosquito_data.set_value(index, 'Mosq', math.ceil(month_avg))
            row['Mosq'] = math.ceil(month_avg)

        # 모기 수가 1000마리 이상인 경우 값을 1000으로 바꾸기
        if 1000 <= row['Mosq']:
            mosquito_data.set_value(index, 'Mosq', 1000)
            row['Mosq'] = 1000

        # 오류인 경우 값을 해당 달의 평균값으로 채우기
        if row['Mosq'] <= -1:
            mosquito_data.set_value(index, 'Mosq', math.ceil(month_avg))
            row['Mosq'] = math.ceil(month_avg)

        # 모기 레벨 계산하기
        if row['Mosq'] <= 20:
            mosquito_data.set_value(index, 'Level', 1)
        else:
            mosquito_data.set_value(index, 'Level', math.ceil(math.log(row['Mosq']/10, 2)))

    mosquito_data.insert(0, 'Location', datafile.split('_')[0])  # 지역 추가하기
    mosquito_data['LandUse'] = location_part[datafile.split('_')[0]]  # LandUse 추가하기

    concat_data = pd.concat([concat_data, mosquito_data])   # 데이터프레임 합치기


concat_data['Date'] = concat_data.index
concat_data = concat_data.set_index('Location')  # key값을 Location으로 바꾸기
del concat_data['Mosq']  # 모기 마리 수에 대한 column 삭제
concat_data.to_csv('MosquitoDataset.csv')