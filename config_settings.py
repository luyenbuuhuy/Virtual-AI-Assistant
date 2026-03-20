from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    jira_base_url: str
    jira_email: str
    jira_api_token: str
    jira_jql: str
    jira_max_results: int = 50


def get_settings() -> Settings:
    # Load .env if present
    load_dotenv()

    jira_base_url = os.getenv("JIRA_BASE_URL", "").strip().rstrip("/")
    jira_email = os.getenv("JIRA_EMAIL", "").strip()
    jira_api_token = os.getenv("JIRA_API_TOKEN", "").strip()
    jira_jql = os.getenv("JIRA_JQL", "").strip()

    max_results_raw = os.getenv("JIRA_MAX_RESULTS", "50").strip()
    try:
        jira_max_results = int(max_results_raw)
    except ValueError:
        jira_max_results = 50

    missing = []
    if not jira_base_url:
        missing.append("JIRA_BASE_URL")
    if not jira_email:
        missing.append("JIRA_EMAIL")
    if not jira_api_token:
        missing.append("JIRA_API_TOKEN")

    # JQL is required only for jira-report command, but we validate here for simplicity.
    if not jira_jql:
        missing.append("JIRA_JQL")

    if missing:
        raise ValueError(
            "Missing required environment variables: "
            + ", ".join(missing)
            + ". Please copy .env.example to .env and fill values."
        )

    return Settings(
        jira_base_url=jira_base_url,
        jira_email=jira_email,
        jira_api_token=jira_api_token,
        jira_jql=jira_jql,
        jira_max_results=jira_max_results,
    )