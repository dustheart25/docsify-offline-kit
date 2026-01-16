import os
import urllib.parse
import shutil
import re

# 始终扫描当前运行目录
root_dir = '.'
output_file = '_sidebar.md'

def clean_name(name):
    """清理文件名中的 UUID 乱码 (.pdf-xxxx...)"""
    return re.sub(r'\.pdf-.*', '', name)

def clean_files():
    """第一步：清理文件夹名称和文件后缀"""
    print("🧹 开始清理文件名和修正后缀...")
    
    # 获取当前目录下的一级文件夹
    for entry in os.listdir(root_dir):
        full_path = os.path.join(root_dir, entry)
        
        # 跳过隐藏文件和特定目录
        if entry.startswith('.') or entry in ['static', 'dist', 'scripts']:
            continue

        if os.path.isdir(full_path):
            # 1. 重命名文件夹（去掉乱码）
            new_name = clean_name(entry)
            new_path = os.path.join(root_dir, new_name)
            
            if entry != new_name:
                try:
                    os.rename(full_path, new_path)
                    print(f"   ✨ 重命名文件夹: {entry[:15]}... -> {new_name}")
                    full_path = new_path # 更新路径指向新文件夹
                except OSError as e:
                    print(f"   ⚠️ 重命名失败: {e}")

            # 2. 修正内容文件 (full -> full.md)
            # 检查文件夹里是否有 'full' 文件
            old_content = os.path.join(full_path, 'full')
            new_content = os.path.join(full_path, 'full.md')
            
            if os.path.exists(old_content) and not os.path.exists(new_content):
                os.rename(old_content, new_content)
                print(f"   📝 添加后缀: {new_name}/full -> full.md")

def generate_sidebar():
    """第二步：生成侧边栏"""
    lines = []
    print("Unh 正在生成目录结构...")

    # 再次遍历（因为刚才改名了，需要重新扫描）
    # os.walk 会递归扫描，如果只要一级目录，也可以用 listdir
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # 排序
        dirnames.sort()
        filenames.sort()
        
        # 排除目录
        if 'static' in dirpath or '/.' in dirpath or 'dist' in dirpath:
            continue

        rel_path = os.path.relpath(dirpath, root_dir)
        
        # 计算缩进层级
        if rel_path == '.':
            level = 0
        else:
            level = rel_path.count(os.sep) + 1

        # --- 处理文件夹（作为章节标题）---
        if rel_path != '.':
            indent = '  ' * (level - 1)
            folder_name = os.path.basename(dirpath)
            
            # 美化显示：把下划线变成空格 (00_Intro -> 00 Intro)
            display_name = folder_name.replace('_', ' ')
            
            # 如果文件夹里直接有 full.md，让标题可点击
            if 'full.md' in filenames:
                # 构造链接
                file_path = os.path.join(rel_path, 'full.md')
                url_path = file_path.replace('\\', '/')
                encoded_path = urllib.parse.quote(url_path)
                lines.append(f'{indent}* [{display_name}]({encoded_path})')
            else:
                # 只是个分类标题，不可点击
                lines.append(f'{indent}* **{display_name}**')

        # --- 处理独立的 .md 文件 ---
        for filename in filenames:
            # 跳过 full.md (因为上面已经作为文件夹标题处理了)
            if filename == 'full.md': 
                continue

            if filename.lower().endswith('.md') and filename.lower() != 'readme.md' and filename != '_sidebar.md':
                indent = '  ' * level
                title = os.path.splitext(filename)[0].replace('_', ' ')
                
                file_path = os.path.join(rel_path, filename)
                if rel_path == '.':
                    file_path = filename
                
                url_path = file_path.replace('\\', '/')
                encoded_path = urllib.parse.quote(url_path)
                
                lines.append(f'{indent}* [{title}]({encoded_path})')

    # 写入 _sidebar.md
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"✅ 已生成目录: {os.path.abspath(output_file)}")

    # 检查是否有 README.md
    readme_file = 'README.md'
    if not os.path.exists(readme_file):
        # 创建一个简单的封面
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(f"# 文档库\n\n欢迎阅读。\n")
        print(f"📄 已生成默认封面: {readme_file}")

if __name__ == '__main__':
    # 先清理，再生成
    clean_files()
    generate_sidebar()