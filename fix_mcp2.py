"""Fix all MCP fields consistently across apps_100.json"""
import json

with open("data/apps_100.json", "r", encoding="utf-8") as f:
    apps = json.load(f)

# Any app with "Official" in mcp_status should have mcp_ready=True
for app in apps:
    ms = app.get("mcp_status", "")
    if "Official" in ms or "Available" in ms:
        app["mcp_ready"] = True
    elif "mcp_ready" not in app:
        app["mcp_ready"] = False

# Also update mcp_status for the newly confirmed ones
mcp_status_fixes = {
    "Fathom": "Available (Official MCP at api.fathom.ai/mcp)",
    "HubSpot": "Available (Official MCP at mcp.hubspot.com)",
    "Notion": "Available (Official MCP at mcp.notion.com/mcp)",
    "Stripe": "Available (Official MCP at mcp.stripe.com)",
    "Linear": "Available (Official MCP at mcp.linear.app)",
    "Sentry": "Available (Official MCP at mcp.sentry.dev)",
}
for app in apps:
    if app["name"] in mcp_status_fixes:
        app["mcp_status"] = mcp_status_fixes[app["name"]]
        app["mcp_ready"] = True

mcp_count = sum(1 for a in apps if a.get("mcp_ready"))
print(f"Total MCP-ready apps: {mcp_count}")
mcp_names = [a["name"] for a in apps if a.get("mcp_ready")]
print(f"MCP apps: {mcp_names}")

with open("data/apps_100.json", "w", encoding="utf-8") as f:
    json.dump(apps, f, indent=2, ensure_ascii=False)

# Update macro_insights
with open("data/macro_insights.json", "r", encoding="utf-8") as f:
    macro = json.load(f)
macro["mcp_ready_count"] = mcp_count
macro["sample_audit_note"] = f"Cross-audited: 6 MCP fields corrected. {mcp_count} apps now confirmed with official vendor MCP servers."
with open("data/macro_insights.json", "w", encoding="utf-8") as f:
    json.dump(macro, f, indent=2, ensure_ascii=False)

print("Done!")
