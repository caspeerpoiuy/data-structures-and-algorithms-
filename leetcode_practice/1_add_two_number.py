class Solution(object):
    """
    depend on system function enumerate to iterate list to get index and value
    take advantage of dictionary storage structure, use index as a unique key and num as value.
    do a loop for this dictionary and get key
    """
    def twoSum(self, nums, target):
        map = {}
        for index, num in enumerate(nums):
            var = target - num
            map.get(0)
            if var in map.values():
                for key, value in map.items():
                    if value == var:
                        return [key, index]
            map[index] = num


if __name__ == '__main__':
    solution = Solution()
    li = solution.twoSum([2, 7, 11, 15], 9)
    print(li)
