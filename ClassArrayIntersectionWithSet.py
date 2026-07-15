from typing import List

class ClassArrayIntersectionWithSet:
    
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        """
        This method returns the intersection of two integer arrays as a list.
        Each element in the result must be unique.
        """
        # Convert both lists to sets to remove duplicates and allow for efficient intersection
        set1 = set(nums1)
        set2 = set(nums2)
        
        # Find the intersection of both sets
        intersection_set = set1.intersection(set2)
        
        # Convert the set back to a list and return it
        return list(intersection_set)

# Example usage
nums1 = [1, 2, 3, 4, 5]
nums2 = [3, 4, 5, 6, 7]
result = ClassArrayIntersectionWithSet().intersection(nums1, nums2)
print(result)
