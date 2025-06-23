
def test_func(computer):
    result = computer(1, 2)
    print(result)


# def computer(x, y):
#     return x + y


test_func(lambda x, y: x + y)


