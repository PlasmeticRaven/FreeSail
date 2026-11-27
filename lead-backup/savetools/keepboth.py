"""Resolve the one conflict in docs/dev/TuningNotes.md by keeping both sections whole: ours,
a blank line, theirs (the resolution the cloud's run 141 was staged with)."""
p='docs/dev/TuningNotes.md'
L=open(p).read().split('\n')
a=[i for i,l in enumerate(L) if l.startswith('<<<<<<< ')]
m=[i for i,l in enumerate(L) if l=='=======']
z=[i for i,l in enumerate(L) if l.startswith('>>>>>>> ')]
assert len(a)==1 and len(z)==1, (a,z)
mid=[i for i in m if a[0]<i<z[0]]; assert len(mid)==1
ours=L[a[0]+1:mid[0]]; theirs=L[mid[0]+1:z[0]]
out=L[:a[0]]+ours+['']+theirs+L[z[0]+1:]
open(p,'w').write('\n'.join(out))
print("kept both:", len(ours), "and", len(theirs), "lines")
