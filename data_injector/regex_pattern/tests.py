import string
import random
from django.test import TestCase
from pyparsing import *

int_range = Word(nums) + Suppress("-") + Word(nums)
int_choice = Word(nums) + OneOrMore(Suppress(",") + Word(nums))
char_choice = Word(alphanums) + OneOrMore(Suppress(",") + Word(alphanums))
star = Word(alphanums) + "*"
parser = int_choice.setResultsName("choice") | \
         int_range.setResultsName("range") | \
         char_choice.setResultsName("char_choice") | \
         star.setResultsName("star")

def generate(pattern):
    value = parser.parseString(pattern)
    print value.asDict()
    if 'range' in value.asDict():
        print "range"
        return random.randint(int(value[0]),int(value[1]))
    if 'choice' in value.asDict():
        print "choice"
        return int(random.choice(value))
    if 'char_choice' in value.asDict():
        return random.choice(value)
    if 'star' in value.asDict():
        new_val =[]
        for val in value:
            if val == "*":
                new_val.append("".join([random.choice(string.letters) for x in range(5)]))
            else:
                new_val.append(val)
        return "".join(new_val)


class TestRegex(TestCase):

    def test_operator(self):
        a = "1-10"
        i = generate("1-10")
        self.assertTrue(isinstance(i,int) and i >= 1 and i <= 10)
        i = generate("10-20")
        self.assertTrue(isinstance(i,int) and i >= 10 and i <= 20)
        i = generate("10,20")
        print i
        self.assertTrue(isinstance(i,int) and (i==10 or i==20))
        i = generate("abc,bca,cba")
        self.assertTrue(i in ["abc","bca","cba"])
        i = generate("A*")
        print i
        self.assertEquals(i[0],"A")
