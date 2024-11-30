This text file will be a summary of the progress and challenges faced in making the project.

This project is option 1 of the project and it is a Quine-McCluskey algorithm.
It was implemented in python3 and later on implemented in perl language.
A small Python code was made to generate .PLA format file but it is not very intrusive.
To ensure the algorithm was correct and accurate, we ran the same sample of code on an online solver (atozmath.com) and verified the solution.
The python script produces a file in pla format called (output.pla) and prints the output in the terminal.
One of the hardest challenges to this assignment was to parse the input given that only half of it was parsing correctly and the other was not working accordingly.
When tested with the file called Z9sym.pla from the GitHub repository, the code would work for around 100 Minterms before it started breaking down. 
The Z9sym.pla code had 9 inputs,1 output, and 420 minterms. It could be due to the fact that we would run out of space that we are allowed to operate on.
A large sample of a successful test case file was 7 inputs,1 output, and 99 minterms. The answer was checked by atozmath.com to verify.
The Code reads a static file that already exists. I will include the file in the Zip package.


As promised as well, I implemented the project in perl language.
The code for the perl language can handle only light amount of inputs and minterms.
The perl code worked on a 4 input and 9 minterm input file which is attached in the zip folder.
