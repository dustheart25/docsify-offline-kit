import os
import urllib.parse
import shutil  # <--- 1. 引入复制文件用的模块

# 始终扫描当前运行目录
root_dir = '.'
output_file = '_sidebar.md'

def generate_sidebar():
    lines = []
    # 按照文件名排序，确保顺序一致
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames.sort()
        filenames.sort()
        
        # 跳过 static 目录、隐藏目录和生成的 dist 目录
        if 'static' in dirpath or '/.' in dirpath or 'dist' in dirpath:
            continue

        rel_path = os.path.relpath(dirpath, root_dir)
        if rel_path == '.':
            level = 0
        else:
            level = rel_path.count(os.sep) + 1

        # 处理文件夹作为标题
        if rel_path != '.':
            indent = '  ' * (level - 1)
            folder_name = os.path.basename(dirpath)
            lines.append(f'{indent}* **{folder_name}**')

        # 处理文件
        for filename in filenames:
            # 只处理 .md 文件，且排除自身和 README (避免死循环或重复)
            if filename.lower().endswith('.md') and filename.lower() != 'readme.md' and filename != '_sidebar.md':
                indent = '  ' * level
                # 移除 .md 后缀作为显示名称
                title = os.path.splitext(filename)[0]
                # URL 编码路径
                file_path = os.path.join(rel_path, filename)
                if rel_path == '.':
                    file_path = filename
                
                # 替换 Windows 反斜杠
                url_path = file_path.replace('\\', '/')
                encoded_path = urllib.parse.quote(url_path)
                
                lines.append(f'{indent}* [{title}]({encoded_path})')

    # 2. 写入 _sidebar.md
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"✅ 已生成目录: {os.path.abspath(output_file)}")

    # 3. 【新增功能】如果没有 README.md，则复制一份目录作为首页
    readme_file = 'README.md'
    if not os.path.exists(readme_file):
        shutil.copyfile(output_file, readme_file)
        print(f"📄 检测到无首页，已将目录复制为: {readme_file}")
    else:
        print(f"ℹ️ 已存在首页 ({readme_file})，跳过自动生成。")

if __name__ == '__main__':
    generate_sidebar()