from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv


# set driver PATH
browser = webdriver.Chrome("chromedriver.exe")
# Crawling URL
browser.get("https://data.kma.go.kr/data/grnd/selectAsosRltmList.do?pgmNo=36")


########################################    페이지 설정    ################################################
#자료형태 - 일 자료
script = browser.find_elements_by_xpath('//*[@id="dataFormCd"]/option[2]')[0]
script.click()
time.sleep(1)


# 기간 선택 - 시작 날짜
script = browser.find_elements_by_xpath('//*[@id="startDt"]')[0]
script.click()
time.sleep(1)

#   2011년
script = browser.find_elements_by_xpath('//*[@id="ui-datepicker-div"]/div[1]/div/select[1]/option[112]')[0]
script.click()
time.sleep(1)

#   1월
script = browser.find_elements_by_xpath('//*[@id="ui-datepicker-div"]/div[1]/div/select[2]/option[1]')[0]
script.click()
time.sleep(1)

#   1일
script = browser.find_elements_by_xpath('//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[7]/a')[0]
script.click()
time.sleep(1)

# 끝 날짜
script = browser.find_elements_by_xpath('//*[@id="endDt"]')[0]
script.click()
time.sleep(1)

#   2016년
script = browser.find_elements_by_xpath('//*[@id="ui-datepicker-div"]/div[1]/div/select[1]/option[117]')[0]
script.click()
time.sleep(1)

#   12월
script = browser.find_elements_by_xpath('//*[@id="ui-datepicker-div"]/div[1]/div/select[2]/option[12]')[0]
script.click()
time.sleep(1)

#   31일
script = browser.find_elements_by_xpath('//*[@id="ui-datepicker-div"]/table/tbody/tr[5]/td[7]/a')[0]
script.click()
time.sleep(1)


# 지점 - 지점 명으로 선택
script = browser.find_elements_by_xpath('//*[@id="btnStn1"]')[0]
script.click()
time.sleep(2)

# 서울
script = browser.find_elements_by_xpath('//*[@id="ztree_4_check"]')[0]
script.click()
time.sleep(1)

# 선택완료
script = browser.find_elements_by_xpath('//*[@id="sidetreecontrol"]/ul[2]/li/a')[0]
script.click()
time.sleep(1)


# 요소 - 선택
script = browser.find_elements_by_xpath('//*[@id="gubun"]')[0]
script.click()
time.sleep(2)

#   최고기온
script = browser.find_elements_by_xpath('//*[@id="ztree_4_check"]')[0]
script.click()
time.sleep(1)

#   최저기온
script = browser.find_elements_by_xpath('//*[@id="ztree_6_check"]')[0]
script.click()
time.sleep(1)

#   평균기온
script = browser.find_elements_by_xpath('//*[@id="ztree_7_check"]')[0]
script.click()
time.sleep(1)

#   일강수량
script = browser.find_elements_by_xpath('//*[@id="ztree_9_check"]')[0]
script.click()
time.sleep(1)

#   평균 상대습도
script = browser.find_elements_by_xpath('//*[@id="ztree_26_check"]')[0]
script.click()
time.sleep(1)

# 선택완료
script = browser.find_elements_by_xpath('//*[@id="sidetreecontrol"]/ul[2]/li/a')[0]
script.click()
time.sleep(1)

# 조회
script = browser.find_elements_by_xpath('//*[@id="dsForm"]/div[3]/a[1]')[0]
script.click()
time.sleep(2)


# 한 페이지 당 자료 개수 - 100
script = browser.find_elements_by_xpath('//*[@id="schListCnt"]/option[10]')[0]
script.click()
time.sleep(1)


# 조회
script = browser.find_elements_by_xpath('//*[@id="dsForm"]/div[3]/a[1]')[0]
script.click()
time.sleep(2)
##########################################################################################################


# open the csv file for write
file = open('CrawlingDataset.csv', 'w', newline='')
wr = csv.writer(file)

# page Crawling
script = browser.find_element_by_xpath("//*").get_attribute("innerHTML")
soup = BeautifulSoup(script , 'html.parser')

# crawled header name
headerNameList = []
for headerName in soup.find_all('tr', id='headerNm'):
    for name in headerName.find_all('th'):
        headerNameList.append(name.get_text())
wr.writerow(headerNameList)


def crawlCurrentPage():
    # page Crawling
    script = browser.find_element_by_xpath("//*").get_attribute("innerHTML")
    soup = BeautifulSoup(script , 'html.parser')

    # crawled contents
    for contentsTable in soup.find_all('tbody', id='contentsList'):
        for contentsTr in contentsTable.find_all('tr'):
            contentsList = []
            for contents in contentsTr.find_all('td'):
                contentsList.append(contents.get_text())
            wr.writerow(contentsList)


def toTheNextPage(front, index, back):
    script = browser.find_elements_by_xpath(front + str(index) + back)[0]
    script.click()
    time.sleep(2)


# crawling by page
xpathFront = '//*[@id="content"]/div[2]/div[3]/div[2]/div[1]/ul/li['
xpathBack = ']/a'
for repeat in range(2):
    for pageIndex in range(4, 14):
        crawlCurrentPage()
        toTheNextPage(xpathFront, pageIndex, xpathBack)
for pageIndex in range(4, 6):
    crawlCurrentPage()
    toTheNextPage(xpathFront, pageIndex, xpathBack)


file.close()
browser.quit()  # 브라우저 종료





#############################   Test Dataset을 만들기 위한 데이터 크롤링   ###############################

# set driver PATH
browser = webdriver.Chrome("chromedriver.exe")
# Crawling URL
browser.get("https://data.kma.go.kr/data/grnd/selectAsosRltmList.do?pgmNo=36")

########################################    페이지 설정    ################################################
#자료형태 - 일 자료
script = browser.find_elements_by_xpath('//*[@id="dataFormCd"]/option[2]')[0]
script.click()
time.sleep(1)


# 기간 선택 - 시작 날짜
script = browser.find_elements_by_xpath('//*[@id="startDt"]')[0]
script.click()
time.sleep(1)

#   1월
script = browser.find_elements_by_xpath('//*[@id="ui-datepicker-div"]/div[1]/div/select[2]/option[1]')[0]
script.click()
time.sleep(1)

#   1일
script = browser.find_elements_by_xpath('//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[1]/a')[0]
script.click()
time.sleep(1)

# 끝 날짜
script = browser.find_elements_by_xpath('//*[@id="endDt"]')[0]
script.click()
time.sleep(1)

#   8월
script = browser.find_elements_by_xpath('//*[@id="ui-datepicker-div"]/div[1]/div/select[2]/option[8]')[0]
script.click()
time.sleep(1)

#   31일
script = browser.find_elements_by_xpath('//*[@id="ui-datepicker-div"]/table/tbody/tr[5]/td[5]/a')[0]
script.click()
time.sleep(1)


# 지점 - 지점 명으로 선택
script = browser.find_elements_by_xpath('//*[@id="btnStn1"]')[0]
script.click()
time.sleep(2)

# 서울
script = browser.find_elements_by_xpath('//*[@id="ztree_4_check"]')[0]
script.click()
time.sleep(1)

# 선택완료
script = browser.find_elements_by_xpath('//*[@id="sidetreecontrol"]/ul[2]/li/a')[0]
script.click()
time.sleep(1)


# 요소 - 선택
script = browser.find_elements_by_xpath('//*[@id="gubun"]')[0]
script.click()
time.sleep(2)

#   최고기온
script = browser.find_elements_by_xpath('//*[@id="ztree_4_check"]')[0]
script.click()
time.sleep(1)

#   최저기온
script = browser.find_elements_by_xpath('//*[@id="ztree_6_check"]')[0]
script.click()
time.sleep(1)

#   평균기온
script = browser.find_elements_by_xpath('//*[@id="ztree_7_check"]')[0]
script.click()
time.sleep(1)

#   일강수량
script = browser.find_elements_by_xpath('//*[@id="ztree_9_check"]')[0]
script.click()
time.sleep(1)

#   평균 상대습도
script = browser.find_elements_by_xpath('//*[@id="ztree_26_check"]')[0]
script.click()
time.sleep(1)

# 선택완료
script = browser.find_elements_by_xpath('//*[@id="sidetreecontrol"]/ul[2]/li/a')[0]
script.click()
time.sleep(1)

# 조회
script = browser.find_elements_by_xpath('//*[@id="dsForm"]/div[3]/a[1]')[0]
script.click()
time.sleep(2)


# 한 페이지 당 자료 개수 - 100
script = browser.find_elements_by_xpath('//*[@id="schListCnt"]/option[10]')[0]
script.click()
time.sleep(1)


# 조회
script = browser.find_elements_by_xpath('//*[@id="dsForm"]/div[3]/a[1]')[0]
script.click()
time.sleep(2)
##########################################################################################################


# open the csv file for write
file = open('CrawlingTestDataset.csv', 'w', newline='')
wr = csv.writer(file)

# page Crawling
script = browser.find_element_by_xpath("//*").get_attribute("innerHTML")
soup = BeautifulSoup(script , 'html.parser')

# crawled header name
headerNameList = []
for headerName in soup.find_all('tr', id='headerNm'):
    for name in headerName.find_all('th'):
        headerNameList.append(name.get_text())
wr.writerow(headerNameList)


def crawlCurrentPage():
    # page Crawling
    script = browser.find_element_by_xpath("//*").get_attribute("innerHTML")
    soup = BeautifulSoup(script , 'html.parser')

    # crawled contents
    for contentsTable in soup.find_all('tbody', id='contentsList'):
        for contentsTr in contentsTable.find_all('tr'):
            contentsList = []
            for contents in contentsTr.find_all('td'):
                contentsList.append(contents.get_text())
            wr.writerow(contentsList)


def toTheNextPage(front, index, back):
    script = browser.find_elements_by_xpath(front + str(index) + back)[0]
    script.click()
    time.sleep(2)


# crawling by page
xpathFront = '//*[@id="content"]/div[2]/div[3]/div[2]/div[1]/ul/li['
xpathBack = ']/a'
for pageIndex in range(2, 4):
    crawlCurrentPage()
    toTheNextPage(xpathFront, pageIndex, xpathBack)
crawlCurrentPage()


file.close()
browser.quit()  # 브라우저 종료