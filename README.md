# 📚 Docsify Offline Kit (高性能离线知识库套件)

这是一个开箱即用的 Docsify 部署套件，专为**内网、弱网或对数据隐私有高要求**的环境设计。
它集成了 MathJax V3 引擎和全套本地字体库，彻底解决了在线 CDN 加载慢、公式渲染卡顿、数学符号乱码等问题。

## ✨ 核心特性

* **⚡ 极速离线体验**：内置所有核心插件（搜索、缩放、分页）和 MathJax V3 引擎，不依赖任何外部 CDN，断网也能秒开。
* **🧮 完美公式支持**：采用 `CHTML` 模式配合本地 `.woff` 字体库，渲染速度比旧版快 10 倍，完美支持复杂药理学/数学公式。
* **🤖 自动化部署**：
    * **自动纠错**：自动将 Linux 敏感的 `readme.md` 修正为 `README.md`。
    * **自动目录**：自动扫描子文件夹生成 `_sidebar.md` 侧边栏。
    * **自动导航**：自动生成带 UTF-8 编码的首页，并列出所有书籍。
* **💾 零空间浪费**：部署脚本使用**硬链接 (Hard Link)** 技术，发布目录不占用额外的硬盘空间。

---

## 🚀 快速开始 (3分钟上线)

### 1. 克隆项目 (傻瓜式操作)
为了避免权限报错，**强烈建议**直接按照下方命令操作，将项目部署在 `/opt/` 目录下：

```bash
# 1. 进入 /opt 目录
cd /opt

# 2. 克隆项目 (请将下面链接中的“你的用户名”替换为实际用户名)
git clone https://github.com/dustheart25/docsify-offline-kit.git

# 3. 进入项目文件夹
cd docsify-offline-kit
```

### 2. 放入你的书籍
将你的 Markdown 文件夹（或 PDF 转换后的文件夹）直接放入 books/ 目录下。 支持多本书，每本书一个子文件夹。

目录结构示例：
books/
├── drug-guide/       <-- 书籍 A (文件夹名即为书名)
│   ├── README.md     <-- 书籍首页
│   └── 01_Chapter.md
└── my-notes/         <-- 书籍 B
    └── README.md
### 3. 一键部署
运行部署脚本，它会自动组装资源、生成目录、修复权限并启动 Docker。  

```bash
chmod +x deploy.sh
./deploy.sh
```
### 4. 访问
打开浏览器访问：http://localhost:3009 (注：端口可在 docker-compose.yml 中修改)

## ⚠️ 避坑指南 (必读)

### 1. 部署路径选择
**❌ 严禁** 将项目克隆到 `/root/` 目录下。
原因：Docker 容器内的 Nginx 运行在普通用户权限下，无法读取 `/root/` 下的文件，会导致 **403 Forbidden** 错误。

**✅ 推荐路径**：
* `/opt/docsify-offline-kit/`
* `/home/ubuntu/docsify-offline-kit/`

### 2. 权限问题
部署脚本会自动处理 `dist` 目录的权限（自动执行 `chmod 755`）。
如果你依然遇到 403 错误，通常是因为**父目录**权限过严。请尝试放开父目录权限：

```bash
# 赋予当前目录及其父级可读权限
chmod 755 .
```

### 项目结构说明
```plaintext
.
├── books/                 # [用户区] 把你的书放这里
├── static/                # [核心区] 本地化静态资源 (JS/CSS/Fonts)
├── template/              # [模板] 书籍通用入口模板 (已配置本地化引用)
├── scripts/               # [工具] 自动生成侧边栏脚本
├── deploy.sh              # [脚本] 自动化部署脚本 (硬链接+权限修复)
├── docker-compose.yml     # Docker 启动配置
└── nginx_config.conf      # Nginx 配置 (优化 Markdown 渲染)
```