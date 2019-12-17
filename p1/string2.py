#!/usr/bin/python3 -tt
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

# Additional basic string exercises


# D. verbing
# Given a string, if its length is at least 3,
# add 'ing' to its end.
# Unless it already ends in 'ing', in which case
# add 'ly' instead.
# If the string length is less than 3, leave it unchanged.
# Return the resulting string.
def verbing(s):
    long = len(s)
    string = s
    if long > 2:
        end = s[long-3] + s[long-2] + s[long-1]
        if end == 'ing':
            string += 'ly'
        else:
            string += 'ing'
    return string


# E. not_bad
# Given a string, find the first appearance of the
# substring 'not' and 'bad'. If the 'bad' follows
# the 'not', replace the whole 'not'...'bad' substring
# with 'good'.
# Return the resulting string.
# So 'This dinner is not that bad!' yields:
# This dinner is good!
def not_bad(s):
    long = len(s)
    string = ''
    flag = 0
    fin = 0
    for i in range(0, long):
        if i > fin:
            flag = 0
        if (s[i] == 'n' and s[i+1] == 'o' and s[i+2] == 't'):
            for j in range(i+2, long):
                if (s[j] == 'b' and s[j+1] == 'a' and s[j+2] == 'd'):
                    string += 'good'
                    fin = j+2
                    flag = 1
        if flag == 0:
            string += s[i]
    return string


# F. front_back
# Consider dividing a string into two halves.
# If the length is even, the front and back halves are the same length.
# If the length is odd, we'll say that the extra char goes in the front half.
# e.g. 'abcde', the front half is 'abc', the back half 'de'.
# Given 2 strings, a and b, return a string of the form
#  a-front + b-front + a-back + b-back
def get_string_intervale(string, ini, fin):
    str = ''
    for i in range(ini, fin):
        str += string[i]
    return str


def front_back(a, b):
    la = len(a)
    lb = len(b)
    ma = la//2
    mb = lb//2
    if ma != la/2:
        ma += 1
    if mb != lb/2:
        mb += 1
    string = get_string_intervale(a, 0, ma) + get_string_intervale(b, 0, mb)
    string += get_string_intervale(a, ma, la) + get_string_intervale(b, mb, lb)
    return string


# Simple provided test() function used in main() to print
# what each function returns vs. what it's supposed to return.
def test(got, expected):
    if got == expected:
        prefix = ' OK '
    else:
        prefix = '  X '
    print('%s got: %s expected: %s' % (prefix, repr(got), repr(expected)))


# main() calls the above functions with interesting inputs,
# using the above test() to check if the result is correct or not.
def main():
    print('\nverbing')
    test(verbing('hail'), 'hailing')
    test(verbing('swiming'), 'swimingly')
    test(verbing('do'), 'do')

    print('\nnot_bad')
    test(not_bad('This movie is not so bad'), 'This movie is good')
    test(not_bad('This dinner is not that bad!'), 'This dinner is good!')
    test(not_bad('This tea is not hot'), 'This tea is not hot')
    test(not_bad("It's bad yet not"), "It's bad yet not")

    print('\nfront_back')
    test(front_back('abcd', 'xy'), 'abxcdy')
    test(front_back('abcde', 'xyz'), 'abcxydez')
    test(front_back('Kitten', 'Donut'), 'KitDontenut')


if __name__ == '__main__':
    main()
