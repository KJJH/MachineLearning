from pandas import DataFrame
import pandas as pd

crawling_data = pd.read_csv('CrawlingDataset.csv', encoding="euc-kr")  # csv 파일 읽어오기
crawling_test_data = pd.read_csv('CrawlingTestDataset.csv', encoding="euc-kr")  # Test용 csv 파일 읽어오기
del crawling_data['지점']
del crawling_test_data['지점']
crawling_data.columns = ['Date', 'Tav', 'Tmi', 'Tmx', 'Raf', 'Hum']  # column 이름 변경
crawling_test_data.columns = ['Date', 'Tav', 'Tmi', 'Tmx', 'Raf', 'Hum']


def SetValueData(dataframe, index, column_name, data_name, day_term):
    if index < day_term:
        dataframe.set_value(index, column_name, crawling_data[data_name].ix[:index].sum())
    else:
        dataframe.set_value(index, column_name, crawling_data[data_name].ix[index-day_term:index].sum())


def ProcessData(original_data, handling_data):
    day_term = {'hum': 4, 'raf': 5, 'rfd': 28, 'tav': 15, 'tmi': 1, 'tmx': 18}  # 계산해야 하는 누적 일수 - 1

    for index in range(original_data.shape[0]):
        # Date에 값 채우기
        handling_data.set_value(index, 'Date', original_data['Date'].ix[index])

        # 5일치 누적 습도 계산
        SetValueData(handling_data, index, 'Hum5', 'Hum', day_term['hum'])

        # 6일치 누적 강수량 계산
        SetValueData(handling_data, index, 'Raf6', 'Raf', day_term['raf'])

        # 29일치 누적 강수일 계산
        if index < day_term['rfd']:
            handling_data.set_value(index, 'Rfd29', original_data['Raf'].ix[:index].notnull().sum())
        else:
            handling_data.set_value(index, 'Rfd29', original_data['Raf'].ix[index-day_term['rfd']:index].notnull().sum())

        # 16일치 누적 평균온도 계산
        SetValueData(handling_data, index, 'Tav16', 'Tav', day_term['tav'])

        # 2일치 누적 최저온도 계산
        SetValueData(handling_data, index, 'Tmi2', 'Tmi', day_term['tmi'])

        # 19일치 누적 최고온도 계산
        SetValueData(handling_data, index, 'Tmx19', 'Tmx', day_term['tmx'])


# 데이터의 누적값 계산하기
accumulation_data = DataFrame(columns=('Date', 'Hum5', 'Raf6', 'Rfd29', 'Tav16', 'Tmi2', 'Tmx19'))  # 컬럼만 있는 데이터프레임 생성
accumulation_test_data = DataFrame(columns=('Date', 'Hum5', 'Raf6', 'Rfd29', 'Tav16', 'Tmi2', 'Tmx19'))

ProcessData(crawling_data, accumulation_data)  # crawling 데이터 처리
ProcessData(crawling_test_data, accumulation_test_data)  # test용 crawling 데이터 처리

accumulation_data = accumulation_data.fillna(0)  # Null값은 0으로 채우기
accumulation_test_data = accumulation_test_data.fillna(0)

accumulation_data = accumulation_data.set_index('Date')  # key값을 Date로 바꾸기
accumulation_test_data = accumulation_test_data.set_index('Date')

accumulation_data.to_csv('WeatherDataset.csv')
accumulation_test_data.to_csv('WeatherTestDataset.csv')