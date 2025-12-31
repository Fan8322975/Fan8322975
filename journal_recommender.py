#!/usr/bin/env python3
"""
智能期刊推荐系统
根据目标期刊推荐难度较低、审稿周期短的替代期刊
"""

import json
from datetime import datetime
from pathlib import Path


class JournalRecommender:
    """
    期刊推荐系统
    基于研究领域、影响因子等推荐合适的期刊
    """

    def __init__(self, target_journal=None, research_field=None):
        """
        初始化推荐系统

        Args:
            target_journal: 目标期刊名称
            research_field: 研究领域
        """
        self.target_journal = target_journal
        self.research_field = research_field

        # 期刊数据库（示例数据，实际使用时需要联网搜索）
        self.journal_database = self._initialize_database()

    def _initialize_database(self):
        """
        初始化期刊数据库
        实际使用时应该从在线数据库获取
        """
        return {
            "nature_communications": {
                "full_name": "Nature Communications",
                "impact_factor": 16.6,
                "acceptance_rate": "~30%",
                "review_time": "6-8 周",
                "publication_time": "8-12 周",
                "difficulty": "高",
                "open_access": True,
                "apc": "$5,290"
            },
            "scientific_reports": {
                "full_name": "Scientific Reports",
                "impact_factor": 4.6,
                "acceptance_rate": "~60%",
                "review_time": "4-6 周",
                "publication_time": "6-8 周",
                "difficulty": "中",
                "open_access": True,
                "apc": "$1,890"
            }
        }

    def get_search_queries(self):
        """
        生成用于搜索替代期刊的查询词
        """
        queries = []

        if self.target_journal:
            # 搜索与目标期刊相似但更易发表的期刊
            queries.extend([
                f"{self.target_journal} alternative journals easier acceptance",
                f"{self.target_journal} similar journals fast review",
                f"journals like {self.target_journal} lower impact factor",
                f"{self.target_journal} field journals high acceptance rate"
            ])

        if self.research_field:
            # 基于研究领域搜索
            queries.extend([
                f"{self.research_field} journals fast review",
                f"{self.research_field} high acceptance rate journals",
                f"{self.research_field} open access journals quick publication"
            ])

        # 通用搜索
        queries.extend([
            "fast peer review journals 2025",
            "high acceptance rate scientific journals",
            "quick publication academic journals"
        ])

        return queries

    def generate_recommendation_report(self, journal_list):
        """
        生成期刊推荐报告

        Args:
            journal_list: 推荐的期刊列表
        """
        report = f"""
{'='*80}
智能期刊推荐报告
{'='*80}

生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
目标期刊: {self.target_journal or '未指定'}
研究领域: {self.research_field or '未指定'}

{'='*80}
推荐理由
{'='*80}

基于以下因素为您推荐替代期刊：
✓ 相似的研究领域和范围
✓ 较高的接受率（更容易发表）
✓ 较短的审稿周期（快速获得反馈）
✓ 合理的发表费用
✓ 良好的学术声誉

{'='*80}
推荐期刊列表
{'='*80}

"""

        for i, journal in enumerate(journal_list, 1):
            report += f"""
{'─'*80}
推荐 #{i}: {journal.get('name', 'N/A')}
{'─'*80}

基本信息:
  期刊全称: {journal.get('name', 'N/A')}
  ISSN: {journal.get('issn', 'N/A')}
  出版商: {journal.get('publisher', 'N/A')}

学术指标:
  影响因子 (2023): {journal.get('impact_factor', 'N/A')}
  中科院分区: {journal.get('cas_zone', 'N/A')}
  JCR 分区: {journal.get('jcr_quartile', 'N/A')}

投稿难度: {journal.get('difficulty', 'N/A')}

审稿信息:
  接受率: {journal.get('acceptance_rate', 'N/A')}
  平均审稿周期: {journal.get('review_time', 'N/A')}
  平均发表周期: {journal.get('publication_time', 'N/A')}

费用:
  开放获取: {journal.get('open_access', 'N/A')}
  APC 费用: {journal.get('apc', 'N/A')}

研究领域:
  {journal.get('fields', 'N/A')}

投稿网址:
  {journal.get('submission_url', 'N/A')}

优势:
"""
            for advantage in journal.get('advantages', []):
                report += f"  ✓ {advantage}\n"

            report += "\n劣势:\n"
            for disadvantage in journal.get('disadvantages', []):
                report += f"  ✗ {disadvantage}\n"

            report += f"\n推荐指数: {'★' * journal.get('recommendation_score', 3)} ({journal.get('recommendation_score', 3)}/5)\n"

        report += f"""
{'='*80}
选择建议
{'='*80}

根据您的需求选择合适的期刊：

1. 如果追求高影响因子和学术声誉
   → 选择推荐列表中 IF > 5 的期刊

2. 如果希望快速发表
   → 选择审稿周期 < 6 周的期刊

3. 如果关注发表成功率
   → 选择接受率 > 50% 的期刊

4. 如果预算有限
   → 选择 APC 费用较低或有免费发表选项的期刊

5. 如果是博士生或早期职业研究者
   → 建议选择接受率高、审稿周期短的期刊，积累发表经验

{'='*80}
下一步行动
{'='*80}

1. 访问推荐期刊的官网，详细了解投稿要求
2. 查看近期发表的文章，确认研究主题匹配
3. 检查期刊是否被 SCI/SSCI 收录（通过 Web of Science）
4. 查看期刊的开放获取政策和版权协议
5. 准备符合目标期刊格式的稿件

{'='*80}
需要帮助？
{'='*80}

我可以帮您：
• 获取任一推荐期刊的详细投稿要求
• 比较多个期刊的优劣势
• 根据特定需求（如快速发表、低费用等）筛选期刊
• 准备符合目标期刊格式的稿件

{'='*80}
"""

        return report

    def search_alternative_journals(self):
        """
        搜索替代期刊
        返回需要搜索的查询词列表
        """
        print(f"\n正在搜索与 {self.target_journal} 相关的替代期刊...")
        print("这将包括：")
        print("  • 相似领域的期刊")
        print("  • 接受率较高的期刊")
        print("  • 审稿周期较短的期刊")
        print("  • 影响因子适中的期刊\n")

        return self.get_search_queries()


def main():
    """主函数"""
    import sys

    if len(sys.argv) < 2:
        print("用法: python journal_recommender.py <目标期刊> [研究领域]")
        print("\n示例:")
        print("  python journal_recommender.py \"Nature Communications\"")
        print("  python journal_recommender.py \"Nature\" \"machine learning\"")
        print("  python journal_recommender.py \"Science\" \"climate change\"")
        sys.exit(1)

    target_journal = sys.argv[1]
    research_field = sys.argv[2] if len(sys.argv) > 2 else None

    recommender = JournalRecommender(target_journal, research_field)
    search_queries = recommender.search_alternative_journals()

    print("\n" + "="*80)
    print("需要搜索的查询词：")
    print("="*80)
    for i, query in enumerate(search_queries, 1):
        print(f"{i}. {query}")

    print("\n" + "="*80)
    print("使用 Claude 的 WebSearch 功能搜索这些查询词")
    print("我将为您整理结果并生成推荐报告")
    print("="*80)


if __name__ == "__main__":
    main()
