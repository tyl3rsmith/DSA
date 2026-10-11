import random
import time
import matplotlib.pyplot as plt

class SortingAlgorithms:

    # Bubble Sort repeatedly compares adjacent elements and swaps them if they're in the wrong order.
    # Time: O(n^2)
    # Space: O(1)
    @staticmethod
    def bubble_sort(arr):
        n = len(arr)
        shrink = 0

        while True:
            swapped = False

            for i in range(n - 1 - shrink): # the largest element always ends up at the end so shrink sorting window each pass
                if arr[i] > arr[i + 1]: # perform a swap
                    swapped = True
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
        
            if not swapped: # if we perform no swaps it's fully sorted
                break  

            shrink += 1
    

    # Selection Sort finds the smallest element in the unsorted portion of the array
    # and swaps it into the next correct position.
    # Time: O(n^2)
    # Space: O(1)
    @staticmethod
    def selection_sort(arr):
        n = len(arr)

        for pivot in range(n): # select a pivot
            current_min_idx = pivot
            for i in range(pivot + 1, n): # correctly swap the pivot with unsorted portion minimum value
                if arr[i] < arr[current_min_idx]:
                    current_min_idx = i
                
            arr[pivot], arr[current_min_idx] = arr[current_min_idx], arr[pivot]


    # Insertion Sort takes the next element and figures out where it belongs in the previous sorted array
    # Time: O(n^2)
    # Space: O(1)
    @staticmethod
    def insertion_sort(arr):
        n = len(arr)

        for i in range(1, n):
            key = arr[i]

            l = i - 1
            while l >= 0 and arr[l] > key:
                arr[l], arr[l + 1] = arr[l + 1], arr[l]
                l -= 1


    # Merge sort follows three steps:
    # Divide: Split the array into two halves.
    # Conquer: Recursively split each half until every subarray has just one element. A single element is already sorted.
    # Merge: Combine the sorted subarrays in the correct order.
    # Time: O(nlogn) logn levels of splitting merging across each level processes n elements
    # Space: O(n)
    @staticmethod
    def merge_sort(arr):
        n = len(arr)

        # base case: array of size 0 or 1 is already sorted
        if n <= 1:
            return arr

        # divide the array into two halves
        mid = n // 2

        left_half = arr[:mid]
        right_half = arr[mid:]

        left_sorted = SortingAlgorithms.merge_sort(left_half) # conquer: sort the left half
        right_sorted = SortingAlgorithms.merge_sort(right_half) # conquer: sort the right half

        def merge(arr1, arr2):
            i = 0
            j = 0
            res = []

            while i < len(arr1) and j < len(arr2): # 2 ptr merge technique
                if arr1[i] <= arr2[j]:
                    res.append(arr1[i])
                    i += 1
                else:
                    res.append(arr2[j])
                    j += 1
                
            while i < len(arr1):
                res.append(arr1[i])
                i += 1
            
            while j < len(arr2):
                res.append(arr2[j])
                j += 1
            
            return res

        return merge(left_sorted, right_sorted)


    # Quick sort follows three steps:
    # Choose a pivot: Pick an element from the array.
    # Partition: Rearrange elements so that smaller values go to the left of the pivot and larger values go to the right.
    # Recurse: Apply quick sort to the left and right partitions.
    # Time: O(nlogn) average worst O(n^2)
    # Space: O(logn) average worst O(n)
    @staticmethod
    def quick_sort(arr):
        def _quick_sort(arr, low, high):
            if low < high:
                pivot_idx = partition(arr, low, high)

                _quick_sort(arr, low, pivot_idx - 1)
                _quick_sort(arr, pivot_idx + 1, high)

        def partition(arr, low, high):
            # low = the starting index of the portion you're sorting.
            # high = the ending index of the portion you're sorting.

            pivot = arr[high]
            i = low - 1

            for j in range(low, high):
                if arr[j] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
                
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            return i + 1

        n = len(arr)
        _quick_sort(arr, 0, n - 1)
    

    # Heap sort has two main phases:
    # Build a max heap. Rearrange the array so the largest element is at index 0.
    # Repeatedly extract the maximum. Swap the root with the last element in the active heap,
    # shrink the heap by one, and restore the max heap property
    # Time: O(nlogn)
    # Space: O(1)
    @staticmethod
    def heap_sort(arr):
        
        def heapify(arr, n, i):
            while True:
                largest = i

                left = 2 * i + 1
                right = 2 * i + 2

                if left < n and arr[left] > arr[largest]:
                    largest = left

                if right < n and arr[right] > arr[largest]:
                    largest = right

                # The current node is already the largest
                if largest == i:
                    break

                # Move the largest child up
                arr[i], arr[largest] = arr[largest], arr[i]

                # Continue down the tree from the child's position
                i = largest
        
        n = len(arr)

        # Build the max heap
        # last non leaf node is at floor(n/2) - 1
        for i in range((n // 2) - 1, -1, -1):
            heapify(arr, n, i)

        for i in range(n - 1, 0, -1):
            # swap the root with arr[i]
            arr[0], arr[i] = arr[i], arr[0]

            # Fix the heap, excluding the element we just sorted
            heapify(arr, i, 0)


algorithms = {
    "Bubble Sort": SortingAlgorithms.bubble_sort,
    "Selection Sort": SortingAlgorithms.selection_sort,
    "Insertion Sort": SortingAlgorithms.insertion_sort,
    "Merge Sort": SortingAlgorithms.merge_sort,
    "Quick Sort": SortingAlgorithms.quick_sort,
    "Heap Sort": SortingAlgorithms.heap_sort,
}

# Smaller sizes for all six algorithms
input_sizes = [100, 200, 400, 800, 1600, 3200, 6400]
runs = 3

runtimes = {name: [] for name in algorithms}

for n in input_sizes:
    for name, sort_func in algorithms.items():
        total_time = 0

        for _ in range(runs):
            original = [random.randint(0, 100000) for _ in range(n)]
            arr = original.copy()

            start = time.perf_counter()
            sort_func(arr)
            elapsed = time.perf_counter() - start

            total_time += elapsed

        runtimes[name].append(total_time / runs)

plt.figure(figsize=(10, 6))

for name, times in runtimes.items():
    plt.plot(input_sizes, times, marker="o", label=name)

plt.xlabel("Input size (n)")
plt.ylabel("Average runtime (seconds)")
plt.title("All Sorting Algorithms: Smaller Inputs")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Larger sizes for merge, quick, and heap sort
fast_algorithms = {
    name: algorithms[name]
    for name in ["Merge Sort", "Quick Sort", "Heap Sort"]
}

large_input_sizes = [
    100, 500, 1000, 2500, 5000, 10000,
    20000, 50000, 100000
]

fast_runtimes = {name: [] for name in fast_algorithms}

for n in large_input_sizes:
    # Reuse the same randomly generated input for a fair comparison
    original = [random.randint(0, 100000) for _ in range(n)]

    for name, sort_func in fast_algorithms.items():
        total_time = 0

        for _ in range(runs):
            arr = original.copy()

            start = time.perf_counter()
            sort_func(arr)
            elapsed = time.perf_counter() - start

            total_time += elapsed

        fast_runtimes[name].append(total_time / runs)

plt.figure(figsize=(10, 6))

for name, times in fast_runtimes.items():
    plt.plot(large_input_sizes, times, marker="o", label=name)

plt.xlabel("Input size (n)")
plt.ylabel("Average runtime (seconds)")
plt.title("Merge, Quick, and Heap Sort: Larger Inputs")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()