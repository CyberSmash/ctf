# Description

I made a simple brain-fuck language emulation program written in C. 
The [ ] commands are not implemented yet. However the rest functionality seems working fine. 
Find a bug and exploit it to get a shell. 

Download : http://pwnable.kr/bin/bf
Download : http://pwnable.kr/bin/bf_libc.so

Running at : nc pwnable.kr 9001

# Step 0 - What does bf do?

The bf program takes in a series of BrainFuck commands, except the loop commands (`[`, `]`) and will execute them, printing out the results.

# Step 1 - Find the bug.

BrainFuck uses a simple pointer to a "tape". This pointer can be manipulated going forwards and backwards across the tape. You can then
perform actions such as increment, decrement, read a character, and print a character. 

`p` in the application (the pointer) lives in the `.data` section of the binary as a global variable. So does `tape` (the buffer) which is 
acted upon.

The primary bug in this case is that p is not bounds checked, meaning that we can move p backwards (or forwards for that matter) almost
arbitrarally. 

In the case of this binary, the memory layout looks like this (see sploit for specific offsets).

[.plt.got section]
[stdin]
[stdout]
[p]
[tape]

As `p` starts off pointing to `tape`, we can move `p` back to point to itself, and modify the least significant byte to make a dramatic
jump into the .plt.got section to perform an overwrite.

# Step 2 - What to call

A call to `system` would be the obvious answer, however there are two complications. The biggest complication is that `system` isn't used anywhere
in the application. This means that we don't know the address. We can look up the address in libc, but libc's base address changes with each run. The best 
we can do at the moment is to identify the offset from the libc that we are given. What this means is we'll need to find a way to leak the address
of libc, or at least a function inside of libc.

## Solving complication #1

The .plt.got table will fill in the actual address of the function inside of libc, once it has been executed, to avoid having to look it up again.
Therefore if we can move our pointer `p` to a function that has already been called, we can leak it's address. Since we have been given a copy of the
libc.so.6 being used on the server, we can then use whatever pointer we just leaked to calculate the offset to the `system` function as it will
remain relative. This means as soon as we solve Complication #2, we can solve this complication.


## Complication #2
The second complication is that we need to overwrite the function pointer of an address that we can pass a pointer to. This function must also
live in the .plt.got (otherwise we can't overwrite anything) and must be used in some convenient location in the application, and operate
off of a pointer we can control.

## Solving Complication #2
There are only a couple functions which have pointers passed to them:

1. `setvbuf`
2. `memset`
3. `strlen`

`strlen` would be the obvious choice as it takes in one pointer. However, as we don't control the stack, and the only location (in main)
where `strlen` is used operates on a variable on the stack, calling `strlen` is out of the question. If we controlled the stack, and could
place the proper pointer ontop of the stack, then this would work fine. In addition to this problem, strlen is called with every 
symbol that is parsed from our input. This means we cannot change the .plt.got table entry for more than one byte, as the call
to strlen must remain valid. We cannot change all 4 bytes at once, and changing any pointer requires the parsing of 8 characters
(".>" x 4).

`memset` might be possible. However, memset suffers from the same issue that strlen has where it operates only on a stack variable.
Therefore `memset` is out as well.

That leaves `setvbuf`. This function has several benefits. First, it's called, and is therefore resolved before we do anything, which means
if we can overwrite it we can also read the pre-existing value and thus leak out the address. Second, it takes in a pointer in the form
of `stdout`. `stdout` lives in our application and will be at a predictible location. In fact it's a pointer that gets dereferenced to point
to the libc `FILE* stdout`. 

This means that a predictable pointer we can control is being passed to a function we can also control. As x86's calling convention
pushes things on the stack right-to-left, and the argument we are worried about is the last one to be pushed onto the stack, 
we don't care much about what else gets pushed on the stack. We now have a way of getting our `system` call.

# How to call setvbuf?

`setvbuf` only gets called twice -- at the beginning of the program. So how are we going to force it to be called again?
Simple, we'll replace a second function in our .plt.got with a call to `main`, another predictable address. 

But which one? Well, as it turns out we only need to output data one time -- to leak the address of `setvbuf` in libc to 
calculate the offset to `system` in libc. Therefore, once we've done that, and since we're already in the right area,
we can also overwrite `putchar` with the address of `main`. All we have to do is make sure we wait to do this AFTER
we have already read out the address of `setvbuf`.

The end result of this is that we will issue a '.' (`putchar`) command in our BrainFuck code as the last command, once all of our 
.plt.got and tape are set up correctly. This will kick off main all over again, and call `setvbuf` all over again.

# Shell String

We also have to get `/bin/sh` into our application at a predictable address. This is surprisingly easy, as we just require 
7 `getchar` calls in the beginning of our brainfuck code. This will place `/bin/sh` into our `tape`, variable
which lives at a predictible location.

This `tape` address will be the address we use in our call to system. To use it we will write the value of `tape` to 
the `stdout` pointer so that the first argument sent to `setvbuf` is now `tape`. 

# Pwn

Look at the script `bf_splot.py` to see how this allcomes together. 
