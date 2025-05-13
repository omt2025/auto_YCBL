import os
import cv2
import numpy as np
import pyautogui

import time
import random



# 模板图片的目录
template_dir = 'assets'
template_names = ['item_1.png', 'item_2.png', 'item_3.png']
template_paths = [os.path.join(template_dir, name) for name in template_names]

for path in template_paths:
    print(f"检查文件是否存在: {path} --> {os.path.exists(path)}")

# 截图屏幕
screenshot = pyautogui.screenshot()
screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

# 遍历每个模板
for template_path in template_paths:
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    if template is None:
        print(f"❌ 无法读取模板图像: {template_path}")
        continue

    h, w = template.shape[:2]

    # 模板匹配
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    print(f"{template_path} 匹配度: {max_val:.2f}")

    # 设置匹配阈值
    threshold = 0.5
    if max_val >= threshold:
        top_left = max_loc
        center_x = top_left[0] + w // 2
        center_y = top_left[1] + h // 2

        # 点击
        pyautogui.moveTo(center_x, center_y, duration=0.2)
        pyautogui.click()
        print(f"点击 {template_path} at ({center_x}, {center_y})")
        wait_time = random.uniform(2, 3)
        print(f"等待 {wait_time:.2f} 秒")
        time.sleep(wait_time)
    else:
        print(f"{template_path} 未找到或匹配度低")
