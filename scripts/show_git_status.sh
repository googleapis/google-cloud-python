#!/bin/bash
set -e

echo 'git --version:'
echo '------------------------------------'
git --version

# SEP
echo '===================================='
# SEP

echo 'git status:'
echo '------------------------------------'
git status

# SEP
echo '===================================='
# SEP

echo 'git remote -vv:'
echo '------------------------------------'
git remote -vv

# SEP
echo '===================================='
# SEP

echo 'git branch -vv:'
echo '------------------------------------'
git branch -vv

# SEP
echo '===================================='
# SEP

echo 'git branch -a:'
echo '------------------------------------'
git branch -a

# SEP
echo '===================================='
# SEP

echo 'git log -5:'
echo '------------------------------------'
git --no-pager log -5

# SEP
echo '===================================='
# SEP

echo 'git log -5 master:'
echo '------------------------------------'
git --no-pager log -5 master

# SEP
echo '===================================='
# SEP

echo 'git log -5 origin/master:'
echo '------------------------------------'
git --no-pager log -5 origin/master
