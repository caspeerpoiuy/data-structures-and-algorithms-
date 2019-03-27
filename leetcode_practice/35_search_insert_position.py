class Solution(object):
    def searchInsert(self, nums, target):
        if target in nums:
            return nums.index(target)
        else:
            nums.append(target)
            nums.sort()
            return nums.index(target)


if __name__ == '__main__':
    soulution = Solution()
    print(soulution.searchInsert([1,3,5,6], 2))
