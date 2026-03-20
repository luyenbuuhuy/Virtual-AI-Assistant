from __future__ import annotations

from dataclasses import dataclass
from typing import List

from rich.console import Console
from rich.table import Table

from integrations.jira_client import JiraClient, JiraIssue


@dataclass(frozen=True)
class JiraReportConfig:
    jql: str
    max_results: int = 50


class DailyJiraReport:
    def __init__(self, jira: JiraClient, console: Console | None = None) -> None:
        self.jira = jira
        self.console = console or Console()

    def run(self, cfg: JiraReportConfig) -> List[JiraIssue]:
        issues = self.jira.search_issues(jql=cfg.jql, max_results=cfg.max_results)
        self._print(issues, cfg)
        return issues

    def _print(self, issues: List[JiraIssue], cfg: JiraReportConfig) -> None:
        self.console.rule("[bold]Daily JIRA Report[/bold]")
        self.console.print(f"[dim]JQL:[/dim] {cfg.jql}")
        self.console.print(f"[dim]Results:[/dim] {len(issues)} (max {cfg.max_results})\n")

        table = Table(show_lines=False)
        table.add_column("Key", style="cyan", no_wrap=True)
        table.add_column("Status", style="magenta", no_wrap=True)
        table.add_column("Assignee", style="green")
        table.add_column("Updated", style="dim", no_wrap=True)
        table.add_column("Summary")

        for it in issues:
            table.add_row(it.key, it.status, it.assignee, it.updated, it.summary)

        self.console.print(table)