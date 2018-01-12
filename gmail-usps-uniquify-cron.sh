#!/usr/bin/env bash
LOG=/usr/local/log/usps_uniquify.log
BIN=/Users/packy/bin
$BIN/gmail-usps-uniquify.py &>> $LOG
