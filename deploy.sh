#!/bin/bash

# 定义颜色输出
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}==> 1. 清理旧构建...${NC}"
rm -rf dist
mkdir -p dist

echo -e "${GREEN}==> 2. 部署公共静态资源 (硬链接模式)...${NC}"
cp -al static dist/static

echo -e "${GREEN}==> 3. 部署图书馆大厅...${NC}"

# 🔴 修复点1：生成带有 UTF-8 编码声明的标准 HTML 首页，并自动列出书籍链接
cat > dist/index.html <<EOF
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>知识库入口</title>
    <style>
        body { font-family: -apple-system, "Microsoft YaHei", sans-serif; padding: 50px; text-align: center; background-color: #f4f4f4; }
        .container { background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); max-width: 600px; margin: 0 auto; }
        h1 { color: #42b983; margin-bottom: 1.5rem; }
        .book-list { text-align: left; }
        .book-item { margin: 10px 0; padding: 10px; border-bottom: 1px solid #eee; }
        a { text-decoration: none; color: #333; font-weight: bold; font-size: 1.2rem; }
        a:hover { color: #42b983; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 My Knowledge Base</h1>
        <div class="book-list">
EOF

echo -e "${GREEN}==> 4. 开始处理书籍...${NC}"

# 遍历 books 目录下的每一个子文件夹
for book_path in books/*; do
    if [ -d "$book_path" ]; then
        book_name=$(basename "$book_path")
        echo "   -> 正在处理书籍: $book_name"

        mkdir -p "dist/$book_name"
        cp -al "$book_path"/* "dist/$book_name/"
        cp template/index.html "dist/$book_name/index.html"

        # 修正大小写
        find "dist/$book_name" -iname "readme.md" -exec sh -c 'mv "$1" "$(dirname "$1")/README.md"' _ {} \;
        
        # 生成侧边栏
        if [ -f "scripts/gen_sidebar.py" ]; then
            cd "dist/$book_name"
            python3 ../../scripts/gen_sidebar.py
            cd ../..
        fi

        # 🔴 修复点1续：自动往首页插入这本书的链接
        echo "<div class='book-item'>📖 <a href='/$book_name/'>$book_name</a></div>" >> dist/index.html
    fi
done

# 🔴 修复点1完：闭合 HTML 标签
cat >> dist/index.html <<EOF
        </div>
        <p style="color:#999; margin-top:20px; font-size:0.9rem;">Powered by Docsify Offline Kit</p>
    </div>
</body>
</html>
EOF

echo -e "${GREEN}==> 5. 修正文件权限 (解决 403 Forbidden)...${NC}"
# 🔴 修复点2：给 dist 目录赋予 755 权限，让 Docker 里的 Nginx 能读取
chmod -R 755 dist

echo -e "${GREEN}==> 6. 启动 Docker 服务...${NC}"
docker compose up -d --build

echo "🔧 正在执行最终权限修复 (chmod 755)..."
chmod 755 /opt/docsify-offline-kit
chmod -R 755 /opt/docsify-offline-kit
docker compose restart

echo -e "${GREEN}✅ 部署完成！${NC}"
echo -e "访问地址: http://localhost:3009"