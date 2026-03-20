from __future__ import annotations

import sys

from rich.console import Console

from config.settings import get_settings
from integrations.jira_client import JiraClient
from workflows.daily_jira_report import DailyJiraReport, JiraReportConfig


def main(argv: list[str]) -> int:
    console = Console()

    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        console.print(
            "Usage:\n"
            "  python main.py jira-report\n\n"
            "Commands:\n"
            "  jira-report   Run Daily JIRA report using JQL from .env\n"
        )
        return 0

    cmd = argv[1]

    if cmd == "jira-report":
        settings = get_settings()
        jira = JiraClient(
            base_url=settings.jira_base_url,
            email=settings.jira_email,
            api_token=settings.jira_api_token,
        )
        report = DailyJiraReport(jira=jira, console=console)
        report.run(JiraReportConfig(jql=settings.jira_jql, max_results=settings.jira_max_results))
        return 0

    console.print(f"[red]Unknown command:[/red] {cmd}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))