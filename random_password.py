import random, string

#required variables
small_letters = string.ascii_lowercase
capital_letters = string.ascii_uppercase
numbers = string.digits
symbols = string.punctuation

my_string = small_letters + capital_letters + numbers

def create_random_password(length):
    password = "".join(random.sample(my_string, length))
    print("The password of length ", length, "is: ", password)
    
    
create_random_password(18)