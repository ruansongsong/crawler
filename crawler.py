#coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
import robotparser
import json
import datetime
import jieba
from boilerpipe.extract import Extractor
from bs4 import BeautifulSoup

# 获取网页内容
def getHtml(url, urlList, logs):
  headers = {
    "User-Agent": "IRCourse2017S+201461551289",
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Connection': 'Keep-Alive'
  };
  try:
    response = requests.get(url, headers = headers);
    if(response.status_code == 200):
      #保存网页
      response.encoding = 'utf-8'
      # print response.text
      saveHtml(url, response.text)
      # 访问过则设置 visit 为 true
      urlList[url]["visit"] = True
      # 生成日志log
      log = generateLogs(url, "IRCourse2017S+201461551289", "Fetching", "successful")
      logs.append(log)
      return response.text;
    else:
      log = generateLogs(url, "IRCourse2017S+201461551289", "Fetching", "Error")
      logs.append(log)
      return False
  except:
    return False

#分词
def cutWord(text):
  segList = jieba.cut(processed_plaintext, cut_all = False)
  return "/".join(segList)

# 保存网页为txt文件
def saveHtml(url, page):
  extractor = Extractor(extractor = 'ArticleExtractor', html = page)
  processed_plaintext = extractor.getText()
  # print processed_plaintext
  fileName = "./doc/" + (url + ".txt").replace("/", "()")
  f = open(fileName, "w")
  f.write(processed_plaintext);
  f.close()

# 解析网页中的url
def parseUrl(htmlPage, deep, urlList, url, logs):
  soup = BeautifulSoup(htmlPage, "lxml")
  if(soup.find_all('a')[0]):
    for link in soup.find_all('a'):
      tempLink = link.get('href')
      
      # 规范会一些url，例如类似这种 /new/2014/..
      if(tempLink and tempLink[0:3] != 'http'):
        if(tempLink[0:4] == "/new"):
          tempLink = url + tempLink[4:]
        elif(tempLink[0:4] != 'http'):
          # print tempLink
          tempLink = url + '/' + tempLink
          # print tempLink
        else:
          continue
      # 将url加入字典中
      urlList[tempLink] = {
        "visit": False,
        "deep": deep
      }
    # 生成日志
    log = generateLogs(url, "IRCourse2017S+201461551289", "Parsing", "Successful")
    logs.append(log)
  else:
    log = generateLogs(url, "IRCourse2017S+201461551289", "Parsing", "Error")
    logs.append(log)


# 生成日志
def generateLogs(url, userAgent, operatType, doneFlag): 
  timestamp = str(datetime.datetime.now())
  log = url + ' ' + userAgent + ' ' + timestamp + ' ' + operatType + ' ' + doneFlag
  return log

# 解析 robots.txt 文件,暂时没用，因为scut.edu.cn上没有robots.txt文件
def parseRobots(url):
  # 解析robots.txt
  rp = robotparser.RobotFileParser()
  rp.set_url(urlparse.urljoin(url, "/robots.txt"))
  rp.read()
  return rp

if __name__ == '__main__':
  # 全局变量
  urlList = {
    "http://news.scut.edu.cn/": {
      "visit": False,
      "deep": -1
    }
  }
  logs = []
  # 统计变量
  # 网页数
  pageNumber = 0;
  for deep in range(0, 4):
    for url in urlList.keys():
      if(urlList.get(url)["visit"] == True):
        continue
      if(getHtml(url, urlList, logs)):
        htmlPage = getHtml(url, urlList, logs)
        pageNumber = pageNumber + 1
        if(pageNumber == 2123):
          print pageNumber
          exit()
          
        parseUrl(htmlPage, deep, urlList, url, logs)
      else:
        continue
  print pageNumber
  # 写入url到json文件,并格式化好
  jsonUrlList = json.dumps(urlList, indent = 2)
  f = open("url.json", "w")
  f.write(jsonUrlList);
  f.close()
  # 写入日志文件
  f1 = open('logs.txt', 'w')  
  for log in logs:  
      f1.write(log)  
      f1.write('\n')  
  f1.close()  
  

