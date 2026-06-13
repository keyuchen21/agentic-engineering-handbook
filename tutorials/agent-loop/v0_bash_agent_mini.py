#!/usr/bin/env python
"""v0_bash_agent_mini.py - Mini Claude Code (Compact)"""
from anthropic import Anthropic; from dotenv import load_dotenv; import subprocess as sp, sys, os
load_dotenv(); C = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"), base_url=os.getenv("ANTHROPIC_BASE_URL")); M = os.getenv("MODEL_NAME", "claude-sonnet-4-20250514")
T = [{"name":"bash","description":"Shell cmd. Read:cat/grep/find/rg/ls. Write:echo>/sed. Subagent(for complex subtask): python v0_bash_agent_mini.py 'task'","input_schema":{"type":"object","properties":{"command":{"type":"string"}},"required":["command"]}}]
S = f"CLI agent at {os.getcwd()}. Use bash to solve problems. Spawn subagent for complex subtasks: python v0_bash_agent_mini.py 'task'. Subagent isolates context and returns summary. Be concise."

def chat(p, h=[]):
    h.append({"role":"user","content":p})
    while (r:=C.messages.create(model=M,system=S,messages=h,tools=T,max_tokens=8000)).stop_reason=="tool_use":
        h.append({"role":"assistant","content":[{"type":b.type,**({"text":b.text}if hasattr(b,"text")else{"id":b.id,"name":b.name,"input":b.input})}for b in r.content]})
        h.append({"role":"user","content":[{"type":"tool_result","tool_use_id":b.id,"content":(print(f"\033[33m$ {b.input['command']}\033[0m"),o:=sp.run(b.input["command"],shell=1,capture_output=1,text=1,timeout=300),print(o.stdout+o.stderr or"(empty)"))and""or(o.stdout+o.stderr)[:50000]}for b in r.content if b.type=="tool_use"]})
    h.append({"role":"assistant","content":[{"type":b.type,**({"text":b.text}if hasattr(b,"text")else{"id":b.id,"name":b.name,"input":b.input})}for b in r.content]})
    return "".join(b.text for b in r.content if hasattr(b,"text"))

if __name__=="__main__":[print(chat(sys.argv[1]))]if len(sys.argv)>1 else[print(chat(q,h))for h in[[]]for _ in iter(int,1)if(q:=input("\033[36m>> \033[0m"))not in("q","")]
