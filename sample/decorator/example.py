print ('###### sample 1 start')
# sample1
def outer_function(msg):
    def inner_function():
        print(msg)
    return inner_function

hi_func = outer_function('Hi')
bye_func = outer_function('Bye')

hi_func()
bye_func()

print ('###### sample 2 start')
# sample 2
def decorator_function(original_function):  #1
    def wrapper_function():  #5
        return original_function()  #7
    return wrapper_function  #6


def display():  #2
    print ('display 함수가 실행됐습니다.')  #8

decorated_display = decorator_function(display)  #3

decorated_display()  #4

print ('###### sample 3 start')
# sample 3
def decorator_function(original_function):
    def wrapper_function():
        print ('{} 함수가 호출되기전 입니다.'.format(original_function.__name__))
        return original_function()
    return wrapper_function


def display_1():
    print ('display_1 함수가 실행됐습니다.')


def display_2():
    print ('display_2 함수가 실행됐습니다.')

display_1 = decorator_function(display_1)  #1
display_2 = decorator_function(display_2)  #2

display_1()
display_2()


print ('###### sample 4 start')
# sample 4

@decorator_function  #1
def display_1():
    print ('display_1 함수가 실행됐습니다.')


@decorator_function  #2
def display_2():
    print ('display_2 함수가 실행됐습니다.')

# display_1 = decorator_function(display_1)  #3
# display_2 = decorator_function(display_2)  #4

display_1()
display_2()


print ('###### sample 5 start')
# sample 5

class DecoratorClass:  #1
    def __init__(self, original_function):
        self.original_function = original_function

    def __call__(self, *args, **kwargs):
        print ('{} 함수가 호출되기전 입니다.'.format(self.original_function.__name__))
        return self.original_function(*args, **kwargs)


@DecoratorClass  #2
def display():
    print ('display 함수가 실행됐습니다.')


@DecoratorClass  #3
def display_info(name, age):
    print ('display_info({}, {}) 함수가 실행됐습니다.'.format(name, age))

display()
display_info('John', 25)