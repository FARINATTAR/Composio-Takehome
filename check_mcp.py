import json
apps=json.load(open('data/apps_100.json','r',encoding='utf-8'))
check=['Sentry','Supabase','Grain','Consensus','GitHub']
for name in check:
    a=[x for x in apps if x['name']==name]
    if a:
        mr = a[0].get('mcp_ready','MISSING')
        ms = a[0].get('mcp_status','MISSING')
        print(f"{name}: mcp_ready={mr}, mcp_status={ms}")
    else:
        print(f"{name}: NOT FOUND")
