#
# .DS_Store 파일을 git에 포함시키지 않기
#
$ find . -name .DS_Store -print0 | xargs -0 git rm --ignore-unmatch

$ vi ~/.gitignore_global
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

.DS_Store
._.DS_Store
**/.DS_Store
**/._.DS_Store

$ git config --global core.excludesfile ~/.gitignore_global
$ git push
$ git pull
