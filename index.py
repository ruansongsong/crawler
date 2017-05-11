# coding:utf-8

# 对doc目录里的所有文件建立索引

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os, lucene, threading, time
from datetime import datetime
from java.io import File
from java.nio.file import Paths
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType, Document, TextField
from org.apache.lucene.index import \
    FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

lucene.initVM() 
print 'lucene',lucene.VERSION
start = datetime.now()
indexDir = './index'
docDir = './doc'
# try :
analyzer = StandardAnalyzer() 
analyzer = LimitTokenCountAnalyzer(analyzer, 10000)
config = IndexWriterConfig(analyzer)
config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
INDEXDIR = SimpleFSDirectory(Paths.get(indexDir))
indexWriter = IndexWriter(INDEXDIR, config)

for root, dirnames, filenames in os.walk(docDir):
    for filename in filenames:
        print filename
        url = filename.replace("()", "/").replace(".txt", "")
        # print url
        if not filename.endswith('.txt'):
            continue
        path = os.path.join(root,filename)
        path = os.path.abspath(os.path.normpath(path))
        with open(path,'r') as c:
            contents = unicode(c.read(),'utf-8')

        doc = Document()
        urlField = Field('url', url, TextField.TYPE_STORED)
        doc.add(urlField)
        nameField = Field('name', filename, TextField.TYPE_STORED)
        doc.add(nameField)
        pathField = Field('path', path, TextField.TYPE_STORED)
        doc.add(pathField)
        contentsField = Field('contents', contents, TextField.TYPE_STORED)
        doc.add(contentsField)

        indexWriter.addDocument(doc)
indexWriter.commit()
indexWriter.close()
end = datetime.now()
print '建立索引花费时间：', (end-start)
