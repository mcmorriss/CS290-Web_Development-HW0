# Author: Michael Morriss
# Date: 11/11/2020
# Description: Function that takes list of integers and squares every value by mutation.
def square_list(num_list):
    """
    Function that takes a list from the user and mutates the list so that
    each element of the list is now squared the original value.
    """
    for num in range(len(num_list)):
        num_list[num] = num_list[num] * num_list[num]