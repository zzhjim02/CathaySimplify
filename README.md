# ⚡ CathaySimplify — TXT 繁简体批量转换工具

> **CathayOCR → CathayRestore → CathaySimplify / CathayShelf → CathayReader**
> 古籍 OCR 完整工作流：批量识别 → 文字层修正 → 繁简统一与批量著录 → 双栏校勘

---

## 🧩 Cathay 人文研究工具链

<div align="center">

| 步骤 | 工具 | 功能 | 状态 |
|:----:|:----|:----|:----:|
| ⓪ | [**CathayRepair**</br>![GitHub](https://img.shields.io/github/stars/zzhjim02/CathayRepair?style=social)](https://github.com/zzhjim02/CathayRepair) | 🩹 抢救损伤 PDF：逐页复制、跳过坏页 | ✅ v1.0.0 |
| ① | [**CathayOCR**</br>![GitHub](https://img.shields.io/github/stars/zzhjim02/CathayOCR?style=social)](https://github.com/zzhjim02/CathayOCR) | 📄 多引擎 GPU 加速</br>古籍 PDF 批处理 OCR | ✅ 已发布 v1.2.4 |
| ② | [**CathayRestore**</br>![GitHub](https://img.shields.io/github/stars/zzhjim02/CathayRestore?style=social)](https://github.com/zzhjim02/CathayRestore) | 🔎 TXT 文本层写回 PDF</br>竖排 · 透明 · 可搜索 | ✅ 已发布 v1.0.0 |
| ③ | **⭐ CathaySimplify**</br>![GitHub](https://img.shields.io/github/stars/zzhjim02/CathaySimplify?style=social) | 🔄 **TXT 繁简体双向转换**</br>编码智能适配 · 智能去重 | 🆕 **你在这里** |
| ④ | [**CathayShelf**</br>![GitHub](https://img.shields.io/github/stars/zzhjim02/CathayShelf?style=social)](https://github.com/zzhjim02/CathayShelf) | 🗂️ 批量著录建夹 · 后缀替换</br>已整合本工具全部功能并扩充 | ✅ 已发布 v0.4.3 |
| ⑤ | [**CathayReader**</br>![GitHub](https://img.shields.io/github/stars/zzhjim02/CathayReader?style=social)](https://github.com/zzhjim02/CathayReader) | 📖 PDF/TXT 双栏同步</br>古籍校勘阅读器 | ✅ 已发布 v1.0.0 |
| ✳ | [**CathayExtract**</br>![GitHub](https://img.shields.io/github/stars/zzhjim02/CathayExtract?style=social)](https://github.com/zzhjim02/CathayExtract) | 🔎 已有双层 PDF → 提取文字层成 TXT | ✅ v1.2.0 |

</div>

```
┌─────────────────────────────────────────────────────────┐
│                   📚 典型工作流                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ① CathayOCR                                            │
│     古籍 PDF 扫描件 → 批量 OCR → 繁体 TXT + 双层 PDF    │
│                        │                                │
│                        ▼                                │
│  ② CathaySimplify  ← ⭐ 本工具                          │
│     繁体 TXT → 批量转为简体 / 简体→繁体                  │
│                        │                                │
│                        ▼                                │
│  ③ CathayReader                                         │
│     PDF 原图 + 简体 TXT 双栏对照校勘 → 定稿              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

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

**Cathay 工具链三部曲**

| 🔗 项目 | 📦 仓库 | 🎯 职责 |
|:-------|:--------|:--------|
| CathayOCR | [github.com/zzhjim02/CathayOCR](https://github.com/zzhjim02/CathayOCR) | 多引擎 GPU 加速 PDF 批量 OCR |
| **CathaySimplify** | **github.com/zzhjim02/CathaySimplify** | **TXT 繁简体批量双向转换** |
| CathayReader | [github.com/zzhjim02/CathayReader](https://github.com/zzhjim02/CathayReader) | PDF/TXT 双栏同步古籍校勘阅读器 |

⭐ **从扫描件到定稿，一条命令都不用敲。**

</div>
