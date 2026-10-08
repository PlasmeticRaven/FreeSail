import json,glob,os,sys
root="D:/Projects/FreeSail"
files=sorted(glob.glob(root+"/FreeSail-gate-m5c/*.json")+glob.glob(root+"/FreeSail-gate-m5c/saves/*.json")+glob.glob(root+"/FreeSail-gate-m5c-b/*.json")+glob.glob(root+"/FreeSail-gate-m5c-b/saves/*.json"))
data={}
for f in files:
    d=json.load(open(f,encoding='utf-8'))
    key=os.path.relpath(f,root).replace(os.sep,'/')
    data[key]=d
def sig(d):
    return [json.dumps(x,sort_keys=True,ensure_ascii=False) for x in d.get('inputs',[])]
sigs={k:sig(d) for k,d in data.items()}
keys=sorted(data,key=lambda k:(data[k]['scenario']['name'],data[k]['end_tick']))
print("%-95s %-28s %8s %5s"%("save","scenario","end_tick","inputs"))
for k in keys:
    d=data[k]
    print("%-95s %-28s %8d %5d  start=%s"%(k[-95:],d['scenario']['name'][:28],d['end_tick'],len(d['inputs']),d['scenario'].get('start_time')))
print()
# prefix relations
for a in keys:
    for b in keys:
        if a==b: continue
        sa,sb=sigs[a],sigs[b]
        if len(sa)<=len(sb) and sb[:len(sa)]==sa:
            if len(sa)==len(sb):
                if a<b: print("IDENTICAL inputs:",a,"==",b)
            else:
                print("PREFIX:",a,"->",b)
