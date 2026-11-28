---
id: cocktail-shaker-sort-algo  
sidebar_position: 18  
title: Cocktail Shaker Sort  
sidebar_label: Cocktail Shaker Sort
description: "Complete guide to Cocktail Shaker Sort, a bidirectional bubble sort variant that traverses the array in both directions."
tags: [sorting algorithms, cocktail shaker sort, bubble sort, dsa]

---

### Definition:

Cocktail Shaker Sort, also known as Bidirectional Bubble Sort, is a variation of the Bubble Sort algorithm that sorts an array in both directions. It traverses the array back and forth, moving larger elements towards the end and smaller elements towards the beginning, making it more efficient than standard Bubble Sort in some cases.

### Video Explanation

<LiteYouTubeEmbed
  id="Xmx_6YRBaq8"
  params="autoplay=1&autohide=1&showinfo=0&rel=0"
  title="Sorting Algorithms Redux 04: Cocktail Sort"
  poster="maxresdefault"
  lazyLoad={true}
  webp
/>

### Characteristics:

- **Bidirectional**:  
  Unlike traditional sorting algorithms that only iterate in one direction, Cocktail Shaker Sort moves in both directions, which can help to reduce the total number of passes required.

- **In-Place**:  
  The algorithm sorts the array without using any additional storage, modifying the input array directly.

- **Stable**:  
  Cocktail Shaker Sort maintains the relative order of equal elements, making it a stable sorting algorithm.

### Time Complexity:

- **Best Case: O(n)**  
  When the array is already sorted, the algorithm makes a single pass.

- **Average Case: O(n²)**  
  In most scenarios, the algorithm's performance resembles that of Bubble Sort.

- **Worst Case: O(n²)**  
  Similar to Bubble Sort, the worst-case scenario occurs with a reversed array.

### Space Complexity:

- **Space Complexity: O(1)**  
  The algorithm operates in constant space since it only requires a few variables for swapping and indexing.

### Java Implementation:

```java
public class CocktailShakerSort {

    // Method to perform Cocktail Shaker Sort
    public static void cocktailShakerSort(int[] arr) {
        boolean swapped = true;
        int start = 0;
        int end = arr.length - 1;

        while (swapped) {
            swapped = false;

            // Forward pass
            for (int i = start; i < end; i++) {
                if (arr[i] > arr[i + 1]) {
                    swap(arr, i, i + 1);
                    swapped = true;
                }
            }

            // If nothing moved, the array is sorted
            if (!swapped) break;

            swapped = false;
            end--;

            // Backward pass
            for (int i = end; i > start; i--) {
                if (arr[i] < arr[i - 1]) {
                    swap(arr, i, i - 1);
                    swapped = true;
                }
            }

            start++;
        }
    }

    // Helper method to swap two elements
    private static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }

    public static void main(String[] args) {
        // Worked example: {5, 3, 1, 4, 2} sorted by bidirectional passes.
        System.out.println("=== Worked example ===");
        int[] arr = {5, 3, 1, 4, 2};
        cocktailShakerSort(arr);
        System.out.println("Sorted array:");
        for (int num : arr) {
            System.out.print(num + " ");
        }
        // Expected output: 1 2 3 4 5

        System.out.println();

        // Boundary: single element.
        // Precondition: start == end (both 0), so the forward loop range(0,0)
        // is empty, swapped stays false, and the while-loop breaks immediately
        // after one partial pass — no comparisons or swaps occur.
        System.out.println("=== Boundary: single element ===");
        int[] single = {42};
        cocktailShakerSort(single);
        System.out.println("Sorted array:");
        for (int num : single) {
            System.out.print(num + " ");
        }
        // Expected output: 42

        System.out.println();

        // Boundary: already-sorted array.
        // Precondition: no pair satisfies arr[i] > arr[i+1], so the forward
        // pass sets no swap, swapped stays false, and the guard "if (!swapped) break"
        // terminates the loop after a single forward scan — the backward pass
        // is never reached.
        System.out.println("=== Boundary: already sorted ===");
        int[] sorted = {1, 2, 3, 4, 5};
        cocktailShakerSort(sorted);
        System.out.println("Sorted array:");
        for (int num : sorted) {
            System.out.print(num + " ");
        }
        // Expected output: 1 2 3 4 5

        System.out.println();
    }
}
```

**Boundary explanation**

The precondition that decides how early the algorithm exits is the value of `swapped` after each directional pass:

- **Single element** (`arr = {42}`): `start = 0`, `end = 0`. The forward loop runs `for (i = 0; i < 0; ...)` — zero iterations — so `swapped` is never set to `true`. The guard `if (!swapped) break` fires and the method returns without touching the array.

- **Already-sorted array** (`arr = {1, 2, 3, 4, 5}`): The forward pass scans all adjacent pairs and finds no inversion, leaving `swapped = false`. The guard breaks the outer loop before the backward pass even starts. This is the best-case O(n) behaviour documented in the time complexity section.

- **General unsorted array** (`arr = {5, 3, 1, 4, 2}`): At least one swap occurs in the forward pass, so `swapped = true` and the guard does not fire. After the forward pass, `end` shrinks by 1 (the largest unsorted element has bubbled to its final position) and the backward pass runs, moving the smallest unsorted element left. `start` then grows by 1. This shrinking window is what gives Cocktail Shaker Sort its advantage over plain Bubble Sort for arrays with small elements near the end.

### Summary:
Cocktail Shaker Sort improves upon the standard Bubble Sort by processing the array in both directions, potentially reducing the number of iterations needed. Its bidirectional approach provides a simple yet effective alternative for sorting, though it still maintains a quadratic time complexity in average and worst-case scenarios, making it less efficient than more advanced algorithms like Quick Sort or Merge Sort.
