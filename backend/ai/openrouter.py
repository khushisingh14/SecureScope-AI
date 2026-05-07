import httpx
import logging

from backend.config import get_settings


logger = logging.getLogger("securescope.ai")


class OpenRouterClient:
    def __init__(self):
        self.settings = get_settings()

    async def complete(self, system: str, user: str) -> str:
        if not self.settings.openrouter_api_key:
            return self._offline_response(user)

        payload = {
            "model": self.settings.openrouter_model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": 0.2,
            "max_tokens": 900,
        }
        headers = {
            "Authorization": f"Bearer {self.settings.openrouter_api_key}",
            "HTTP-Referer": "https://securescope.local",
            "X-Title": "SecureScope AI",
        }
        try:
            async with httpx.AsyncClient(base_url=str(self.settings.openrouter_base_url), timeout=30) as client:
                response = await client.post("/chat/completions", json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"].strip()
        except (httpx.HTTPError, KeyError, IndexError, TypeError) as exc:
            logger.warning("OpenRouter request failed, using offline analysis: %s", exc)
            return self._offline_response(user)

    def _offline_response(self, prompt: str) -> str:
        return (
            "AI offline mode: configure OPENROUTER_API_KEY to enable live analysis. "
            "Recommended action: validate exploitability, prioritize internet-facing critical/high findings, "
            "patch affected services, and document compensating controls for accepted risk."
        )


def vulnerability_prompt(finding) -> tuple[str, str]:
    system = (
        "You are a senior penetration testing report writer. Produce concise, accurate, "
        "client-ready vulnerability analysis with clear business risk and remediation."
    )
    user = f"""
Analyze this vulnerability and return:
1. Plain-English explanation
2. Business impact
3. Specific remediation
4. Prioritization rationale

Title: {finding.title}
Severity: {finding.severity}
Affected host: {finding.affected_host}
Description: {finding.description}
Current remediation: {finding.remediation}
Source: {finding.source}
"""
    return system, user


def executive_summary_prompt(findings: list) -> tuple[str, str]:
    system = "You write executive cybersecurity assessment summaries for consulting deliverables."
    condensed = "\n".join(
        f"- {item.severity}: {item.title} on {item.affected_host}" for item in findings[:30]
    )
    user = f"""
Create a concise executive summary for a penetration testing report. Include security posture,
key themes, risk prioritization, and remediation direction.

Findings:
{condensed or "- No findings imported"}
"""
    return system, user
