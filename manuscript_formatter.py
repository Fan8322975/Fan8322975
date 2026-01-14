#!/usr/bin/env python3
"""
学术稿件自动格式化工具
用于检查和调整稿件以符合目标期刊的投稿要求
"""

import os
import sys
import json
import re
from datetime import datetime
from pathlib import Path

class ManuscriptFormatter:
    def __init__(self, manuscript_path, journal_name, special_issue=None):
        """
        初始化稿件格式化工具

        Args:
            manuscript_path: 稿件文件路径
            journal_name: 期刊名称
            special_issue: 特刊名称（可选）
        """
        self.manuscript_path = Path(manuscript_path)
        self.journal_name = journal_name
        self.special_issue = special_issue
        self.requirements = {}
        self.issues = []
        self.suggestions = []

        # 创建工作目录
        self.work_dir = Path("manuscript-submission")
        self.setup_directories()

    def setup_directories(self):
        """创建项目目录结构"""
        dirs = [
            "original",
            "revised",
            "figures",
            "tables",
            "references",
            "supplementary",
            "submission",
            "reports"
        ]

        for dir_name in dirs:
            (self.work_dir / dir_name).mkdir(parents=True, exist_ok=True)

        print(f"✓ 工作目录已创建: {self.work_dir.absolute()}")

    def fetch_journal_requirements(self):
        """
        联网获取期刊投稿要求
        这个方法需要调用 Claude 的 WebSearch 功能
        """
        print(f"\n正在搜索 {self.journal_name} 的投稿要求...")

        # 返回需要搜索的关键词
        search_queries = [
            f"{self.journal_name} author guidelines",
            f"{self.journal_name} manuscript preparation",
            f"{self.journal_name} submission requirements"
        ]

        if self.special_issue:
            search_queries.append(f"{self.journal_name} {self.special_issue} special issue")

        return search_queries

    def analyze_manuscript_structure(self, content):
        """分析稿件结构"""
        print("\n📋 分析稿件结构...")

        structure = {
            "has_title": False,
            "has_abstract": False,
            "has_keywords": False,
            "has_introduction": False,
            "has_methods": False,
            "has_results": False,
            "has_discussion": False,
            "has_conclusion": False,
            "has_references": False,
            "sections": []
        }

        # 常见章节标题模式
        section_patterns = {
            "title": r"^#\s+.+|^[A-Z][^a-z]{10,}$",
            "abstract": r"(?i)^#+\s*abstract|^abstract\s*$",
            "keywords": r"(?i)^#+\s*keywords?|^keywords?:",
            "introduction": r"(?i)^#+\s*introduction|^\d+\.?\s*introduction",
            "methods": r"(?i)^#+\s*(methods?|materials? and methods?|methodology)",
            "results": r"(?i)^#+\s*results?",
            "discussion": r"(?i)^#+\s*discussion",
            "conclusion": r"(?i)^#+\s*conclusions?",
            "references": r"(?i)^#+\s*(references?|bibliography)"
        }

        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue

            for section, pattern in section_patterns.items():
                if re.match(pattern, line):
                    structure[f"has_{section}"] = True
                    structure["sections"].append(section.capitalize())

        return structure

    def check_word_count(self, content):
        """检查字数"""
        # 移除多余空白
        text = re.sub(r'\s+', ' ', content)
        word_count = len(text.split())

        return {
            "total_words": word_count,
            "abstract_words": self.extract_section_word_count(content, "abstract"),
            "main_text_words": word_count  # 需要更精确的计算
        }

    def extract_section_word_count(self, content, section_name):
        """提取特定章节的字数"""
        pattern = rf"(?i)(?:^|\n)#+\s*{section_name}.*?\n(.*?)(?=\n#+|\Z)"
        match = re.search(pattern, content, re.DOTALL)

        if match:
            section_text = match.group(1)
            return len(re.sub(r'\s+', ' ', section_text).split())
        return 0

    def check_figures_and_tables(self, content):
        """检查图表引用"""
        # 查找图表引用
        fig_references = re.findall(r'(?i)fig(?:ure)?\.?\s*(\d+)', content)
        table_references = re.findall(r'(?i)table\.?\s*(\d+)', content)

        return {
            "figures": sorted(set(map(int, fig_references))) if fig_references else [],
            "tables": sorted(set(map(int, table_references))) if table_references else [],
            "figure_count": len(set(fig_references)),
            "table_count": len(set(table_references))
        }

    def check_references(self, content):
        """检查参考文献"""
        # 查找引用标记 [1], (1), etc.
        citations = re.findall(r'\[(\d+)\]|\((\d+)\)', content)
        citations = [int(c[0] or c[1]) for c in citations]

        # 查找参考文献列表
        ref_section = re.search(r'(?i)(?:^|\n)#+\s*references.*?\n(.*)', content, re.DOTALL)
        ref_count = 0

        if ref_section:
            ref_text = ref_section.group(1)
            # 简单计数参考文献条目（以数字开头的行）
            ref_count = len(re.findall(r'^\s*\d+\.', ref_text, re.MULTILINE))

        return {
            "citation_count": len(set(citations)),
            "reference_count": ref_count,
            "max_citation": max(citations) if citations else 0
        }

    def generate_report(self, analysis_results):
        """生成检查报告"""
        report = f"""
{'='*80}
学术稿件格式检查报告
{'='*80}

生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
稿件文件: {self.manuscript_path}
目标期刊: {self.journal_name}
{'特刊: ' + self.special_issue if self.special_issue else ''}

{'='*80}
1. 结构检查
{'='*80}

检测到的章节:
"""

        structure = analysis_results.get('structure', {})
        for section in structure.get('sections', []):
            report += f"  ✓ {section}\n"

        # 检查缺失的必需章节
        required_sections = ['abstract', 'introduction', 'methods', 'results', 'conclusion', 'references']
        missing = [s for s in required_sections if not structure.get(f'has_{s}', False)]

        if missing:
            report += f"\n⚠️ 缺失的必需章节:\n"
            for section in missing:
                report += f"  ✗ {section.capitalize()}\n"

        report += f"""
{'='*80}
2. 字数统计
{'='*80}

总字数: {analysis_results['word_count']['total_words']} 词
摘要字数: {analysis_results['word_count']['abstract_words']} 词

"""

        report += f"""
{'='*80}
3. 图表检查
{'='*80}

图片数量: {analysis_results['figures']['figure_count']}
引用的图片编号: {analysis_results['figures']['figures']}

表格数量: {analysis_results['figures']['table_count']}
引用的表格编号: {analysis_results['figures']['tables']}

"""

        report += f"""
{'='*80}
4. 参考文献检查
{'='*80}

文中引用次数: {analysis_results['references']['citation_count']}
参考文献条目数: {analysis_results['references']['reference_count']}
最大引用编号: {analysis_results['references']['max_citation']}

"""

        # 检查引用和文献是否匹配
        if analysis_results['references']['max_citation'] != analysis_results['references']['reference_count']:
            report += "⚠️ 警告: 引用编号与参考文献数量不匹配！\n"

        report += f"""
{'='*80}
5. 建议事项
{'='*80}

"""

        # 生成建议
        suggestions = []

        if analysis_results['word_count']['abstract_words'] > 300:
            suggestions.append("• 摘要超过300词，建议精简")
        elif analysis_results['word_count']['abstract_words'] < 150:
            suggestions.append("• 摘要少于150词，可能需要补充内容")

        if missing:
            suggestions.append(f"• 补充缺失的章节: {', '.join(missing)}")

        if not structure.get('has_keywords'):
            suggestions.append("• 添加关键词（通常3-6个）")

        # 检查图表编号连续性
        figs = analysis_results['figures']['figures']
        if figs and figs != list(range(1, len(figs) + 1)):
            suggestions.append("• 检查图片编号是否连续")

        tables = analysis_results['figures']['tables']
        if tables and tables != list(range(1, len(tables) + 1)):
            suggestions.append("• 检查表格编号是否连续")

        if suggestions:
            for suggestion in suggestions:
                report += suggestion + "\n"
        else:
            report += "✓ 暂无特别建议\n"

        report += f"""
{'='*80}
下一步行动
{'='*80}

1. 查看期刊的具体格式要求（字体、行距、页边距等）
2. 检查图片文件是否符合分辨率要求（通常≥300 DPI）
3. 确认参考文献格式符合期刊要求
4. 准备 Cover Letter 和其他补充材料
5. 在投稿系统中选择正确的 Special Issue

{'='*80}
"""

        return report

    def process(self):
        """执行完整的处理流程"""
        print(f"\n{'='*80}")
        print(f"开始处理稿件: {self.manuscript_path.name}")
        print(f"{'='*80}")

        # 读取稿件内容
        try:
            with open(self.manuscript_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"❌ 错误: 无法读取稿件文件 - {e}")
            return False

        # 分析稿件
        analysis_results = {
            'structure': self.analyze_manuscript_structure(content),
            'word_count': self.check_word_count(content),
            'figures': self.check_figures_and_tables(content),
            'references': self.check_references(content)
        }

        # 生成报告
        report = self.generate_report(analysis_results)

        # 保存报告
        report_path = self.work_dir / "reports" / f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)

        print(report)
        print(f"\n✓ 报告已保存至: {report_path}")

        # 返回需要搜索的期刊要求
        search_queries = self.fetch_journal_requirements()

        return {
            'analysis': analysis_results,
            'report_path': report_path,
            'search_queries': search_queries
        }


def main():
    """主函数"""
    if len(sys.argv) < 3:
        print("用法: python manuscript_formatter.py <稿件路径> <期刊名称> [特刊名称]")
        print("\n示例:")
        print("  python manuscript_formatter.py my_paper.md \"Nature Communications\"")
        print("  python manuscript_formatter.py paper.txt \"IEEE Access\" \"Machine Learning Applications\"")
        sys.exit(1)

    manuscript_path = sys.argv[1]
    journal_name = sys.argv[2]
    special_issue = sys.argv[3] if len(sys.argv) > 3 else None

    formatter = ManuscriptFormatter(manuscript_path, journal_name, special_issue)
    result = formatter.process()

    if result:
        print("\n" + "="*80)
        print("需要搜索的期刊信息:")
        print("="*80)
        for query in result['search_queries']:
            print(f"  • {query}")
        print("\n请使用这些关键词搜索期刊的具体要求")


if __name__ == "__main__":
    main()
