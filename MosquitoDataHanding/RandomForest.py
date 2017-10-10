import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def split_train_dataset(dataset, feature_headers, target_header):
    train_x = dataset[feature_headers]
    train_y = dataset[target_header]

    return train_x, train_y


def split_test_dataset(landUse):
    testdataset = pd.read_csv('WeatherTestDataset.csv')
    testdataset['LandUse'] = landUse
    column_list = (testdataset.columns.values)

    test_x = testdataset[column_list[1:]].tail(31)

    return test_x


def random_forest_classifier(features, target):
    clf = RandomForestClassifier()
    clf.fit(features, target)
    return clf


def main():
    dataset = pd.read_csv('MergeDataset.csv', encoding="euc-kr")
    column_list = (dataset.columns.values)

    train_x, train_y = split_train_dataset(dataset, column_list[2:9], column_list[-1])
    trained_model = random_forest_classifier(train_x, train_y)
    prediction = trained_model.predict(train_x)

    # 훈련시킨 데이터의 예측값 확인
    for i in range(100, 111):
        print("Actual outcome :: {} and Predict outcome :: {}".format(list(train_y)[i], prediction[i]))

    # 훈련의 정확도가 어느 정도인지 측정
    print("\n>> Train Accuracy :: ", accuracy_score(train_y, prediction))


    # LandUse값에 따른 2017년 8월의 모기 레벨 예측값
    for landuse in range(1, 4):
        test_x = split_test_dataset(landuse)
        prediction = trained_model.predict(test_x)

        print("\nLandUse : " + str(landuse))
        for i in range(0, 31):
            print("{}day Predict outcome :: {}".format(i+1, prediction[i]))


if __name__ == '__main__':
    main()
