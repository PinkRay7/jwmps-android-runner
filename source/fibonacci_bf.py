def fibonacci(num):
    num1 = 0
    num2 = 1
    series = 0
    i = 0
    while i<=num:
        print(series)
        num1 = num2
        num2 = series
        series = num1 + num2
        i+= 1

if __name__ == "__main__":
    # running function after taking user input
    num = int(input('Enter how many numbers needed in Fibonacci series : '))
    fibonacci(num)