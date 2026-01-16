#!/bin/bash

# 定义颜色输出，看起来更专业
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}==> 1. 清理旧构建...${NC}"
rm -rf dist
mkdir -p dist

echo -e "${GREEN}==> 2. 部署公共静态资源 (硬链接模式)...${NC}"
# 使用 -al 创建硬链接，秒级复制且不占额外空间
cp -al static dist/static

echo -e "${GREEN}==> 3. 部署图书馆大厅...${NC}"
# 如果有 portal/index.html 就用，没有就生成默认的
if [ -d "portal" ] && [ -f "portal/index.html" ]; then
    cp portal/index.html dist/index.html
else
    echo "<h1>📚 My Knowledge Base</h1><p>请在 books/ 目录下添加书籍。</p>" > dist/index.html
fi

echo -e "${GREEN}==> 4. 开始处理书籍...${NC}"

# 遍历 books 目录下的每一个子文件夹
for book_path in books/*; do
    if [ -d "$book_path" ]; then
        book_name=$(basename "$book_path")
        echo "   -> 正在处理书籍: $book_name"

        mkdir -p "dist/$book_name"
        
        # 硬链接复制书籍内容
        cp -al "$book_path"/* "dist/$book_name/"

        # 注入标准模板 (index.html)
        cp template/index.html "dist/$book_name/index.html"

        # 【智能修复】强制修正 README.md 大小写 (Linux敏感)
        find "dist/$book_name" -iname "readme.md" -exec sh -c 'mv "$1" "$(dirname "$1")/README.md"' _ {} \;
        
        # 【自动生成】调用 Python 生成侧边栏
        if [ -f "scripts/gen_sidebar.py" ]; then
            cd "dist/$book_name"
            python3 ../../scripts/gen_sidebar.py
            cd ../..
        fi
    fi
done

echo -e "${GREEN}==> 5. 启动 Docker 服务...${NC}"
docker compose up -d --build

echo -e "${GREEN}✅ 部署完成！${NC}"
echo -e "访问地址: http://localhost:3009"