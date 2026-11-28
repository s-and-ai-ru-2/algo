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
        // Worked example: {5, 3, 1, 4, 2} -> sorted ascending in 4 passes.
        System.out.println("=== Worked example ===");
        int[] arr = {5, 3, 1, 4, 2};
        oddEvenSort(arr);
        System.out.println("Sorted array:");
        for (int num : arr) {
            System.out.print(num + " ");
        }
        // Expected output: 1 2 3 4 5

        System.out.println();

        // Boundary example: already-sorted array requires only one pass.
        System.out.println("=== Boundary: already sorted ===");
        int[] sorted = {1, 2, 3, 4, 5};
        oddEvenSort(sorted);
        System.out.println("Sorted array:");
        for (int num : sorted) {
            System.out.print(num + " ");
        }
        // Expected output: 1 2 3 4 5

        System.out.println();

        // Boundary example: single element — terminates immediately.
        System.out.println("=== Boundary: single element ===");
        int[] single = {42};
        oddEvenSort(single);
        System.out.println("Sorted array:");
        for (int num : single) {
            System.out.print(num + " ");
        }
        // Expected output: 42

        System.out.println();
    }
}
```

**Invariant explanation**

The key invariant of Odd-Even Sort is:

> After each complete pass (one odd phase followed by one even phase), the largest unsorted element has bubbled into its correct final position at the end of the unsorted portion.

More precisely, after pass `k`, the `k` largest elements occupy the last `k` positions of the array and will never move again. This mirrors bubble sort's invariant but advances two positions per pass by interleaving odd- and even-indexed comparisons in parallel.

**Worked example trace** — input `{5, 3, 1, 4, 2}`:

| Pass | After odd phase | After even phase |
|------|----------------|-----------------|
| 1 | `{5, 1, 3, 2, 4}` | `{1, 5, 2, 3, 4}` |
| 2 | `{1, 2, 5, 3, 4}` | `{1, 2, 3, 5, 4}` |
| 3 | `{1, 2, 3, 4, 5}` | `{1, 2, 3, 4, 5}` |
| 4 | *(no swaps — isSorted stays true)* | *(terminates)* |

After pass 1: `4` and `5` are in their final positions (last two slots).  
After pass 2: `3`, `4`, `5` are settled.  
After pass 3: the array is fully sorted; pass 4 confirms it and exits.

**Boundary example traces**

- `{1, 2, 3, 4, 5}` — already sorted: the odd and even phases make no swaps, `isSorted` stays `true`, and the loop exits after a single pass.
- `{42}` — single element: both phases find no adjacent pair to compare, so `isSorted` stays `true` and the loop exits after one pass.

### Summary:
Odd-Even Sort is a straightforward sorting algorithm that alternates between odd and even phases to sort an array. While it can be implemented efficiently in parallel computing environments, its average and worst-case time complexities of O(n2) make it less efficient compared to more advanced algorithms like Quick Sort or Merge Sort.
