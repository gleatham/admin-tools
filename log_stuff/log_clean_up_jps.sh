#!/bin/bash

cleanup_JPS_logs() {
    # JPS logs directory
    dir = /path/to/JPS-logs

    # If $dir is a directory delete all files in the first level
    if [-d "$dir"]; then
        find "$dir" -maxdepth 1 -type f -name "*.jps" -mtime +30 -exec rm -f {} \;

}

cleanup_JPS_logs