# -*- coding: utf-8 -*-
"""
CathaySimplify - 批量 TXT 繁简体转换工具
支持：选文件、导入文件夹、拖入文件/文件夹、智能去重、默认输出到源目录
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import opencc
import threading
import os
import chardet
import re

# ── 尝试加载拖放支持 ──────────────────────────────────────────────
HAS_DND = False
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    HAS_DND = True
except ImportError:
    pass


# ═══════════════════════════════════════════════════════════════════
#  工具函数
# ═══════════════════════════════════════════════════════════════════

# 所有需要检查的输出变体后缀（带下划线 + 不带下划线，两种方向）
OUTPUT_SUFFIXES_T2S = ["_【繁转简】", "【繁转简】"]
OUTPUT_SUFFIXES_S2T = ["_【简转繁】", "【简转繁】"]


def _strip_ext(name: str) -> str:
    """去掉后缀 .TXT/.txt，返回纯文件名主干"""
    # splitext 区分大小写，统一小写比较
    if name.lower().endswith(".txt"):
        return name[:-4]
    return name


def _has_output_variant(dirpath: str, basename_stem: str) -> bool:
    """检查目录下是否存在任意输出变体"""
    for suffix in OUTPUT_SUFFIXES_T2S + OUTPUT_SUFFIXES_S2T:
        candidate = os.path.join(dirpath, f"{basename_stem}{suffix}.txt")
        if os.path.exists(candidate):
            return True
    return False


def _is_output_file(filename: str) -> bool:
    """判断文件名本身是否属于输出变体"""
    stem = _strip_ext(filename)
    lower = stem.lower()
    for suffix in OUTPUT_SUFFIXES_T2S + OUTPUT_SUFFIXES_S2T:
        if lower.endswith(suffix.lower()):
            return True
    return False


def scan_folder_for_txt(folder_path: str) -> list:
    """递归扫描文件夹，返回需要处理的 TXT 文件列表（已排除输出变体 & 已转换过的）"""
    result = []
    for root, dirs, files in os.walk(folder_path):
        for f in files:
            if not f.lower().endswith(".txt"):
                continue
            # 跳过本身就是输出变体的文件
            if _is_output_file(f):
                continue
            # 检查是否已有对应的输出变体存在
            stem = _strip_ext(f)
            if _has_output_variant(root, stem):
                continue
            # 通过检查
            result.append(os.path.join(root, f))
    return result


def parse_dropped_paths(data: str) -> list:
    """解析 tkinterdnd 拖放返回的路径字符串，返回合法路径列表"""
    raw_paths = []
    # tkdnd 返回的花括号分组格式：{path1} {path2} ...
    # 或者没有花括号的简单路径
    # 用正则提取 {} 内的内容
    brace_pattern = re.findall(r'\{([^}]+)\}', data)
    if brace_pattern:
        raw_paths = brace_pattern
    else:
        # 空格分隔
        raw_paths = data.split()

    valid = []
    for p in raw_paths:
        p = p.strip().strip('"').strip("'")
        if os.path.exists(p):
            valid.append(p)
    return valid


# ═══════════════════════════════════════════════════════════════════
#  主程序类
# ═══════════════════════════════════════════════════════════════════

class CathaySimplify:
    """CathaySimplify 主窗口"""

    def __init__(self, root):
        self.root = root
        self.root.title("CathaySimplify - 繁简体转换工具")
        self.root.geometry("900x700")

        # ── 数据 ──
        self.file_list: list[tuple[str, str]] = []  # (full_path, display_name)
        # 拖放时暂存，防止被 GC
        self._drop_target_refs = []

        # ── 构建 UI ──
        self.create_ui()
        self.setup_drag_drop()

    # ───────────────────────── UI 构建 ─────────────────────────

    def create_ui(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # ── 文件选择区域 ──
        file_frame = ttk.LabelFrame(main_frame, text="文件选择（支持拖放）", padding="10")
        file_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)

        btn_frame = ttk.Frame(file_frame)
        btn_frame.grid(row=0, column=0, columnspan=2, sticky="w")

        ttk.Button(btn_frame, text="📄 选择TXT文件", command=self.select_files).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="📁 导入文件夹", command=self.import_folders).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="🗑 清空列表", command=self.clear_files).pack(side=tk.LEFT, padx=(0, 5))

        self.file_count_label = ttk.Label(btn_frame, text="已选择 0 个文件")
        self.file_count_label.pack(side=tk.LEFT, padx=(15, 0))
        ttk.Label(btn_frame, text="💡 支持拖放文件/文件夹到列表区域",
                  foreground="gray").pack(side=tk.LEFT, padx=(10, 0))

        # 文件列表 + 滚动条
        list_frame = ttk.Frame(main_frame)
        list_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.file_listbox = tk.Listbox(
            list_frame, yscrollcommand=scrollbar.set,
            selectmode=tk.SINGLE, font=("Microsoft YaHei UI", 9)
        )
        self.file_listbox.grid(row=0, column=0, sticky="nsew")
        scrollbar.config(command=self.file_listbox.yview)

        # ── 转换设置区域 ──
        settings_frame = ttk.LabelFrame(main_frame, text="转换设置", padding="10")
        settings_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        settings_frame.columnconfigure(1, weight=1)

        # 行 0：转换方向 + 输出目录
        self.direction_var = tk.StringVar(value="t2s")
        direction_frame = ttk.Frame(settings_frame)
        direction_frame.grid(row=0, column=0, sticky="w", padx=(0, 20))

        ttk.Label(direction_frame, text="转换方向：").pack(side=tk.LEFT)
        rb_t2s = ttk.Radiobutton(
            direction_frame, text="繁体→简体",
            variable=self.direction_var, value="t2s",
            command=self._on_direction_change
        )
        rb_t2s.pack(side=tk.LEFT, padx=(10, 5))
        rb_s2t = ttk.Radiobutton(
            direction_frame, text="简体→繁体",
            variable=self.direction_var, value="s2t",
            command=self._on_direction_change
        )
        rb_s2t.pack(side=tk.LEFT, padx=(0, 5))

        ttk.Label(settings_frame, text="输出目录：").grid(row=0, column=1, sticky="w", padx=(0, 5))
        self.output_path_var = tk.StringVar(value="")  # 空 = 使用源文件目录
        self.output_entry = ttk.Entry(
            settings_frame, textvariable=self.output_path_var, width=40
        )
        self.output_entry.grid(row=0, column=2, sticky="ew", padx=(0, 5))
        self.output_entry.insert(0, "")  # 默认空
        ttk.Button(settings_frame, text="浏览", command=self.select_output_dir).grid(
            row=0, column=3, sticky="w"
        )
        ttk.Label(settings_frame, text="（留空 = 输出到原文件所在目录）",
                  foreground="gray", font=("", 8)).grid(
            row=0, column=4, sticky="w", padx=(5, 0)
        )

        # 行 1：文件命名
        name_frame = ttk.Frame(settings_frame)
        name_frame.grid(row=1, column=0, columnspan=5, sticky="w", pady=(8, 0))

        ttk.Label(name_frame, text="文件命名：").pack(side=tk.LEFT)
        self.naming_var = tk.StringVar(value="suffix")
        ttk.Radiobutton(
            name_frame, text="添加后缀", variable=self.naming_var,
            value="suffix", command=self._on_naming_change
        ).pack(side=tk.LEFT, padx=(10, 5))
        ttk.Radiobutton(
            name_frame, text="覆盖原文件", variable=self.naming_var,
            value="overwrite"
        ).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Label(name_frame, text="后缀：").pack(side=tk.LEFT, padx=(15, 5))
        self.suffix_var = tk.StringVar(value="_【繁转简】")
        self.suffix_entry = ttk.Entry(name_frame, textvariable=self.suffix_var, width=18)
        self.suffix_entry.pack(side=tk.LEFT, padx=(0, 5))

        # ── 进度区域 ──
        progress_frame = ttk.LabelFrame(main_frame, text="转换进度", padding="10")
        progress_frame.grid(row=3, column=0, sticky="ew", pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)

        self.progress = ttk.Progressbar(progress_frame, mode="determinate")
        self.progress.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        self.status_label = ttk.Label(progress_frame, text="就绪")
        self.status_label.grid(row=1, column=0, sticky="w")

        # ── 操作按钮 ──
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=4, column=0, pady=(0, 10))
        self.convert_button = ttk.Button(
            action_frame, text="▶ 开始转换", command=self.start_conversion
        )
        self.convert_button.pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="退出", command=self.root.quit).pack(
            side=tk.LEFT, padx=5
        )

        # ── 日志区域 ──
        log_frame = ttk.LabelFrame(main_frame, text="转换日志", padding="10")
        log_frame.grid(row=5, column=0, sticky="nsew")
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

        self.log_text = scrolledtext.ScrolledText(
            log_frame, height=8, wrap=tk.WORD,
            font=("Consolas", 9)
        )
        self.log_text.grid(row=0, column=0, sticky="nsew")
        self.log_text.tag_config("info", foreground="black")
        self.log_text.tag_config("success", foreground="green")
        self.log_text.tag_config("error", foreground="red")
        self.log_text.tag_config("warning", foreground="orange")

    # ───────────────────────── 拖放支持 ─────────────────────────

    def setup_drag_drop(self):
        """注册文件/文件夹拖放"""
        if not HAS_DND:
            self.log_message("💡 提示：安装 tkinterdnd2 可启用拖放功能", "warning")
            self.log_message("   pip install tkinterdnd2", "warning")
            return

        # 为整个窗口和列表注册拖放
        targets = [self.file_listbox, self.root]
        for widget in targets:
            widget.drop_target_register(DND_FILES)
            widget.dnd_bind("<<Drop>>", self.on_drop)
            self._drop_target_refs.append(widget)

        self.log_message("✅ 拖放功能已就绪", "success")

    def on_drop(self, event):
        """处理拖放事件"""
        data = getattr(event, "data", "")
        if not data:
            return

        paths = parse_dropped_paths(data)
        if not paths:
            return

        added_count = 0
        for path in paths:
            if os.path.isfile(path):
                if path.lower().endswith(".txt"):
                    if self._add_single_file(path):
                        added_count += 1
                else:
                    self.log_message(f"⏭ 跳过非 TXT 文件：{os.path.basename(path)}", "warning")
            elif os.path.isdir(path):
                found = scan_folder_for_txt(path)
                count = self._add_multiple_files(found)
                if count > 0:
                    added_count += count
                    self.log_message(f"📁 从文件夹扫入 {count} 个文件：{path}", "info")

        if added_count > 0:
            self.log_message(f"✅ 拖放完成，新增 {added_count} 个文件", "success")

    # ───────────────────────── 文件操作 ─────────────────────────

    def select_files(self):
        """选择单个或多个 TXT 文件"""
        files = filedialog.askopenfilenames(
            title="选择 TXT 文件",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        if not files:
            return
        count = self._add_multiple_files(files)
        if count > 0:
            self.log_message(f"📄 添加了 {count} 个文件", "info")

    def import_folders(self):
        """导入一个或多个文件夹"""
        folders = filedialog.askdirectory(title="选择要扫描的文件夹（可多次添加）")
        if not folders:
            return

        # 支持多次选择，用单次循环 + 递归
        found = scan_folder_for_txt(folders)
        if not found:
            self.log_message(f"⏭ 未在文件夹中发现需要处理的 TXT 文件：{folders}", "info")
            return

        count = self._add_multiple_files(found)
        self.log_message(f"📁 导入文件夹，新增 {count} 个文件：{folders}", "info")

    def clear_files(self):
        """清空文件列表"""
        self.file_list.clear()
        self.file_listbox.delete(0, tk.END)
        self.file_count_label.config(text="已选择 0 个文件")
        self.progress["value"] = 0
        self.status_label.config(text="已清空")
        self.log_message("🗑 已清空文件列表", "info")

    def _add_single_file(self, full_path: str) -> bool:
        """添加单个文件到列表（去重 + 排除检查），返回是否成功添加"""
        # 去重
        for existing_path, _ in self.file_list:
            if os.path.abspath(existing_path) == os.path.abspath(full_path):
                return False

        # 跳过输出变体文件
        filename = os.path.basename(full_path)
        if _is_output_file(filename):
            self.log_message(f"⏭ 跳过输出文件：{filename}", "warning")
            return False

        # 检查是否已被转换
        parent = os.path.dirname(full_path)
        stem = _strip_ext(filename)
        if _has_output_variant(parent, stem):
            self.log_message(f"⏭ 跳过已转换文件：{filename}", "warning")
            return False

        # 显示名：文件名，若有重名则加父目录名
        display = self._make_display_name(full_path, filename)
        self.file_list.append((full_path, display))
        self.file_listbox.insert(tk.END, display)
        self._update_file_count()
        return True

    def _add_multiple_files(self, paths: list) -> int:
        """批量添加文件，返回成功添加的数量"""
        count = 0
        for p in paths:
            if self._add_single_file(p):
                count += 1
        self._update_file_count()
        return count

    def _make_display_name(self, full_path: str, filename: str) -> str:
        """生成显示名：简单文件名，若重名则加父文件夹名"""
        # 检查是否有同文件名的冲突
        for existing_path, _ in self.file_list:
            if os.path.basename(existing_path) == filename:
                # 冲突，附带父文件夹名区分
                parent_folder = os.path.basename(os.path.dirname(full_path))
                return f"{parent_folder}\\{filename}"
        return filename

    def _update_file_count(self):
        self.file_count_label.config(text=f"已选择 {len(self.file_list)} 个文件")

    # ───────────────────────── 设置交互 ─────────────────────────

    def _on_direction_change(self):
        """切换转换方向时自动更新默认后缀"""
        if self.direction_var.get() == "t2s":
            # 只有当前后缀与 s2t 默认值相同时才自动切换
            current = self.suffix_var.get()
            if current in ("_【简转繁】", "_【繁转简】"):
                self.suffix_var.set("_【繁转简】")
        else:
            current = self.suffix_var.get()
            if current in ("_【简转繁】", "_【繁转简】"):
                self.suffix_var.set("_【简转繁】")

    def _on_naming_change(self):
        """切换命名方式时的处理"""
        if self.naming_var.get() == "overwrite":
            self.suffix_entry.config(state="disabled")
        else:
            self.suffix_entry.config(state="normal")

    def select_output_dir(self):
        """选择自定义输出目录"""
        directory = filedialog.askdirectory(title="选择输出目录（留空=输出到源文件目录）")
        if directory:
            self.output_path_var.set(directory)
            self.log_message(f"📂 输出目录设置为：{directory}", "info")

    # ───────────────────────── 日志 ─────────────────────────

    def log_message(self, message: str, level: str = "info"):
        """在日志区域输出一条消息"""
        self.log_text.insert(tk.END, message + "\n", level)
        self.log_text.see(tk.END)
        self.root.update()

    # ───────────────────────── 编码检测 ─────────────────────────

    def detect_encoding(self, file_path: str):
        """自动检测文件编码"""
        try:
            with open(file_path, "rb") as f:
                raw = f.read()
                result = chardet.detect(raw)
                return result["encoding"], result["confidence"]
        except Exception:
            return None, 0

    def read_file_with_encoding(self, file_path: str):
        """尝试用各种编码读取文件"""
        encodings = [
            "utf-8", "gbk", "gb2312", "gb18030",
            "big5", "utf-16", "utf-16-le", "utf-16-be", "ascii"
        ]

        # 先自动检测
        detected_enc, conf = self.detect_encoding(file_path)
        if detected_enc and conf > 0.7:
            try:
                with open(file_path, "r", encoding=detected_enc) as f:
                    text = f.read()
                return text, detected_enc, conf
            except Exception:
                pass

        # 逐个尝试
        for enc in encodings:
            try:
                with open(file_path, "r", encoding=enc) as f:
                    text = f.read()
                if "\ufffd" not in text:
                    return text, enc, 1.0
            except Exception:
                continue

        # 最后用 utf-8 忽略错误兜底
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
            return text, "utf-8 (with errors)", 0.5
        except Exception:
            return None, None, 0

    # ───────────────────────── 转换引擎 ─────────────────────────

    def convert_file(self, input_path: str, output_path: str):
        """转换单个文件，返回 (success, error_msg, stats)"""
        try:
            text, detected_enc, conf = self.read_file_with_encoding(input_path)
            if text is None:
                return False, "无法读取文件或识别编码", None

            direction = self.direction_var.get()
            cc = opencc.OpenCC(direction)
            converted_text = cc.convert(text)

            stats = self.analyze_conversion(text, converted_text)
            stats["original_encoding"] = detected_enc
            stats["encoding_confidence"] = conf

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(converted_text)

            return True, None, stats
        except Exception as e:
            return False, str(e), None

    def analyze_conversion(self, original_text: str, converted_text: str) -> dict:
        """分析转换统计"""
        stats = {
            "total_chars": len(original_text),
            "changed_chars": 0,
            "one_to_many": 0,
            "many_to_one": 0,
            "examples": [],
        }

        changed_pairs = []
        for orig, conv in zip(original_text, converted_text):
            if orig != conv:
                changed_pairs.append((orig, conv))
                stats["changed_chars"] += 1

        one_to_many = {}
        many_to_one = {}
        for orig, conv in changed_pairs:
            one_to_many.setdefault(orig, set()).add(conv)
            many_to_one.setdefault(conv, set()).add(orig)

        for trad, simp_set in one_to_many.items():
            if len(simp_set) > 1:
                stats["one_to_many"] += len(simp_set) - 1
                stats["examples"].append(f"一对多: {trad} -> {', '.join(simp_set)}")

        for simp, trad_set in many_to_one.items():
            if len(trad_set) > 1:
                stats["many_to_one"] += len(trad_set) - 1
                stats["examples"].append(f"多对一: {', '.join(trad_set)} -> {simp}")

        stats["examples"] = stats["examples"][:5]
        return stats

    # ───────────────────────── 批量转换 ─────────────────────────

    def start_conversion(self):
        """启动转换线程"""
        if not self.file_list:
            messagebox.showwarning("警告", "请先添加要转换的文件")
            return

        # 如果输出目录指定了但不存在，创建
        output_dir = self.output_path_var.get().strip()
        if output_dir and not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except Exception as e:
                messagebox.showerror("错误", f"无法创建输出目录：{e}")
                return

        self.convert_button.config(state="disabled")
        thread = threading.Thread(target=self._process_conversion, daemon=True)
        thread.start()

    def _get_output_path(self, input_path: str) -> str:
        """根据命名模式决定输出路径"""
        naming = self.naming_var.get()
        parent_dir = os.path.dirname(input_path)
        filename = os.path.basename(input_path)
        stem = _strip_ext(filename)
        ext = ".txt"

        # 输出目录：用户指定 or 源文件目录
        custom_dir = self.output_path_var.get().strip()
        out_dir = custom_dir if custom_dir else parent_dir
        if not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)

        if naming == "overwrite":
            return os.path.join(parent_dir, filename)

        # 添加后缀
        suffix = self.suffix_var.get()
        output_name = f"{stem}{suffix}{ext}"
        return os.path.join(out_dir, output_name)

    def _process_conversion(self):
        """在线程中处理批量转换"""
        total = len(self.file_list)
        success_count = 0
        error_count = 0
        total_stats = {
            "total_chars": 0,
            "changed_chars": 0,
            "one_to_many": 0,
            "many_to_one": 0,
            "all_examples": [],
        }

        self.log_message("=" * 56, "info")
        self.log_message(f"▶ 开始转换 {total} 个文件…", "info")
        self.log_message("=" * 56, "info")

        for i, (input_path, display_name) in enumerate(self.file_list):
            self.status_label.config(
                text=f"正在转换 [{i + 1}/{total}]：{display_name}"
            )
            self.log_message(f"[{i + 1}/{total}] {display_name}", "info")

            output_path = self._get_output_path(input_path)

            # 检查是否会覆盖
            if os.path.exists(output_path) and output_path != input_path:
                self.log_message(f"  ⚠ 目标文件已存在，跳过：{os.path.basename(output_path)}", "warning")
                error_count += 1
                continue

            success, error, stats = self.convert_file(input_path, output_path)

            if success:
                success_count += 1
                self.log_message(f"  ✓ 成功 → {os.path.basename(output_path)}", "success")
                if stats:
                    self.log_message(
                        f"    编码: {stats['original_encoding']} "
                        f"(置信度: {stats['encoding_confidence']:.0%}) → UTF-8",
                        "info"
                    )
                    self.log_message(
                        f"    字符: {stats['total_chars']}, "
                        f"变化: {stats['changed_chars']}, "
                        f"一对多: {stats['one_to_many']}, "
                        f"多对一: {stats['many_to_one']}",
                        "info"
                    )
                    for ex in stats["examples"]:
                        self.log_message(f"    {ex}", "warning")
                total_stats["total_chars"] += stats["total_chars"]
                total_stats["changed_chars"] += stats["changed_chars"]
                total_stats["one_to_many"] += stats["one_to_many"]
                total_stats["many_to_one"] += stats["many_to_one"]
                total_stats["all_examples"].extend(stats["examples"])
            else:
                error_count += 1
                self.log_message(f"  ✗ 失败：{error}", "error")

            self.progress["value"] = (i + 1) / total * 100
            self.root.update()

        # ── 汇总 ──
        self.log_message("=" * 56, "info")
        self.log_message(f"🏁 转换完成！成功: {success_count}，失败: {error_count}", "info")
        if total_stats["total_chars"] > 0:
            self.log_message(
                f"   总字符: {total_stats['total_chars']}, "
                f"变化: {total_stats['changed_chars']}",
                "info"
            )
        unique_examples = list(set(total_stats["all_examples"]))
        if unique_examples:
            self.log_message("转换示例（前 10 条）：", "info")
            for ex in unique_examples[:10]:
                self.log_message(f"  {ex}", "warning")

        self.status_label.config(
            text=f"完成！成功: {success_count}，失败: {error_count}"
        )
        self.convert_button.config(state="normal")
        self.root.update()


# ═══════════════════════════════════════════════════════════════════
#  入口
# ═══════════════════════════════════════════════════════════════════

def main():
    if HAS_DND:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()
    try:
        root.iconbitmap('CathaySimplify.ico')
    except:
        pass
    app = CathaySimplify(root)
    root.mainloop()


if __name__ == "__main__":
    main()
