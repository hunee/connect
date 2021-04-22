#!/usr/bin/env bash


upgrade() {
  
  fullpath="$1"
  filename="${fullpath##*/}"                      # Strip longest match of */ from start
  dir="${fullpath:0:${#fullpath} - ${#filename}}" # Substring from 0 thru pos of filename
  base="${filename%.[^.]*}"                       # Strip shortest match of . plus at least one non-dot char from end
  ext="${filename:${#base} + 1}"                  # Substring from len of base thru end
  if [[ -z "$base" && -n "$ext" ]]; then          # If we have an extension and no base, it's really the base
      base=".$ext"
      ext=""
  fi
  #echo -e "$fullpath:\n\tdir  = \"$dir\"\n\tbase = \"$base\"\n\text  = \"$ext\""

  echo "->> upgrade: $fullpath"

  # look for empty dir 
  if [ -d "$base" ]
  then
    cd $base
      git pull
      pip3 install .
    cd ..
  else
    git clone $fullpath --recurse-submodules
    pip3 install ./$base
  fi
  # rest of the logic

  return 1
}

#pip3 install wheel

#pip3 install cffi

#pip3 uninstall cython
upgrade https://github.com/cython/cython


#result=$?
#echo "upgrade [ ${result} ]"

##pip3 uninstall ujson
upgrade https://github.com/ultrajson/ultrajson

##pip3 uninstall PyYAML
upgrade https://github.com/yaml/pyyaml

##pip3 uninstall uvloop
upgrade https://github.com/MagicStack/uvloop

upgrade https://github.com/aaugustin/websockets

##pip3 uninstall uvicorn
upgrade https://github.com/encode/uvicorn

#pip3 uninstall requests
upgrade https://github.com/psf/requests

upgrade https://github.com/encode/starlette
upgrade https://github.com/tiangolo/fastapi


upgrade https://github.com/aio-libs/aiomysql
upgrade https://github.com/aio-libs/aioredis-py

upgrade https://github.com/MagicStack/asyncpg

#pip3 uninstall sqlalchemy
upgrade https://github.com/sqlalchemy/sqlalchemy


upgrade https://github.com/nackjicholson/aiosql


pip3 install aiohttp
##upgrade https://github.com/aio-libs/aiohttp

