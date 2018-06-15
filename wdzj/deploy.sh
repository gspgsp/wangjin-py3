#!/bin/sh
kill -9 `cat twistd.pid`
scrapyd > scrapyd.log &
scrapyd-deploy -p wdzj