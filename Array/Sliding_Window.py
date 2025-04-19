# Sliding window: Efficiently solves subarray problems with fixed or variable window sizes
# Time complexity: O(n), where n is the size of the input array'
# Space complexity: O(n), where n is the size of the input array'
'''
[1, 3, 5, 2, 8, 1, 5]
Now say we want to find the maximum sum of any subarray of size 3.

We use a "window" of size 3 that slides through the array:
We "slide" the window by removing the first element of the previous window and adding the next one.

[1, 3, 5] 2  8  1  5   → Sum = 9  
1 [3, 5, 2] 8  1  5   → Sum = 10  
1  3 [5, 2, 8] 1  5   → Sum = 15  
1  3  5 [2, 8, 1] 5   → Sum = 11  
1  3  5  2 [8, 1, 5]  → Sum = 14  
'''

class Array:
    def __init__(self, *args):
        self.input = args
    
    def MaxSumK_Subarray(self, k):
        arrlist = list(arrlist)
        window_sum = sum(arrlist[0:k])
        max_sum = window_sum
        for i in range(k, len(arrlist)):
            print(f" itr {i} : total {k} so {i-k}")
            window_sum = window_sum - arrlist[i-k] + arrlist[i]
            print(f"window sum {window_sum}")
            max_sum = max(max_sum, window_sum)
        return max_sum
        
    def longestSubStr(self):
        pass
        
        
        
def main():
    arr = Array(1, 4, 2, 10, 23, 3, 1, 0, 20)
    k = 2
    result = arr.MaxSumK_Subarray(k)
    print(f"Maximum sum of any subarray of size {k} is: {result}")

if __name__ == "__main__":
    main()