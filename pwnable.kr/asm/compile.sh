#!/bin/bash

nasm -f elf64 ./chrisasm.asm -o chrisasm.o
ld ./chrisasm.o -o ./chrisasm
