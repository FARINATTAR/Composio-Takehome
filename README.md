# Composio Tooling Intelligence: 100-App SaaS Research & Verification Study

> **Objective:** Evaluate authentication patterns, gating friction, and official MCP/API feasibility across 100 popular SaaS applications to determine readiness for agentic automation in Composio.

---

## Executive Summary

We conducted a dual-agent research study evaluating 100 SaaS applications across 10 core verticals. Rather than trusting raw model outputs, findings were subjected to adversarial verification and a line-by-line human audit across 10 high-disagreement applications against official developer documentation.

### Key Macro Findings

* **76% Ready to Build:** 76 out of 100 applications provide open REST/GraphQL APIs with self-serve credential creation.
* **17% Enterprise / Gated:** 17 applications require customer enterprise contracts, sales underwriting, or platform review (BYOK enterprise moat).
* **5% Genuinely Blocked:** 5 applications lack any usable public cloud APIs (e.g., PitchBook, Waterfall.io, fanbasis).
* **2% CLI Wrappers:** Tools without cloud APIs that can execute locally via terminal binaries (e.g., Mermaid CLI).
* **87% Protocol Standardization:** 87 apps rely on standard Bearer API Keys (45) or OAuth 2.0 (42), requiring zero custom connector logic for Composio.
* **Inter-Model Disagreement:** Gemini and Perplexity disagreed on at least one critical dimension across **76 of 100 apps**, showing that unverified automated scraping produces material inaccuracies.

---

## 10-App Human Hand-Check Audit Matrix

To evaluate the empirical accuracy of automated agents, 9 high-disagreement applications and 1 consensus baseline (Slack) were audited directly against vendor primary sources:

| # | Application | Domain | Official API | Official MCP? | Human-Verified Verdict | Audit Confidence | Primary Source |
|---|---|---|:---:|:---:|---|---|---|
| 1 | **Fathom** | fathom.video | Yes | Yes | **Ready to Build** | High *(dev vs support URL noted)* | [developers.fathom.ai](https://developers.fathom.ai) |
| 2 | **Pumble** | pumble.com | Yes | Yes | **Ready to Build** | High *(Help center verified)* | [pumble.com/help](https://pumble.com/help/integrations/automation-workflow-integrations/how-to-use-the-pumble-mcp-server/) |
| 3 | **Grain** | grain.com | Yes | Yes | **Ready to Build** | High *(PAT for MCP verified)* | [developers.grain.com](https://developers.grain.com/) |
| 4 | **Otter.ai** | otter.ai | Yes | Yes | **Gated (API) / MCP Available** | High *(10 req/s limit verified)* | [help.otter.ai](https://help.otter.ai/hc/en-us/articles/36130822688279-Otter-ai-Public-API) |
| 5 | **PitchBook** | pitchbook.com | Yes | No | **Unverified (Do Not Build)** | Unverified *(Requires direct docs)* | [pitchbook.com](https://pitchbook.com/products/direct-data) |
| 6 | **WhatsApp Business** | facebook.com | Yes | Yes | **Ready with Access Controls** | High *(System user flow verified)* | [developers.facebook.com](https://developers.facebook.com/docs/whatsapp/cloud-api/get-started) |
| 7 | **Google Ads** | google.com | Yes | Yes | **Ready with Access Controls** | High *(Token sunset verified)* | [developers.google.com](https://developers.google.com/google-ads/api/docs/developer-toolkit/mcp-server) |
| 8 | **Notion** | notion.so | Yes | Yes | **Ready to Build** | High *(mcp.notion.com verified)* | [developers.notion.com](https://developers.notion.com/guides/mcp/get-started-with-mcp) |
| 9 | **Stripe** | stripe.com | Yes | Yes | **Ready to Build** | High *(mcp.stripe.com verified)* | [docs.stripe.com/mcp](https://docs.stripe.com/mcp) |
| 10 | **Slack** | slack.com | Yes | Yes | **Ready to Build** | High *(Admin approval noted)* | [docs.slack.dev](https://docs.slack.dev/ai/slack-mcp-server/) |

### Empirical Agent Performance on Sample
* **Gemini Raw Extraction:** `50.0%` (5/10 accurate) — Caught open REST APIs and MCP releases, but missed WhatsApp Meta verification, Otter plan limits, and PitchBook sales gating.
* **Perplexity Web Audit:** `60.0%` (6/10 accurate) — Strong on compliance gating, but produced false negatives on Fathom, Pumble, and Grain due to subdomain documentation structures.
* **Control Baseline (Slack):** Full consensus on core Web API and OAuth 2.0 bot token architecture.

---

## Where Agents Failed: Systematic Error Analysis

1. **Systematic MCP Undercounting:** Both agents initially missed that Fathom, Pumble, Notion, Stripe, and Google Ads all provide official, vendor-hosted MCP servers.
2. **Subdomain False Negatives:** Perplexity marked tools like Pumble and Grain as "Blocked" because developer docs reside on subdomains (`api.grain.com`, `help.pumble.com`).
3. **Outdated Auth & Sunset Features:** Both models cited legacy Google Ads Developer Tokens, failing to catch that Google officially sunset them on September 9, 2026, in favor of Cloud Project access tiers.

---

## Repository Structure

```
├── data/
│   ├── apps_100.json                  # Complete 100-app dataset across 10 verticals
│   ├── macro_insights.json            # Aggregated statistics and breakdown counts
│   └── sample_audit_10.json           # 10-app deep-dive human verification audit
├── build_dashboard.py                 # Generates the self-contained executive case study
├── composio_agent.py                  # 2-pass Python research agent and spec generator
├── test_pipeline.py                   # Automated unit test suite (10 test cases)
├── verified_10_apps_audit.csv         # Full spreadsheet export with official documentation URLs
├── verified_10_apps_audit_corrected.xlsx # Formatted Excel audit with confidence ratings
├── index.html                         # Self-contained single-page executive case study
└── README.md                          # Project documentation
```

---

## Quickstart & Verification

### 1. Run Automated Unit Tests (10 Passed)
Verify schema compliance, buildability counts, and cross-verification logic:
```bash
python test_pipeline.py
```

### 2. Run the 2-Pass Research Agent
Inspect verification and tool specification generation for tricky targets:
```bash
# Audit specific target with gating controls
python composio_agent.py --app "WhatsApp Business"

# Audit standard self-serve application
python composio_agent.py --app "Fathom"

# Output summary stats across all 100 apps
python composio_agent.py --stats
```

### 3. Open the Interactive Dashboard
Open `index.html` in any modern web browser or visit the live deployment:
👉 **[Live Case Study](https://farinattar.github.io/Composio-Takehome/)**
