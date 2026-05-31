import tkinter as tk
import random
import math
import time

# 配置参数
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
WINDOW_WIDTH = 160
WINDOW_HEIGHT = 70
TOTAL_WINDOWS = 100    # 爱心便签数量
MAX_TRY = 500          # 尝试多少次找不到空位就认为屏幕满了
BATCH_SIZE = 3         # 每批同时生成几个便签
COLORS = ["#FFB6C1", "#87CEEB", "#98FB98", "#FFA07A", "#DDA0DD", "#F0E68C"]  # 便签背景色
TEXTS = [
    "每天都要开心呀", "好好吃饭哦", "别太累啦", "记得多喝水",
    "早点睡呀", "照顾好自己", "万事顺心～", "笑容常在呀",
    "好好生活", "放宽心哦", "元气满满每一天", "三餐都要好好吃",
    "愿你事事顺利", "好好休息呀", "保持好心情", "别胡思乱想啦",
    "日子甜甜的", "一定要快乐", "平安喜乐呀", "慢慢来就好",
    "我想你了", "我想你了", "我想你了", "我想你了",
]

def generate_heart_points(count, sw, sh, ww, wh):
    """生成爱心形状的坐标点"""
    points = []
    scale = min(sw, sh) / 50  # 爱心大小缩放
    center_x, center_y = sw // 2, sh // 2 - 50  # 爱心中心位置
    for i in range(count):
        t = i / count * 2 * math.pi
        # 心形线参数方程
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        # 坐标转换到屏幕上
        px = center_x + x * scale - ww // 2 
        py = center_y - y * scale - wh // 2
        points.append((px, py))
    return points


def create_note_window(x, y, text, color, fade_in=True):
    """创建单个便签窗口，可选渐进淡入效果"""
    win = tk.Toplevel()
    win.title(text)
    win.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{int(x)}+{int(y)}")
    win.configure(bg=color)

    # 添加文字标签
    label = tk.Label(win, text=text, font=("微软雅黑", 11, "bold"), bg=color, fg="black")
    label.pack(expand=True)

    # 空格键退出整个程序
    win.bind("<space>", lambda e: win.master.destroy())

    if fade_in:
        win.attributes("-alpha", 0.0)  # 初始完全透明
        _fade_in(win)

    return win


def _fade_in(win, step=0, total=10):
    """渐进淡入：分 10 步从透明到不透明"""
    alpha = (step + 1) / total
    try:
        win.attributes("-alpha", alpha)
    except tk.TclError:
        return  # 窗口已被关闭
    if step < total - 1:
        win.after(30, lambda: _fade_in(win, step + 1, total))


if __name__ == "__main__":
    print("程序启动中...")
    try:
        # 初始化主窗口（隐藏）
        root = tk.Tk()
        root.withdraw()
        root.title("爱心便签")
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        print(f"屏幕分辨率: {sw}x{sh}")

        # 生成爱心坐标
        points = generate_heart_points(TOTAL_WINDOWS, sw, sh, WINDOW_WIDTH, WINDOW_HEIGHT)
        all_windows = []

        # 动态弹出窗口
        print(f"开始创建 {TOTAL_WINDOWS} 个便签窗口...")
        for i, (x, y) in enumerate(points):
            text = random.choice(TEXTS)
            color = random.choice(COLORS)
            win = create_note_window(x, y, text, color)
            all_windows.append(win)
            root.update()
            time.sleep(0.01)  # 控制弹出速度，越小越快

        # 收集所有已占用的位置（用于碰撞检测）
        occupied = []  # [(x, y, w, h), ...]

        def is_overlapping(x, y):
            """检查新窗口是否与已有窗口重叠"""
            for ox, oy, ow, oh in occupied:
                if (x < ox + ow and x + WINDOW_WIDTH > ox and
                    y < oy + oh and y + WINDOW_HEIGHT > oy):
                    return True
            return False

        def find_empty_spot():
            """找一个不重叠的位置，连续尝试失败返回 None"""
            for _ in range(MAX_TRY):
                rx = random.randint(0, sw - WINDOW_WIDTH)
                ry = random.randint(0, sh - WINDOW_HEIGHT)
                if not is_overlapping(rx, ry):
                    return rx, ry
            return None

        print("爱心便签已全部创建！开始全屏随机飘洒...")

        def random_spawn():
            """全屏随机生成便签，永不停止，空格键手动退出"""
            rx = random.randint(0, sw - WINDOW_WIDTH)
            ry = random.randint(0, sh - WINDOW_HEIGHT)
            text = random.choice(TEXTS)  
            color = random.choice(COLORS)
            create_note_window(rx, ry, text, color)
            root.after(random.randint(10, 40), random_spawn)

        # 爱心窗口的位置也加入已占用列表
        for x, y in points:
            occupied.append((x, y, WINDOW_WIDTH, WINDOW_HEIGHT))

        # 爱心展示完等 0.5 秒后开始随机飘洒
        root.after(500, random_spawn)

        # 15 秒后自动关闭程序，防止窗口太多电脑卡死
        root.after(15000, root.destroy)
        root.mainloop()
        print("程序已退出")
    except Exception as e:
        print(f"出错了: {e}")
        import traceback
        traceback.print_exc()
        input("按回车键退出...")
