import time
import ctypes
import winsound

# 为实现输出时重置光标，而不是清屏（调用 cls 会有延时、闪屏现象），使用 ctypes 中的 api，先构建一个类
# 定义 x, y 坐标类型为 c 中的 short 类型
class COORD(ctypes.Structure):
    _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

    def __init__(self, x, y):
        self.X = x
        self.Y = y


# 定义光标位置
STD_OUTPUT_HANDLE = -11
hOut = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
INIT_POS = COORD(0, 0)

"""
注意：精准控制每 1/30 秒输出一帧，不能使用 sleep 函数，。
sleep 线程休眠时间并不精准，且易受其他干扰因素影响。
每一次不准，积累到最后将会有 10~20s 的播放误差。
因此要采用设置循环反复查询间隔时间的方式。这样控制极为精准，最后误差可控在  0.5s 内。
但由于短时间内反复执行大量循环，会对 cpu 资源有一定消耗。
"""

# 总运行计时起点
total_start = time.time()

# 间隔时间控制，每处理完一帧，只有过（0.03333 - 修正误差值）秒后才会处理
check_start = time.perf_counter()
check_end = time.perf_counter()

# 每一帧实际处理输出时间计时，用于修正每个 1/30 秒周期的误差
process_start = time.perf_counter()
process_end = time.perf_counter()

# 异步播放音乐
winsound.PlaySound(r"./BadApple.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)

i = 0
while i < 6571:
    check_end = time.perf_counter()
    # 检查间隔时间是否满足，满足则处理下一帧，否则更新 check_end
    if check_end - check_start > 0.03333 - process_end + process_start:
        process_start = time.perf_counter()
        
        # 重置光标于（0,0）
        ctypes.windll.kernel32.SetConsoleCursorPosition(hOut, INIT_POS)
        with open(r'./frames/BA (%s).txt' % str(i), 'r') as fp:
            string = "".join(fp.readlines())
            print(string + '\n frames: %s' % str(i + 1))
        check_start = time.perf_counter()
        i += 1
        
        process_end = time.perf_counter()
    else:
        check_end = time.perf_counter()
        
# 输出总运行时
total_end = time.time()
print("播放时间：%s" %(total_end - total_start))
