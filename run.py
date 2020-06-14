from LGM import *
from Tools import *



adb = GearADB()
lm = LGManager()

mode = "答题"
# mode = "题库"


input("start.")

while True:
    if mode == "题库":

        lm.init()
        lm.init()

        # 点答案
        print("---点答案---")
        adb.tap((0.714 * lm.size[0], 0.35 * lm.size[1]),sleep=0)
        adb.tap((0.714 * lm.size[0], 0.47 * lm.size[1]),sleep=0)
        adb.tap((0.714 * lm.size[0], 0.53 * lm.size[1]),sleep=0)

        # 点提交
        print("---点提交---")
        adb.tap((0.714 * lm.size[0], 0.60 * lm.size[1]),sleep=0)
        adb.tap((0.714 * lm.size[0], 0.66 * lm.size[1]),sleep=0)
        adb.tap((0.714 * lm.size[0], 0.70 * lm.size[1]),sleep=0)



        adb.screenshot()
        lm.init()
        lm.run()
        lm.db_write()      
        print("-------截图识别完毕-------") 


        # 点下一题
        print("---点下一题---")
        adb.tap((0.714 * lm.size[0], 0.80 * lm.size[1]),sleep=0)
        adb.tap((0.714 * lm.size[0], 0.83 * lm.size[1]),sleep=0)
        adb.tap((0.714 * lm.size[0], 0.86 * lm.size[1]),sleep=0)

    elif mode == "答题":
        input("Press Enter to next question...")
        adb.screenshot(sleep = 2)
        lm.init()
        lm.run(get_ans = False)
        print("-------截图识别完毕-------") 
        lm.out_answer()    









if __name__ == '__main__':
    main()