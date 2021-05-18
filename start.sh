#!/bin/bash

memcached -u memcache &
pypy3 -m gunicorn app:app