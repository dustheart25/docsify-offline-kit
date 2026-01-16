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

## 🚀 快速开始 (3分钟上线)

### 1. 克隆项目
```bash
git clone [https://github.com/你的用户名/docsify-offline-kit.git](https://github.com/你的用户名/docsify-offline-kit.git)
cd docsify-offline-kit
