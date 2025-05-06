import tkinter as tk
from tkinter import ttk
import win32api
import time
from PIL import ImageGrab


def wait_for_mouse_click():
    """等待鼠标左键点击并返回坐标"""
    while True:
        if win32api.GetAsyncKeyState(0x01) & 0x8000:
            x, y = win32api.GetCursorPos()
            while win32api.GetAsyncKeyState(0x01) & 0x8000:
                time.sleep(0.01)
            return x, y
        time.sleep(0.01)


def get_pixel_color(x, y):
    """获取屏幕指定坐标的 RGB 颜色值"""
    bbox = (x, y, x + 1, y + 1)
    im = ImageGrab.grab(bbox=bbox).convert('RGB')
    return im.getpixel((0, 0))


def pick_color():
    """颜色选取主逻辑"""
    root.withdraw()
    root.update()

    x, y = wait_for_mouse_click()
    color = get_pixel_color(x, y)

    root.deiconify()
    color_hex = '#%02X%02X%02X' % color
    update_color_display(color, color_hex)


def update_color_display(rgb, hex_code):
    """更新颜色显示区域"""
    color_label.config(bg=hex_code)
    rgb_label.config(text=f'RGB: {rgb[0]}, {rgb[1]}, {rgb[2]}')
    hex_label.config(text=f'HEX: {hex_code}')

    # 根据亮度自动调整文字颜色
    brightness = (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2])
    text_color = '#FFFFFF' if brightness < 128 else '#000000'
    color_label.config(fg=text_color, text=f'{hex_code}\nRGB: {rgb[0]},{rgb[1]},{rgb[2]}')


def create_gui():
    """创建图形界面"""
    root = tk.Tk()
    root.title("高级颜色吸管工具")
    root.resizable(False, False)

    # 现代风格主题配置
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('Accent.TButton',
                    font=('Segoe UI', 11),
                    foreground='white',
                    background='#0078d4',
                    padding=8)

    main_frame = ttk.Frame(root, padding=20)
    main_frame.pack()

    # 颜色预览标签
    global color_label, rgb_label, hex_label
    color_label = tk.Label(main_frame,
                           text="选择颜色后显示\nRGB和HEX值",
                           width=25,
                           height=8,
                           relief='groove',
                           font=('微软雅黑', 10),
                           justify='center')

    # 信息显示标签
    rgb_label = ttk.Label(main_frame,
                          text='RGB: ',
                          font=('Consolas', 12),
                          foreground='#666')

    hex_label = ttk.Label(main_frame,
                          text='HEX: ',
                          font=('Consolas', 12, 'bold'),
                          foreground='#333')

    # 操作按钮
    pick_button = ttk.Button(main_frame,
                             text="点击选取颜色",
                             command=pick_color,
                             style='Accent.TButton')

    # 布局组件
    color_label.pack(pady=15)
    pick_button.pack(pady=10, fill='x')
    rgb_label.pack(pady=3, anchor='w')
    hex_label.pack(pady=3, anchor='w')

    return root


if __name__ == "__main__":
    root = create_gui()
    root.mainloop()