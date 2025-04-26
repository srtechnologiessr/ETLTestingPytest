#modules should starts with test_
#functions also should starts with test_

#operators
def test_equality():
    assert 5 == 5 #assert can not be used multiple times in a single test case

def test_not_eauality():
    assert 3 != 5

def test_greater():
    assert 3 < 5

def test_lesser():
    assert 3 < 5