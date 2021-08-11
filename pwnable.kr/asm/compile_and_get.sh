#!/usr/bin/env bash

nasm -f elf64 ./chrisasm.asm -o ./chrisasm.o
gcc chrisasm.o -o chrisasm -nostdlib
objdump -d ./chrisasm|grep '[0-9a-f]:'|grep -v 'file'|cut -f2 -d:|cut -f1-6 -d' '|tr -s ' '|tr '\t' ' '|sed 's/ $//g'|sed 's/ /\\x/g'|paste -d '' -s |sed 's/^/"/'|sed 's/$/"/g'
