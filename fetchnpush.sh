#!/bin/bash

git fetch origin master
git merge origin/master
git push heroku master
