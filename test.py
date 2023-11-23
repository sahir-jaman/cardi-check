# swapping 2 numbers in place:
x,y= 7,8
x,y = y, x
print(x,y)

# reverse a string 
my_string = "12345"
my_string = my_string[::-1]
print(my_string)

# finding the most frequent item in a list 

my_list = ['a', 'b', 'a', 'c', 'd', 'e']
print(max((my_list), key=my_list.count))

# Let's break down the counts for each element:
# Count of 'a' in my_list: 2
# Count of 'b' in my_list: 1
# Count of 'c' in my_list: 1
# Count of 'd' in my_list: 1
# Count of 'e' in my_list: 1

for index, value in enumerate(my_list):
    print(index, value)

    
my_string = "Python is fun!"
every_second_char = my_string[::-2]
print(every_second_char)
