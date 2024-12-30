class Foo():
    def __init__(self):
        self._spam = 0

    @property
    def spam(self):
        print("in the getter: ")
        return self._spam

    @spam.setter
    def spam(self, move):
        print("in the setter: ")
        self._spam = move + self._spam

f = Foo()
f.spam = 2
print(f.spam)