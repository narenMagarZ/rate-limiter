#!/bin/bash

for i in {1..1000}
  do
    echo "Request #$i"
    curl -H "X-Client-Id: 10" http://localhost:8000/api/public/v1/limited
    # sleep 1 # 500ms
  done