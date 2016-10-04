#!/bin/bash
set -ev

git status
echo '===================================='
git remote -vv
echo '===================================='
git branch -vv
echo '===================================='
git branch -a
