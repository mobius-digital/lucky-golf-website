#!/bin/sh
# build.py deletes v9/out, which kills any server holding it: rebuild, then serve.
cd "$(dirname "$0")/../.." || exit 1
python v9/tools/build.py || exit 1
exec python -m http.server 8795 --directory v9/out
