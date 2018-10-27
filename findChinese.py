import re
import os

# desc 用来前端文件的中文字符获取的脚本
# exapmle
# excludeList = ['./edas/nls', './edas/aliyun-edas-tpl.js', './edas/controllers/dbgInfoController.js']
# file = CompileProject('./demo')
# file.compile()

class CompileProject:
    '''编译单个文件脚本'''

    def __init__(self, path, excludePath=[]):
        self.path = path
        self.excludePath = excludePath
        self.allfile = []
        self._hasMultiComment = False

    def removeComments(self, txt):

        # 以 **/结尾
        if (re.match(".*/*\/\s*$", txt)):
            self._hasMultiComment = False

        # 以 /**开头
        if(re.match("^\s*/\*.*", txt)):
            self._hasMultiComment = True

        if(self._hasMultiComment):
            return ''

        # 删除 /*开头的注释 (/*COMMENT */) from string
        # txt = re.sub(re.compile("\s*/\*.*", re.DOTALL), "", txt)
        # txt = re.sub(re.compile("/\*.*?\*/", re.DOTALL), "", txt)

        # 删除所有的单行comment (//COMMENT\n )
        txt = re.sub(re.compile("//.*?\n"), "", txt)

        # 删除所有的html中的注释 < !-- -->
        txt = re.sub(re.compile("<!--.*"), "", txt)

        # 删除所有的console.log中的注释
        txt = re.sub(re.compile("console.log.*"), "", txt)
        return txt

    # 查找中文
    def findChinese(self, txt):
        txt = self.removeComments(txt)
        pattern = re.compile('([\u4e00-\u9fa5]+)+?')
        return pattern.findall(txt)


    def compliefile(self, filename):
        # 用于打印文件路径(出现中文时候只打印一次)
        shouldPrintPath = True

        def complieSigleLine(line, filename):
            nonlocal shouldPrintPath
            for line, value in enumerate(line):
                chineseVal = self.findChinese(value)
                if (chineseVal):
                    if shouldPrintPath:
                        print(filename)
                    shouldPrintPath = False
                    print('%s: 中文字符%s' % (line + 1, chineseVal))

        with open(filename) as f:
            try:
                complieSigleLine(f.readlines(), filename)
            except Exception as e:
                print(e)

    def getallfile(self, path=''):
        path = path or self.path
        allfilelist = os.listdir(path)
        for file in allfilelist:
            filepath = os.path.join(path, file)
            # 排除某些路径
            if (filepath in self.excludePath):
                continue

            # 判断是不是文件夹
            isFileDir = os.path.isdir(filepath)
            self.getallfile(filepath) if isFileDir else self.allfile.append(filepath)
        return self.allfile

    def compile(self):
        allfiles = self.getallfile()
        for file in allfiles:
            self.compliefile(file)


