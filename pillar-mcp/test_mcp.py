import json, mcp_server as m
def t_init(): assert m.handle({"id":1,"method":"initialize"})["result"]["serverInfo"]["name"]=="pillar-fabric"
def t_list(): assert {x["name"] for x in m.handle({"id":2,"method":"tools/list"})["result"]["tools"]}=={"pillar_products","pillar_brand_facts"}
def t_call(): assert "Security Desk" in m.handle({"id":3,"method":"tools/call","params":{"name":"pillar_products"}})["result"]["content"][0]["text"]
def t_unknown(): assert m.handle({"id":4,"method":"tools/call","params":{"name":"x"}})["error"]["code"]==-32602
def t_notif(): assert m.handle({"method":"notifications/initialized"}) is None
for k,v in list(globals().items()):
    if k.startswith("t_"): v(); print("ok",k)
