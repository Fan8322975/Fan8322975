#!/usr/bin/env python3
"""
Word 文档处理模块
用于读取和生成 Word 格式的学术稿件
"""

import os
import re
from pathlib import Path
from datetime import datetime


class WordDocumentProcessor:
    """
    处理 Word 文档的类
    注意：这是一个基础版本，实际使用时需要安装 python-docx 库
    """

    def __init__(self):
        self.has_docx = self._check_docx_library()

    def _check_docx_library(self):
        """检查是否安装了 python-docx"""
        try:
            import docx
            return True
        except ImportError:
            return False

    def read_docx(self, file_path):
        """
        读取 Word 文档内容

        Args:
            file_path: Word 文档路径

        Returns:
            文档内容（文本格式）
        """
        if not self.has_docx:
            return self._read_docx_fallback(file_path)

        try:
            import docx
            doc = docx.Document(file_path)

            content = []
            for paragraph in doc.paragraphs:
                content.append(paragraph.text)

            return '\n'.join(content)
        except Exception as e:
            print(f"读取 Word 文档时出错: {e}")
            return None

    def _read_docx_fallback(self, file_path):
        """
        备用方案：提示用户如何安装库
        """
        print("⚠️ 需要安装 python-docx 库来处理 Word 文档")
        print("请运行: pip install python-docx")
        print("\n临时解决方案：")
        print("1. 将 Word 文档另存为 .txt 或 .md 格式")
        print("2. 或者直接复制文档内容到文本文件")
        return None

    def create_formatted_docx(self, content_dict, output_path, journal_name):
        """
        创建格式化的 Word 文档

        Args:
            content_dict: 包含各部分内容的字典
            output_path: 输出文件路径
            journal_name: 期刊名称（用于选择格式）
        """
        if not self.has_docx:
            self._create_docx_fallback(content_dict, output_path)
            return

        try:
            import docx
            from docx.shared import Pt, Inches, RGBColor
            from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

            # 创建新文档
            doc = docx.Document()

            # 设置页面
            section = doc.sections[0]
            section.page_height = Inches(11)  # Letter size
            section.page_width = Inches(8.5)
            section.top_margin = Inches(1)
            section.bottom_margin = Inches(1)
            section.left_margin = Inches(1)
            section.right_margin = Inches(1)

            # 标题
            if 'title' in content_dict:
                title = doc.add_paragraph(content_dict['title'])
                title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
                title_format = title.runs[0]
                title_format.font.size = Pt(16)
                title_format.font.bold = True
                title_format.font.name = 'Times New Roman'

            # 作者
            if 'authors' in content_dict:
                authors = doc.add_paragraph(content_dict['authors'])
                authors.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
                authors_format = authors.runs[0]
                authors_format.font.size = Pt(12)
                authors_format.font.name = 'Times New Roman'

            # 单位
            if 'affiliations' in content_dict:
                affiliations = doc.add_paragraph(content_dict['affiliations'])
                affiliations.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
                affiliations_format = affiliations.runs[0]
                affiliations_format.font.size = Pt(10)
                affiliations_format.font.italic = True

            doc.add_paragraph()  # 空行

            # 摘要
            if 'abstract' in content_dict:
                abstract_heading = doc.add_paragraph('Abstract')
                abstract_heading.runs[0].font.bold = True
                abstract_heading.runs[0].font.size = Pt(12)

                abstract_text = doc.add_paragraph(content_dict['abstract'])
                abstract_text.runs[0].font.size = Pt(11)
                abstract_text.paragraph_format.line_spacing = 1.5

            # 关键词
            if 'keywords' in content_dict:
                keywords_para = doc.add_paragraph()
                keywords_para.add_run('Keywords: ').bold = True
                keywords_para.add_run(content_dict['keywords'])
                keywords_para.runs[0].font.size = Pt(11)

            doc.add_paragraph()  # 空行

            # 主体部分
            sections = ['introduction', 'methods', 'results', 'discussion', 'conclusion']
            section_titles = {
                'introduction': 'Introduction',
                'methods': 'Materials and Methods',
                'results': 'Results',
                'discussion': 'Discussion',
                'conclusion': 'Conclusion'
            }

            for section_key in sections:
                if section_key in content_dict:
                    # 章节标题
                    heading = doc.add_paragraph(section_titles[section_key])
                    heading.runs[0].font.bold = True
                    heading.runs[0].font.size = Pt(14)
                    heading.runs[0].font.name = 'Times New Roman'

                    # 章节内容
                    paragraphs = content_dict[section_key].split('\n\n')
                    for para_text in paragraphs:
                        if para_text.strip():
                            para = doc.add_paragraph(para_text.strip())
                            para.runs[0].font.size = Pt(11)
                            para.runs[0].font.name = 'Times New Roman'
                            para.paragraph_format.line_spacing = 2.0  # 双倍行距
                            para.paragraph_format.first_line_indent = Inches(0.5)

            # 参考文献
            if 'references' in content_dict:
                ref_heading = doc.add_paragraph('References')
                ref_heading.runs[0].font.bold = True
                ref_heading.runs[0].font.size = Pt(14)

                references = content_dict['references'].split('\n')
                for ref in references:
                    if ref.strip():
                        ref_para = doc.add_paragraph(ref.strip())
                        ref_para.runs[0].font.size = Pt(10)
                        ref_para.paragraph_format.line_spacing = 1.0
                        ref_para.paragraph_format.left_indent = Inches(0.5)
                        ref_para.paragraph_format.first_line_indent = Inches(-0.5)

            # 保存文档
            doc.save(output_path)
            print(f"✓ Word 文档已创建: {output_path}")

        except Exception as e:
            print(f"❌ 创建 Word 文档时出错: {e}")
            self._create_docx_fallback(content_dict, output_path)

    def _create_docx_fallback(self, content_dict, output_path):
        """
        备用方案：创建纯文本版本
        """
        txt_path = output_path.replace('.docx', '.txt')

        with open(txt_path, 'w', encoding='utf-8') as f:
            if 'title' in content_dict:
                f.write(f"{content_dict['title']}\n")
                f.write("=" * len(content_dict['title']) + "\n\n")

            if 'authors' in content_dict:
                f.write(f"{content_dict['authors']}\n\n")

            if 'affiliations' in content_dict:
                f.write(f"{content_dict['affiliations']}\n\n")

            if 'abstract' in content_dict:
                f.write("Abstract\n--------\n")
                f.write(f"{content_dict['abstract']}\n\n")

            if 'keywords' in content_dict:
                f.write(f"Keywords: {content_dict['keywords']}\n\n")

            sections = ['introduction', 'methods', 'results', 'discussion', 'conclusion']
            section_titles = {
                'introduction': 'Introduction',
                'methods': 'Materials and Methods',
                'results': 'Results',
                'discussion': 'Discussion',
                'conclusion': 'Conclusion'
            }

            for section_key in sections:
                if section_key in content_dict:
                    f.write(f"\n{section_titles[section_key]}\n")
                    f.write("-" * len(section_titles[section_key]) + "\n\n")
                    f.write(f"{content_dict[section_key]}\n\n")

            if 'references' in content_dict:
                f.write("\nReferences\n----------\n")
                f.write(f"{content_dict['references']}\n")

        print(f"⚠️ 已创建文本版本: {txt_path}")
        print("要创建 Word 版本，请安装: pip install python-docx")


def install_dependencies():
    """安装必需的依赖"""
    print("正在安装必需的依赖...")
    os.system("pip install python-docx")
    print("✓ 依赖安装完成")


if __name__ == "__main__":
    # 测试
    processor = WordDocumentProcessor()

    if not processor.has_docx:
        print("是否现在安装 python-docx? (y/n)")
        choice = input().strip().lower()
        if choice == 'y':
            install_dependencies()

    # 创建示例文档
    sample_content = {
        'title': 'Sample Research Article Title',
        'authors': 'Author A¹, Author B², Author C¹*',
        'affiliations': '¹Department of Science, University A\n²Institute of Research, University B\n*Corresponding author: email@example.com',
        'abstract': 'This is a sample abstract. It should be concise and summarize the main findings of the research. Typically 150-300 words.',
        'keywords': 'keyword1, keyword2, keyword3, keyword4',
        'introduction': 'This is the introduction section. It provides background information and states the research objectives.',
        'methods': 'This section describes the materials and methods used in the study.',
        'results': 'This section presents the findings of the research.',
        'discussion': 'This section interprets the results and discusses their implications.',
        'conclusion': 'This section summarizes the main conclusions of the study.',
        'references': '1. Author A, et al. (2024). Title of paper. Journal Name, 10(2), 123-145.\n2. Author B, et al. (2023). Another paper. Another Journal, 5(1), 67-89.'
    }

    output = 'sample_manuscript.docx'
    processor.create_formatted_docx(sample_content, output, 'Nature')
