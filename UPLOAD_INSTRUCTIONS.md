# 📤 文档上传和使用说明

## 🎯 如何提供稿件给我

### 方法 1: 直接上传文件（推荐）

在对话界面中，您可以：

1. **点击上传按钮** 📎 （通常在输入框附近）
2. **选择您的稿件文件**
3. **发送消息**："帮我检查这篇稿件，要投到 [期刊名称]"

**支持的文件格式：**
- ✅ Microsoft Word (.docx, .doc)
- ✅ PDF (.pdf)
- ✅ Markdown (.md)
- ✅ LaTeX (.tex)
- ✅ 纯文本 (.txt)
- ✅ Rich Text (.rtf)

---

### 方法 2: 提供文件路径

如果文件已经在系统中，直接告诉我路径：

```
我的稿件在 /path/to/manuscript.docx
要投到 Nature Communications
```

---

### 方法 3: 直接粘贴内容

对于较短的文档，可以直接粘贴内容：

```
我要投稿到 Science，稿件内容如下：

[粘贴全文内容]

请帮我检查格式
```

---

## 📝 完整使用流程

### 示例对话 1: 标准投稿

```
👤 用户：
我上传了一篇关于机器学习的论文（attached: ml_paper.docx），
要投到 IEEE Access 的 Artificial Intelligence 特刊。
请帮我检查格式并准备投稿。

🤖 助手：
收到您的稿件！开始处理...

第一步：分析您的稿件
✓ 文件类型: Word 文档
✓ 总字数: 6,234 词
✓ 检测到的章节: Abstract, Introduction, Methods, Results, Discussion, Conclusion, References

第二步：搜索期刊要求
正在搜索 IEEE Access AI 特刊的投稿要求...

[显示搜索结果和期刊要求]

第三步：格式检查
✓ 结构完整
⚠️ 需要调整的地方:
  1. 摘要略长（当前 256 词，建议 200 词以内）
  2. 缺少 Index Terms（关键词）
  3. 参考文献需要改为 IEEE 格式
  4. 图片需要单独提交（JPEG/PNG格式）

第四步：生成 Word 格式输出
✓ 已生成符合 IEEE Access 格式的 Word 文档
✓ 已生成 Cover Letter
✓ 已生成检查报告

文件保存在：
- manuscript-submission/submission/revised_manuscript.docx
- manuscript-submission/submission/cover_letter.docx
- manuscript-submission/reports/check_report.txt

是否需要我帮您修改摘要和参考文献格式？
```

---

### 示例对话 2: 快速检查

```
👤 用户：
快速检查一下这个文档的格式（attached: draft.pdf）

🤖 助手：
快速检查结果：

✓ 标题: ✓
✓ 摘要: ✓ (178 词)
✓ 关键词: ✓ (5 个)
✓ 引言: ✓
✓ 方法: ✓
✓ 结果: ✓
✓ 讨论: ✓
✓ 结论: ✓
✗ 参考文献: 文中引用 35 处，但参考文献列表只有 33 条

建议：
- 检查并补充缺失的 2 条参考文献

需要详细报告吗？
```

---

### 示例对话 3: 生成图片

```
👤 用户：
我需要一个研究流程图，包括：
数据收集 → 预处理 → 特征提取 → 模型训练 → 验证 → 结果分析

🤖 助手：
好的！由于我无法直接生成图片，我为您准备了专业的 AI 绘图 prompt：

=== 复制以下 Prompt 到 DALL-E 或 Midjourney ===

Create a professional scientific flowchart for a machine learning research workflow with the following steps:

1. Data Collection (database icon)
2. Data Preprocessing (filter/clean icon)
3. Feature Extraction (selection icon)
4. Model Training (neural network icon)
5. Validation (checkmark icon)
6. Results Analysis (chart icon)

Style requirements:
- Clean academic style suitable for Nature journal
- Use rectangular boxes for each step
- Blue and white color scheme (#2E86AB primary, white background)
- Arrows showing flow direction between steps
- Each box labeled with clear sans-serif font (Arial/Helvetica)
- High resolution (300 DPI minimum)
- Professional publication quality
- Modern flat design

=====================================

生成图片后：
1. 保存为高分辨率 TIFF 或 PNG (≥300 DPI)
2. 告诉我，我会帮您插入到 Word 文档中
3. 我会添加适当的图注

您也可以查看 image_prompts_library.md 获取更多图片 prompt 模板。
```

---

## 📊 最终交付格式：Word 文档

### 系统会生成的文件：

```
manuscript-submission/
└── submission/
    ├── manuscript_final.docx          ⭐ 主稿件（格式化完成）
    ├── cover_letter.docx              ⭐ 投稿信
    ├── highlights.docx                 （如期刊需要）
    ├── author_info.docx                 作者信息表
    ├── figures/
    │   ├── Figure_1.tiff              ⭐ 高分辨率图片
    │   ├── Figure_2.tiff
    │   └── ...
    └── supplementary/
        └── supplementary_materials.docx
```

### Word 文档特点：

✅ **完全符合期刊格式要求**
- 正确的页面设置（页边距、纸张大小）
- 标准字体（Times New Roman / Arial）
- 合适的行距（双倍行距或期刊要求）
- 规范的标题层级

✅ **可直接编辑**
- 使用 Word 样式，便于修改
- 图表题注使用交叉引用
- 参考文献可更新
- 包含修订标记（如需要）

✅ **ready for submission**
- 包含行号（如期刊要求）
- 图表位置标记
- 页眉页脚设置
- 符合字数限制

---

## 🔄 典型工作流程时间线

| 步骤 | 您需要做的 | 我会做的 | 时间 |
|------|-----------|---------|------|
| 1️⃣ | 上传稿件 + 告知期刊 | 读取并分析 | 1 分钟 |
| 2️⃣ | 等待 | 搜索期刊要求 | 2-3 分钟 |
| 3️⃣ | 等待 | 格式检查 | 1 分钟 |
| 4️⃣ | 查看报告，确认修改 | 生成检查报告 | 即时 |
| 5️⃣ | 等待或提供图片 | 调整格式，生成 Word | 2-3 分钟 |
| 6️⃣ | 下载最终文件 | 打包交付 | 即时 |
| **总计** | **约 5-10 分钟** | | |

---

## 💡 高级功能

### 1. 批量处理

```
我有 3 篇文章要投不同期刊：
1. paper1.docx → Nature Communications
2. paper2.docx → Science Advances
3. paper3.docx → PNAS

请分别检查并生成投稿文件
```

---

### 2. 版本对比

```
我修改了稿件，帮我对比新旧版本：
原版: manuscript_v1.docx
新版: manuscript_v2.docx

生成修改对照文档
```

---

### 3. 审稿意见回复

```
我收到审稿意见了（attached: reviewer_comments.pdf）
稿件是 manuscript.docx

帮我：
1. 整理审稿意见
2. 准备逐条回复模板
3. 在稿件中标记需要修改的地方
```

---

## ⚙️ 系统配置

### 安装必需库（可选，用于 Word 处理）

```bash
pip install python-docx
```

如果不安装，系统会：
- ✅ 仍然可以读取和分析文档（通过文本转换）
- ✅ 生成文本格式的检查报告
- ⚠️ Word 输出会先生成 .txt 格式，然后提供转换指导

---

## 📋 投稿前检查清单（自动化）

我会自动检查以下所有项目：

### 内容检查
- [ ] 标题长度合适（≤20 词）
- [ ] 摘要字数符合要求（通常 150-300 词）
- [ ] 关键词数量正确（通常 3-6 个）
- [ ] 所有必需章节完整
- [ ] 图表在文中被引用
- [ ] 参考文献引用完整

### 格式检查
- [ ] 页面设置正确
- [ ] 字体统一
- [ ] 行距符合要求
- [ ] 图表编号连续
- [ ] 参考文献格式统一

### 文件检查
- [ ] 主稿件 Word 格式
- [ ] 图片高分辨率（≥300 DPI）
- [ ] Cover Letter 完成
- [ ] 补充材料准备好

---

## 🎯 立即开始！

### 三种快速开始方式：

**方式 1: 上传 + 简单说明**
```
[上传文件: my_paper.docx]
投到 Nature，帮我检查
```

**方式 2: 详细说明**
```
[上传文件: research.pdf]
这是一篇关于气候变化的研究论文
要投到 Nature Climate Change
请全面检查格式并生成 Word 投稿文件
```

**方式 3: 测试运行**
```
用 sample_manuscript.md 测试一下系统
假设要投到 Nature Communications
```

---

## ❓ 常见问题

### Q: 上传文件大小有限制吗？
A: 通常 <50MB。如果文件太大，可以先压缩图片或分开处理。

### Q: 是否保存我的文件？
A: 所有处理都是临时的。您可以选择保存输出文件。

### Q: 可以处理非英文稿件吗？
A: 可以！支持中文、英文及其他语言。

### Q: 如果期刊要求很特殊怎么办？
A: 告诉我具体要求，我会自定义处理流程。

### Q: 生成的 Word 文档可以修改吗？
A: 完全可以！文档使用标准 Word 格式和样式，您可以自由编辑。

---

**准备好了吗？现在就上传您的稿件，让我们开始吧！** 🚀

**或者先用测试稿件试试：**
```
帮我测试一下系统
用 sample_manuscript.md
假设投到 Nature Communications
```
