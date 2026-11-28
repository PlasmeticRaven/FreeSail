#!/bin/bash
# FreeSail's launcher for macOS (package 130; tools/bundle.py writes it into the download).
# It runs the game with the Python in this folder (Apple silicon's or Intel's, by the
# machine) and nothing of the machine's own: the interpreter by its own path, -I (no user
# site, no PYTHON* variables), -B (nothing written beside the code), -X utf8.
HERE="$(CDPATH= cd -- "$(/usr/bin/dirname -- "$0")" && pwd -P)"

case "$(/usr/bin/uname -m)" in
    arm64) PY="$HERE/python-arm64/bin/python3.11" ;;
    x86_64) PY="$HERE/python-x86_64/bin/python3.11" ;;
    *) echo "FreeSail runs on a Mac with Apple silicon or Intel; this is $(/usr/bin/uname -m)."; exit 1 ;;
esac
if [ ! -x "$PY" ] || [ ! -f "$HERE/game/freesail/__main__.py" ]; then
    echo
    echo "  FreeSail cannot start from here: not all of its folder was unpacked."
    echo "  Double-click the zip you downloaded again, and open FreeSail.command in the"
    echo "  folder it makes."
    echo
    exit 1
fi

# The browser's "downloaded from the internet" mark, which the Mac's unzip gives every file
# in the folder: once you have opened this launcher, the rest of the download (the Python
# and its libraries, the game) is yours too, and is not asked about file by file. Only the
# download's own folders: nothing beside them.
/usr/bin/xattr -dr com.apple.quarantine "$HERE/python-arm64" "$HERE/python-x86_64" \
    "$HERE/game" "$HERE/licences" 2>/dev/null

unset PYTHONHOME PYTHONPATH PYTHONSTARTUP PYTHONUSERBASE PYTHONEXECUTABLE __PYVENV_LAUNCHER__
export PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PYTHONUTF8=1

/bin/cat <<WORDS

  FreeSail ({{NAME}}) is starting.

  This window is the game's server: keep it open while you play.
  In a few seconds your web browser opens the harbour, at
      http://localhost:8000/harbour
  (if it does not, open that address yourself). Begin with "A first passage".

  To stop the game: press Control-C in this window, or close it.

  Your saves and settings are kept in
      ~/Library/Application Support/FreeSail
  not in this folder: a newer download keeps them.

WORDS

"$PY" -I -B -X utf8 -m freesail "$@"
code=$?
echo
echo "  FreeSail has stopped (exit code $code). You can close this window."
if [ "$code" != "0" ] && [ "$code" != "130" ]; then
    echo "  If that was not you, START HERE.txt says where to tell us what went wrong."
fi
echo
exit $code
