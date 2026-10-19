number = int(input("Enter an integer: "))

if number <= 1:
    print("Not a Prime Number")

else:
    for i in range(2, number):
        if number % i == 0:
            print("Not a Prime Number")
            break
    else:
        print("Prime Number")