## Part 1
We are given a Minecraft datapack with a bunch of functions. Since `elfcraft:initchecks` is the thing we use to start the search, let's start there.
It's pretty simple: just sets a scoreboard objective to 0, calls a bunch of functions (228 checks), and after it all if the scoreoboard value is 228 then we've "found" an ELF.

Let's take a look at one of the checks now. It follows a similar pattern of setting an objective to 0, doing a bunch of checks, then checking the objective's value.
However, this time each check is just for a block at a specific location. If enough blocks are in the right place, we've passed the check. 

Now, we might start by manually looking through the first few checks and placing some of these blocks in Minecraft (or drawing them out on a grid, etc.) and arrive at something like this:
![image](https://user-images.githubusercontent.com/46304966/111165747-c6541880-8575-11eb-8fc3-9a6eb90d8e53.png)

It seems like each check is looking for some picture of a byte, and hopefully these bytes seem very familiar—the ELF header! 
From here, the task is to write a script that "extracts" the bytes from the checks and write them to a file.

## Part 2
The generated ELF is pretty small. It simply reads in one byte and XORs each byte of a string with the input byte, then prints it out.
Since it's only one byte, we can just brute-force it until the program spits out a flag.

