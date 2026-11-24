"""
Fix confirmed MCP undercounting errors and other factual corrections
based on cross-audit from external AI reviewer against official docs.

Confirmed fixes (all verified via live web search):
1. Fathom: official_mcp false->true (https://api.fathom.ai/mcp)
2. HubSpot: official_mcp false->true (https://mcp.hubspot.com)
3. Notion: official_mcp false->true (https://mcp.notion.com/mcp)
4. Stripe: official_mcp false->true (https://mcp.stripe.com)
5. Linear: official_mcp false->true (https://mcp.linear.app/mcp)
6. Sentry: already true, but ground_truth text needs update
7. PitchBook: soften $25k claim to "Enterprise sales contract"
8. Front: fix JWT -> Bearer Token
"""
import json

# ============================================================
# FIX sample_audit_25.json
# ============================================================
with open("data/sample_audit_25.json", "r", encoding="utf-8") as f:
    audit = json.load(f)

fixes_audit = {
    "Fathom": {
        "official_mcp": True,
        "auth_type": "API Key (Bearer) / OAuth 2.0",
        "access_gating": "Self-serve (User Settings -> API Access; plan entitlement may vary)",
        "docs_url": "https://developers.fathom.ai/api-overview",
        "ground_truth": "Ready to Build (Official MCP at api.fathom.ai/mcp)",
        "winner": "Both Partially Correct (Gemini got API right; both missed official MCP)"
    },
    "HubSpot": {
        "official_mcp": True,
        "ground_truth": "Ready to Build (Official MCP at mcp.hubspot.com)",
        "winner": "Perplexity Correct on auth (deprecated HAPIKEY); both missed official MCP"
    },
    "Notion": {
        "official_mcp": True,
        "docs_url": "https://developers.notion.com/",
        "gemini_status": "Available (Official MCP)",
        "ground_truth": "Ready to Build (Official MCP at mcp.notion.com/mcp)",
        "winner": "Gemini Correct on MCP existence (Notion launched official MCP server)"
    },
    "Stripe": {
        "official_mcp": True,
        "ground_truth": "Ready to Build (Official MCP at mcp.stripe.com)",
        "winner": "Gemini Correct on MCP existence (Stripe launched official MCP at docs.stripe.com/mcp)"
    },
    "Linear": {
        "official_mcp": True,
        "ground_truth": "Ready to Build (Official MCP at mcp.linear.app)",
        "winner": "Gemini Correct on MCP existence (Linear launched official MCP server)"
    },
    "Sentry": {
        "ground_truth": "Ready to Build (Official MCP at mcp.sentry.dev)"
    },
    "PitchBook": {
        "access_gating": "Enterprise Contract Gated (sales contact required)",
        "ground_truth": "Feasible with Gating (Enterprise sales contract)",
        "winner": "Perplexity Correct (Gemini missed enterprise paywall)"
    },
    "Front": {
        "auth_type": "Bearer API Token / OAuth 2.0"
    }
}

for item in audit:
    name = item["name"]
    if name in fixes_audit:
        for key, val in fixes_audit[name].items():
            item[key] = val

with open("data/sample_audit_25.json", "w", encoding="utf-8") as f:
    json.dump(audit, f, indent=2, ensure_ascii=False)

print("Fixed sample_audit_25.json")

# ============================================================
# FIX apps_100.json - update MCP fields for the same apps
# ============================================================
with open("data/apps_100.json", "r", encoding="utf-8") as f:
    apps = json.load(f)

# Map of app names to their MCP fix
mcp_fixes = {
    "Fathom": {
        "mcp_ready": True,
        "primary_auth": "API Key (Bearer) / OAuth 2.0",
    },
    "HubSpot": {
        "mcp_ready": True,
    },
    "Notion": {
        "mcp_ready": True,
    },
    "Stripe": {
        "mcp_ready": True,
    },
    "Linear": {
        "mcp_ready": True,
    },
    # Sentry already true
    # Supabase already true
    "PitchBook": {
        "gating_status": "Enterprise Contract Gated (sales contact required)",
    },
    "Front": {
        "primary_auth": "Bearer API Token / OAuth 2.0",
    }
}

fixed_count = 0
for app in apps:
    name = app["name"]
    if name in mcp_fixes:
        for key, val in mcp_fixes[name].items():
            app[key] = val
            fixed_count += 1

with open("data/apps_100.json", "w", encoding="utf-8") as f:
    json.dump(apps, f, indent=2, ensure_ascii=False)

print(f"Fixed apps_100.json ({fixed_count} field updates)")

# ============================================================
# Update macro_insights.json MCP count
# ============================================================
with open("data/macro_insights.json", "r", encoding="utf-8") as f:
    macro = json.load(f)

# Recount MCP-ready apps
mcp_count = sum(1 for a in apps if a.get("mcp_ready", False))
macro["mcp_ready_count"] = mcp_count
# Update sample audit accuracy note
macro["sample_audit_note"] = "Cross-audited: 6 MCP fields corrected (Fathom, HubSpot, Notion, Stripe, Linear confirmed official MCP servers)"

with open("data/macro_insights.json", "w", encoding="utf-8") as f:
    json.dump(macro, f, indent=2, ensure_ascii=False)

print(f"Updated macro_insights.json (MCP-ready count: {mcp_count})")
print("All fixes applied successfully!")
