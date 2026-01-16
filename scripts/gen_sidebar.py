import os
import urllib.parse

# 始终扫描当前运行目录
root_dir = '.'
output_file = '_sidebar.md'

def generate_sidebar():
    lines = []
    # 按照文件名排序，确保顺序一致
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames.sort()
        filenames.sort()
        
        # 跳过 static 目录和隐藏目录
        if 'static' in dirpath or '/.' in dirpath:
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

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"✅ 已生成目录: {os.path.abspath(output_file)}")

if __name__ == '__main__':
    generate_sidebar()