# ⚡ CathaySimplify — TXT 繁简体批量转换工具

> 🧭 **Cathay 工具链**：[CathayRepair](https://github.com/zzhjim02/CathayRepair) · [CathayPDG](https://github.com/zzhjim02/CathayPDG) · [CathayOCR](https://github.com/zzhjim02/CathayOCR) · [CathayRestore](https://github.com/zzhjim02/CathayRestore) · [CathayExtract](https://github.com/zzhjim02/CathayExtract) · [CathayShelf](https://github.com/zzhjim02/CathayShelf) · [CathayFinder](https://github.com/zzhjim02/CathayFinder) · **[CathayHub](https://github.com/zzhjim02/CathayHub)** · [CathayDir](https://github.com/zzhjim02/CathayDir)
> ⚠️ 本工具的功能**已并入 CathayShelf**，详见下方工具链表与说明。
> 古籍 OCR 完整工作流：批量识别 → 文字层修正 → 繁简统一与批量著录 → 双栏校勘

---


## 🔗 Cathay 人文社科工具链

> ⚠️ **本仓库已停止更新**：功能已并入后面的新一代工具（见下方「已成历史」表），这份代码保留原样、继续可用。日常建议改用 ⑦ [CathayHub](https://github.com/zzhjim02/CathayHub)。

这是一整套给人文社科研究者用的**本地**工具：从「找到一本书」，到「把它变成能搜、能读、能引用的 PDF」，再到「在上万本书里一秒检索」——每一步一个小程序，**各自独立，只挑你用得上的那一步就行**。

| 步骤 | 工具 | 一句话 | 版本 |
|:---:|---|---|---|
| ⓪ | [CathayRepair](https://github.com/zzhjim02/CathayRepair) | PDF 打不开、一翻就崩 → 先把它抢救回来 | v1.0.0 |
| ① | [CathayPDG](https://github.com/zzhjim02/CathayPDG) | 读秀 / 超星的 PDG 压缩包 → PDF | v0.1.8 |
| ② | [CathayOCR](https://github.com/zzhjim02/CathayOCR) | 扫描件做 OCR → 能搜索、能复制的 PDF | v1.2.4 |
| ③ | [CathayRestore](https://github.com/zzhjim02/CathayRestore) | 把 OCR 出来的 TXT 写回 PDF，做成双层 | v1.0.0 |
| ④ | [CathayExtract](https://github.com/zzhjim02/CathayExtract) | 已经是双层 PDF → 直接把文字抽成 TXT | v1.2.3 |
| ⑤ | [CathayShelf](https://github.com/zzhjim02/CathayShelf) | 批量建档归位、规范命名、繁简转换 | v0.4.6 |
| ⑥ | [CathayFinder](https://github.com/zzhjim02/CathayFinder) | 11 个渠道查这本书在哪（找书号 / 找路径） | v1.1.0 |
| ⑦ | [CathayHub](https://github.com/zzhjim02/CathayHub) | **索引 + 全库检索 + 浏览阅读，四合一的日常入口** | v0.3.16 |

> 🧭 **最常用的一条线**：⑥ 查到书 → ① 转成 PDF → ② 让它能搜 → ⑤ 著录归架 → ⑦ 检索、翻开。
> 每一步都能单独用，不强制串起来；整套**纯本地、不联网、不动你的原件**。

**已成历史（功能已并入后面的工具，代码还能跑）**

| 工具 | 现状 |
|---|---|
| [CathayIndex](https://github.com/zzhjim02/CathayIndex) | 已并入 ⑥ CathayFinder 的「本地文件库索引」页签，以及 ⑦ CathayHub Indexer |
| [CathayViewer](https://github.com/zzhjim02/CathayViewer) | 已并入 ⑦ CathayHub Viewer |
| [CathayReader](https://github.com/zzhjim02/CathayReader) | 已由 ⑦ CathayHub Viewer 取代 |
| **CathaySimplify（本仓库）** | 已并入 ⑤ CathayShelf 的「繁简转换 / 编码规范化」 |

**🛠️ 备用小工具（不占主线，按需取用）**

| 工具 | 什么时候想到它 |
|---|---|
| [CathayDir](https://github.com/zzhjim02/CathayDir) | 成批 PDF 摆在那儿，想先知道各自是**横排还是竖排**（分流做 OCR、挑引擎参数、建库前摸底）—— 每 10 页抽一页批量判，结果能存 CSV，也能直接分成「横排 / 竖排 / 未知」三个柜。判定算法借自 CathayPDG |

---

> 💡 **本工具的全部功能已整合进 [CathayShelf](https://github.com/zzhjim02/CathayShelf) 的「繁简转换 / 编码规范化」选项卡**，并提供批量著录建夹、产物后缀替换等扩充；本仓库继续独立维护，轻量场景仍可直接用本工具。

## 功能特点

### 🖥️ 可视化操作

- **纯图形界面**（Tkinter），免命令行操作
- 批量添加文件、文件夹递归扫描、拖放操作三合一
- 实时进度条 + 完整转换日志

### 🔄 智能转换

| 方向 | 默认后缀 | 说明 |
|------|---------|------|
| 繁体→简体 | `_【繁转简】` | 古籍繁体文本统一为简体 |
| 简体→繁体 | `_【简转繁】` | 学术出版场合将简体转回繁体 |

### 🧠 智能去重（自动跳过）

导入文件夹时自动检测，对于任意 `某文件名.txt`，若同目录下已存在以下任一文件：

- `某文件名_【繁转简】.txt`
- `某文件名【繁转简】.txt`
- `某文件名_【简转繁】.txt`
- `某文件名【简转繁】.txt`

则该文件 **自动排除**，不会出现在待处理列表中，避免重复转换造成混乱。

### 📁 灵活的输出策略

- **留空** → 每个文件输出到自己的源目录（推荐，保持文件就近管理）
- **指定目录** → 统一输出到指定文件夹

### 🌐 编码智能适配

- 自动检测输入文件编码（UTF-8 / GBK / GB2312 / BIG5 / UTF-16 ...）
- 无论输入编码如何，输出统一为 **UTF-8**
- 完美兼容 CathayOCR 和 CathayReader 的输出

### 📊 转换分析

- 一对多转换检测（同一个字有多种简/繁对应关系时列出）
- 多对一转换检测（多个不同字映射到同一个字时列出）
- 帮助研究人员了解 OpenCC 的转换规则和边界情况

---

## 快速上手

### 从源代码运行

```bash
# 1. 安装依赖
pip install opencc-python-reimplemented chardet tkinterdnd2

# 2. 运行
python converter.py
```

### 直接使用 EXE

从 [Releases](https://github.com/zzhjim02/CathaySimplify/releases) 下载 `CathaySimplify.exe`，双击即开即用，无需安装任何环境。

### 使用步骤

```
1️⃣ 打开程序  → 双击 CathaySimplify.exe
2️⃣ 添加文件  → 点「选择TXT文件」/「导入文件夹」或直接拖入
3️⃣ 选方向    → 繁体→简体 或 简体→繁体
4️⃣ 设输出    → 留空即输出到源目录（推荐）
5️⃣ 点开始    → 实时看进度条和日志
```

---

## 与 CathayOCR / CathayReader 配合使用

### 场景一：古籍 OCR → 繁简统一 → 校勘

```
CathayOCR 识别古籍 PDF
       ↓ 生成原始繁体 TXT
CathaySimplify 批量转为简体
       ↓ 统一编码的简体 TXT + 标记后缀
CathayReader 双栏校勘定稿
       ↓
  最终定稿文本
```

### 场景二：多版本 OCR 结果统一转换

CathayReader 支持多版本 OCR 结果切换（PPOCR-VL1.6、PPOCR V6 等）。选定最佳版本后，先用 CathaySimplify 将不同版本统一为同一字体方向，再由 CathayReader 加载校勘。

### 场景三：批量输出命名规范

所有转换后的文件自带 `_【繁转简】` 或 `_【简转繁】` 标记后缀，与 CathayReader 的可配置后缀体系兼容，不会与 OCR 引擎的原始输出（`_PDVL6AIFOCR`、`_layered` 等）混淆。

---

## 文件结构

```
CathaySimplify/
├── converter.py              ← 主程序（单一文件）
├── requirements.txt          ← 依赖列表
├── README.md                 ← 本文件
├── CathaySimplify.spec       ← PyInstaller 打包配置
├── test_conversion.py        ← 转换功能测试
├── test_encoding_conversion.py  ← 编码检测测试
├── test_traditional.txt      ← 繁体测试样本
├── test_gbk.txt              ← GBK 编码测试样本
├── test_gb2312.txt           ← GB2312 编码测试样本
├── test_utf8.txt             ← UTF-8 编码测试样本
└── screenshot.png            ← 界面截图
```

---

## 技术栈

| 组件 | 用途 |
|------|------|
| **Python 3.11+** | 运行环境 |
| **Tkinter** | GUI 界面（标准库，无需额外安装） |
| **tkinterdnd2** | 拖放支持 |
| **OpenCC (python-reimplemented)** | 繁简体转换引擎 — 规则精确，覆盖全面 |
| **chardet** | 自动编码检测 |
| **PyInstaller** | 打包为独立 EXE |

---

## 许可

本项目基于 **GPL-3.0 License**。

---

<div align="center">

**Cathay 人文社科工具链（9 个）**

| 🔗 项目 | 🎯 职责 |
|:-------|:--------|
| [CathayRepair](https://github.com/zzhjim02/CathayRepair) | 打不开的 PDF 抢救回来 |
| [CathayPDG](https://github.com/zzhjim02/CathayPDG) | 读秀 / 超星 PDG 批量转 PDF |
| [CathayOCR](https://github.com/zzhjim02/CathayOCR) | 多引擎 GPU 加速 PDF 批量 OCR |
| [CathayRestore](https://github.com/zzhjim02/CathayRestore) | OCR 的 TXT 写回 PDF 文字层 |
| [CathayExtract](https://github.com/zzhjim02/CathayExtract) | 双层 PDF 抽出 TXT |
| [CathayShelf](https://github.com/zzhjim02/CathayShelf) | 著录归档 / 命名规范 / **繁简转换（含本工具全部功能）** |
| [CathayFinder](https://github.com/zzhjim02/CathayFinder) | 11 个渠道查书 |
| **[CathayHub](https://github.com/zzhjim02/CathayHub)** | **索引 + 全库检索 + 浏览阅读（日常入口）** |
| [CathayDir](https://github.com/zzhjim02/CathayDir) | 批量判断 PDF 是**横排还是竖排**（OCR 前分流用） |

</div>
