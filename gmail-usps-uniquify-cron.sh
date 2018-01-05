#!/usr/bin/env bash
LOG=/usr/local/log/usps_uniquify.log
BIN=/Users/packy/bin
echo Starting $BIN/gmail-usps-uniquify.py
$BIN/gmail-usps-uniquify.py &>> $LOG
