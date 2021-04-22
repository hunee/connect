#
# .DS_Store 파일을 git에 포함시키지 않기
#
$ find . -name .DS_Store -print0 | xargs -0 git rm --ignore-unmatch

# git 원하는 폴더 삭제 
$ git rm -rf backend/deps

1-1. git rm -rf {파일 및 폴더명} // 모두 삭제
1-2. git rm -r --cached {파일 및 폴더명} // 원격 저장소에 있는것만 삭제
2. git commit -m "commit 내용"
3. git push -u origin master


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
