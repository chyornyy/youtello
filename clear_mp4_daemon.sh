#!/bin/bash

folder_path="/home/admin/youtello"

if [ -d "$folder_path" ]; then
  find "$folder_path" -type f -name "*.mp4" -delete