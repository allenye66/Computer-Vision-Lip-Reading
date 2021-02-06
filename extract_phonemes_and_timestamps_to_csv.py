inputfile = open('/Users/allen/Desktop/Automated-Speech-Recognition/align_example.txt')

for i in range(4): inputfile.next() # skip first four lines
for line in inputfile:
    print(line)

