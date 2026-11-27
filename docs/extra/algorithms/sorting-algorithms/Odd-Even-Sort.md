---
id: odd-even-sort-algo  
sidebar_position: 19  
title: Odd-Even Sort  
sidebar_label: Odd-Even Sort
description: "Complete guide to Odd-Even Sort, a parallel sorting algorithm that alternates between odd and even phases to gradually sort the array."
tags: [sorting algorithms, odd even sort, parallel sorting, dsa]

---

### Definition:

Odd-Even Sort is a simple parallel sorting algorithm that works by repeatedly performing two phases: an odd phase and an even phase. It compares and swaps adjacent elements in two passes, which gradually sorts the array. It is mainly used in parallel computing environments due to its ability to be implemented efficiently across multiple processors.

### Video Explanation

<LiteYouTubeEmbed
  id="Sazh4Y-WlDk"
  params="autoplay=1&autohide=1&showinfo=0&rel=0"
  title="Odd Even Transposition Parallel Formulation || Bubble Sort and it's Variants || Explained in Hindi"
  poster="maxresdefault"
  lazyLoad={true}
  webp
/>

### Characteristics:

- **Two Phases**:  
  The algorithm alternates between an odd phase (comparing elements at odd indexes with their next even index) and an even phase (comparing elements at even indexes with their next odd index).

- **In-Place**:  
  The algorithm sorts the array without requiring any additional storage, modifying the input array directly.

- **Not Stable**:  
  Odd-Even Sort is not stable, meaning that the relative order of equal elements may not be preserved.

### Time Complexity:

- **Best Case: O(n)**  
  When the array is already sorted, the algorithm only requires one pass.

- **Average Case: O(n²)**  
The average time complexity is quadratic, similar to other simple sorting algorithms.

- **Worst Case: O(n²)**  
The worst-case scenario occurs when the array is in reverse order.

### Space Complexity:

- **Space Complexity: O(1)**  
The algorithm operates in constant space, only using a few variables for swapping.

### Loop Invariant:

The key invariant of Odd-Even Sort is:

> **After k complete passes (one odd phase + one even phase), the last k elements of the array are in their final sorted positions.**

**Why this holds:**
- Each odd-even pair of phases acts like one bidirectional bubble-sweep. During the odd phase, odd-indexed elements are compared with their right neighbors; during the even phase, even-indexed elements are compared with their right neighbors.
- Together, these phases ensure that the largest unsorted element "bubbles" toward the right end of the array at least one position per complete pass.
- Once an element reaches its correct final position at the right end, subsequent passes never move it leftward (comparisons only swap when `arr[i] > arr[i+1]`, so a correctly-placed large element is never swapped left).
- When k = n-1 complete passes have occurred, all n-1 largest elements are in place, and the remaining first element is trivially correct — the array is fully sorted.

This invariant guarantees termination: after at most n-1 passes, no swaps occur and `isSorted` remains `true`, exiting the loop.

### Java Implementation:

```java
public class OddEvenSort {

    // Method to perform Odd-Even Sort
    public static void oddEvenSort(int[] arr) {
        boolean isSorted = false;
        int n = arr.length;

        while (!isSorted) {
            isSorted = true;

            // Odd phase
            for (int i = 1; i < n - 1; i += 2) {
                if (arr[i] > arr[i + 1]) {
                    swap(arr, i, i + 1);
                    isSorted = false;
                }
            }

            // Even phase
            for (int i = 0; i < n - 1; i += 2) {
                if (arr[i] > arr[i + 1]) {
                    swap(arr, i, i + 1);
                    isSorted = false;
                }
            }
        }
    }

    // Helper method to swap two elements
    private static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }

    public static void main(String[] args) {
        int[] arr = {5, 3, 1, 4, 2};
        oddEvenSort(arr);
        System.out.println("Sorted array:");
        for (int num : arr) {
            System.out.print(num + " ");
        }
    }
}
```

### Summary:
Odd-Even Sort is a straightforward sorting algorithm that alternates between odd and even phases to sort an array. While it can be implemented efficiently in parallel computing environments, its average and worst-case time complexities of O(n2) make it less efficient compared to more advanced algorithms like Quick Sort or Merge Sort.
