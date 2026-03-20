from __future__ import annotations

import base64
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests


@dataclass(frozen=True)
class JiraIssue:
    key: str
    summary: str
    status: str
    assignee: str
    updated: str
    url: str


class JiraClient:
    def __init__(self, base_url: str, email: str, api_token: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        token = base64.b64encode(f"{email}:{api_token}".encode("utf-8")).decode("utf-8")
        self.session.headers.update(
            {
                "Authorization": f"Basic {token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

    def search_issues(self, jql: str, max_results: int = 50) -> List[JiraIssue]:
        url = f"{self.base_url}/rest/api/3/search"
        payload: Dict[str, Any] = {
            "jql": jql,
            "maxResults": max_results,
            "fields": ["summary", "status", "assignee", "updated"],
        }

        resp = self.session.post(url, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        issues: List[JiraIssue] = []
        for item in data.get("issues", []):
            fields = item.get("fields", {})
            key = item.get("key", "")
            summary = fields.get("summary", "") or ""
            status = (fields.get("status") or {}).get("name", "") or ""
            assignee_obj: Optional[Dict[str, Any]] = fields.get("assignee")
            assignee = (
                (assignee_obj or {}).get("displayName")
                or (assignee_obj or {}).get("emailAddress")
                or "Unassigned"
            )
            updated = fields.get("updated", "") or ""
            browse_url = f"{self.base_url}/browse/{key}" if key else self.base_url

            issues.append(
                JiraIssue(
                    key=key,
                    summary=summary,
                    status=status,
                    assignee=assignee,
                    updated=updated,
                    url=browse_url,
                )
            )

        return issues