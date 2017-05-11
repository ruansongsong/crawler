#coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import sys, os, time
import lucene
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.util import Version

indexDir = './index'
query = 'null'
lucene.initVM()
print 'lucene', lucene.VERSION
keyWords = ["学术论坛", "媒体", "校园新闻", "创新", "机构设置", "教学在线", "科研处", "招生"]
#索引的存放位置
indir = SimpleFSDirectory(Paths.get(indexDir))
#分词器
analyzer = StandardAnalyzer()
#检索器
searcher = IndexSearcher(DirectoryReader.open(indir))

for i in range(0, 8):
  keyword = keyWords[i]
  query = QueryParser('contents', analyzer).parse(keyword) 
  #开始搜索
  hits = searcher.search(query,100)
  print '搜索到的结果数为：', hits.totalHits
  f = open("result.txt", "a")
  f.write("\nTD" + str(i) + " " + keyword);
  f.write('\n')
  f.close()
  for hit in hits.scoreDocs:
      doc = searcher.doc(hit.doc)
      temp = doc.get('url') + " " + str(hit.score)
      f = open("result.txt", "a")
      f.write(temp);
      f.write('\n')
      f.close()
