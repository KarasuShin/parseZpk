import os
import json
import shutil
import pandas as pd
import requests

# 定义要搜索的目录
directory = '.'  # 替换为你要搜索的目录
anki_import_dir = 'anki_import'  # 定义目标目录
output_file = 'anki_import/anki_output.csv'  # 输出 CSV 文件名


def download_audio(word):
    audio_file = os.path.join(anki_import_dir, f"{word}.mp3")
    if not os.path.isfile(audio_file):  # 如果文件不存在，则下载
        url = f"https://dict.youdao.com/dictvoice?type=0&audio={word}"
        response = requests.get(url)
        if response.status_code == 200:
            with open(audio_file, 'wb') as f:
                f.write(response.content)
            print(f"下载音频: {audio_file}")
        else:
            print(f"下载失败: {url}，状态码: {response.status_code}")
os.makedirs(anki_import_dir, exist_ok=True)

# 用于存储数据的列表
data = []

# 遍历目录及其子目录
for root, dirs, files in os.walk(directory):
    for file in files:
        if file == 'word.json':
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    # 读取 JSON 内容
                    word_data = json.load(f)
                    
                    # 提取所需字段
                    word = word_data.get('word', '')
                    accent = word_data.get('accent', '')
                    image_file = word_data.get('image_file', '')
                    mean_cn = word_data.get('mean_cn', '')
                    word_etyma = word_data.get('word_etyma', '')
                    # 复制图片文件到 anki_import 目录
                    if image_file:
                        image_source_path = os.path.join(root, image_file)
                        if os.path.isfile(image_source_path):
                            shutil.copy(image_source_path, anki_import_dir)
                    # 组装正面和背面字段
                    front = f"""
<div style="text-align: center;">
    <img src='{image_file}' style="max-width: 100%; height: auto;">
    <div>{word}</div>
    <div>{accent}</div>
    <div>{mean_cn}</div>
    [sound:{word}.mp3]
</div>
"""

                    back = word_etyma
                    
                    # 添加到数据列表
                    data.append({'Front': front, })      # 下载音频
                    download_audio(word)
                    
                except json.JSONDecodeError:
                    print(f"无法解析文件: {file_path}")

# 将数据写入 CSV 文件
df = pd.DataFrame(data)
df.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"已成功写入 {output_file}")
