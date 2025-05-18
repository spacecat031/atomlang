# IF CONDITION

## introduction to if conditions

if conditions are used to do something when something happens.

# how to use if conditions

lets say you want to make a program that check if a number is equal to another number and if yes it says "its equal".

<pre>if 5 == 5
print("its equal!")
print("yay")
if.end //closes the if conditions so code below doesnt get included
</pre>

this also works with variables.

<pre>
var less = 5
var more = 6
if more == less 
print("its equal!")
print("yay")
if.end //closes the if conditions so code below doesnt get included
</pre>

hmm you may have noticed that this doesnt print anything
thats because its **NOT** equal so it doesnt run.

however if you want to check if a number or a variable is **NOT** equal to a number or variable you should use ?=

why? thats the **NOT** equal check its pretty obvious what it does.

so if you want to code to print something it should look like.

<pre>
var less = 5
var more = 6
if more ?= less 
print("its NOT equal!")
print("yay")
if.end //closes the if conditions so code below doesnt get included
</pre>

or

<pre>if 5 ?= 12
print("its NOT equal!")
print("yay")
if.end //closes the if conditions so code below doesnt get included
</pre>

funfact:operations also work so like 

<pre>if 5 ?= op[5 + 5]
print("its NOT equal!")
print("yay")
if.end //closes the if conditions so code below doesnt get included
</pre>

or

<pre>if 5 ?= op[1 + 4í]
print("its equal!")
print("yay")
if.end //closes the if conditions so code below doesnt get included
</pre>
