import os
import sys
import time
from PIL import Image
##
#工具性文件
##

class GearADB(object):
    """docstring for GearADB"""
    def __init__(self):
        self.screenshot_path = os.getcwd() + '/screenshot'

    def push(self, string):
        os.popen(string)

    def screenshot(self, sleep=5):
        print('正在开始截图.')

        while True:
            try:
                self.push("adb shell screencap -p /data/local/tmp/tmp.jpg")

                # 如不存在，新建文件夹
                if not os.path.isdir(self.screenshot_path):
                    os.makedirs(self.screenshot_path)

                time.sleep(sleep)
                os.popen("adb pull /data/local/tmp/tmp.jpg " + os.path.abspath(self.screenshot_path + "/screenshot_temp.jpg"))

                time.sleep(2)
                os.popen("adb shell rm /data/local/tmp/tmp.jpg")
                print('截图完成.')

                img = Image.open(r"screenshot\screenshot_temp.jpg").convert('L')
                return img
            except:
                sleep += 1

    def tap(self, position, sleep=1):
        x = position[0]
        y = position[1]
        print(f'正在点击坐标 ({x},{y})')
        self.push(f'adb shell input tap {x} {y}')
        time.sleep(1)


    def dump_device_info(self):
        """
        显示设备信息
        """
        size_str = os.popen('adb shell wm size').read()
        device_str = os.popen('adb shell getprop ro.product.device').read()
        phone_os_str = os.popen('adb shell getprop ro.build.version.release').read()
        density_str = os.popen('adb shell wm density').read()
        print("""**********
            Screen: {size}
            Density: {dpi}
            Device: {device}
            Phone OS: {phone_os}
            Host OS: {host_os}
            Python: {python}
            **********""".format(
            size=size_str.strip(),
            dpi=density_str.strip(),
            device=device_str.strip(),
            phone_os=phone_os_str.strip(),
            host_os=sys.platform,
            python=sys.version
        ))


if __name__ == '__main__':
    adb = GearADB()
    adb.screenshot()
