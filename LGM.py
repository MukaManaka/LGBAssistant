# -*- coding: utf-8 -*-
from PIL import Image
from OCRTool import *
import time
###
# 图片处理
###

       
# 练功
class LGManager(object):
    """docstring for LGManager"""
    def __init__(self):
        super(LGManager, self).__init__()
        self.init()
        self.color_init()
        self.ocr_init()
        self.db_init()
        self.img = Image.open(r'screenshot\screenshot_temp.jpg').convert('RGB')
        self.size = self.img.size # 1400 x 3120
        self.load_db()
        self.loopn = 0  # 总个数
        self.dupln = 0  # 重复的个数


    def color_init(self):
        self.color_nomal = (250,250,250)
        self.color_yes =  (246,249,255)
        self.color_no =  (255,244,243)
        self.color_mid = (255,255,255) # 中间颜色


    # 单次的值
    def init(self):
        self.ans_num = 0
        self.ans_pos = []  # 答案的坐标
        self.question = None
        self.answer = []   # 答案的文本
        self.ans_right = [] # 答案的正误
        self.point_y = 0 # y轴指针

    def ocr_init(self):
        # self.ocr = OCR_tesseract()
        self.ocr = OCR_cnocr()

    def db_init(self):
        self.db_question_type = []
        self.db_question = []
        self.db_answer = []
        self.db_ansright = []


    # 题型获取
    def get_question_type(self):

        color = self.img.getpixel((1073,610))
        print(color)
        if color == (136,137,139):
            self.question_type = "判断题"
        if color == (247,181,0):
            self.question_type = "多选题"
        if color == (82,113,255):
            self.question_type = "单选题"
        print("题型： ", self.question_type)


    # 题目获取
    def get_question(self):
        # 找到题目的尾端 
        for y in range(729, 1704): # y轴 1k的余量
            for x in range(200,1200):          # 遍历x轴的中间部分颜色
                que = True
                color = self.img.getpixel((x,y))
                if (color != self.color_nomal and color != self.color_yes and color != self.color_no):
                    que = False  # 颜色错误
                    break
                    
            if que == True:
                self.point_y = y # 标记尾端 y轴值 指针到题目的尾端
                break


        bbox = (134, 737, 1271, self.point_y)
        self.img_temp = self.img.crop(bbox)
        # self.img_temp.show()

        content = self.ocr.run(self.img_temp)
        self.question =  content # 题目内容
        print("问题： ", content)



    def get_answers(self):

        # 查找选项
        for idx in range(5): # 最多6个选项
            start = (170, self.point_y+2) # 指针+20保证进入选项区域
            # 找到下一个选项的头
            for y in range(start[1], self.size[1]):  # y轴裕量1000
                for x in range(200,1200):          # 遍历x轴的中间部分颜色
                    que = True
                    color = self.img.getpixel((x,y))
                    if ((color != self.color_nomal) and (color != self.color_yes) and (color != self.color_no)):
                        que = False  # 颜色错误 跳出x轴遍历
                        break

                # 当前x轴遍历结束
                if que == True: # 颜色正确
                    self.point_y = y # 标记头端 y轴值 指针到选项的头端
                    start = (170, y) # 修正开始值
                    print("答案头坐标：", start)
                    break # 跳出y轴遍历
                else: # 颜色错误
                    pass

            if que == False: # 没找到答案头
                print("没有答案了.")
                break



                 

            # 寻找答案尾
            end = (170, self.point_y+1) # 留下一点裕量

            # 找到第n个选项的尾端
            for y in range(end[1], self.size[1]): 
                for x in range(200,1200):          # 遍历x轴的中间部分颜色
                    que = True
                    color = self.img.getpixel((x,y))
                    if color != self.color_mid: # 不是中间颜色
                        que = False
                        break

                # 当前x轴遍历结束
                if que == True: # 颜色正确
                    self.point_y = y # 标记头端 y轴值 指针到选项的头端
                    end = (170, y)# 修正开始值
                    print("答案尾坐标：", end)
                    break # 跳出y轴遍历
                else: # 颜色错误
                    pass


            self.ans_pos.append((1250, (end[1] + start[1])/2))
            self.ans_num += 1

            bbox = (280, start[1], 1136, end[1])
            self.img_temp = self.img.crop(bbox)
            # self.img_temp.show()

            content = self.ocr.run(self.img_temp)
            self.answer.append(content) # 答案内容
            print("答案：", content)



    def run(self, get_ans = True):
        
        self.img = Image.open(r'screenshot\screenshot_temp.jpg').convert('RGB')
        self.size = self.img.size # 1400 x 3120
        # self.img.show()

        self.get_question_type()
        self.get_question()
        self.loopn += 1
        if get_ans:
            self.get_answers()



    # 载入数据库
    def load_db(self):
        with open("database.txt", "r") as f:
            db_list = f.readlines()

        for db in db_list:
            text = db.split("---")
            self.db_question_type.append(text[0])
            self.db_question.append(text[1])
            db_ansr = []
            db_ans = []
            for tx in text[2:]:
                tx = tx.replace("\n", "")
                if tx == "Y" or tx == "N":
                    db_ansr.append(tx)
                else:
                    db_ans.append(tx)

            self.db_ansright.append(db_ansr)
            self.db_answer.append(db_ans)


    # 判断相似度
    def disting(self, new_quest, dp = 0.9):
        qlen = len(new_quest) # 长度
        nosame = True
        for que in self.db_question: # 遍历数据库中的每个问题
            sc = 0
            for word in new_quest:
                if word in que:
                    sc += 1
            if sc/qlen >= dp:
                nosame = False
                print("---警告:重复问题---")
                print("---数据库问题:", que)
                print("---当前问题:", new_quest)
                break
            
        return nosame


    # 判断正误
    def judge(self):
        for pos in self.ans_pos:
            color = self.img.getpixel(pos)
            if color == self.color_yes:
                self.ans_right.append("Y")
            else:
                self.ans_right.append("N")

    # 查询问题
    def out_answer(self, dp = 0.9):
        qlen = len(self.question) # 长度
        nosame = True
        for idx, que in enumerate(self.db_question): # 遍历数据库中的每个问题
            sc = 0
            for word in self.question:
                if word in que:
                    sc += 1
            if sc/qlen >= dp:
                nosame = False
                print("-----找到问题-----")
                print("-数据库问题:", que)
                for i in range(len(self.db_answer[idx])):
                    print(f"-数据库答案{i+1}: ", self.db_answer[idx][i], end = "--")
                    print("---", self.db_ansright[idx][i])

        if nosame:
            print("---没找到此问题!---")
                




    # 题库写入
    def db_write(self):

        self.judge()
        # 判断是否存在
        if self.disting(self.question):
            print("----正在写入-----")
            # 写入database list
            self.db_question_type.append(self.question_type)
            self.db_question.append(self.question)
            self.db_ansright.append(self.ans_right)
            self.db_answer.append(self.answer)

            with open("database.txt", "a+") as f:
                f.write(self.question_type + "---" + self.question)
                for i in range(self.ans_num):
                    f.write("---" + self.answer[i] + "---" + self.ans_right[i])
                f.write("\n")
        else:
            self.dupln += 1 # 重复

        print(f"---重复率：{self.dupln} / {self.loopn} = {self.dupln * 100.0 / self.loopn}%")

        


if __name__ == '__main__':
    lm = LGManager()
    lm.run()
    lm.db_write()