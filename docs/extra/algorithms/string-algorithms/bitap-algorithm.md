---

id: bitap-algo  
sidebar_position: 3  
title: Bitap Algorithm  
sidebar_label: Bitap Algorithm  

---

### Definition:

The Bitap algorithm, also known as the **Shift-Or**, **Shift-And**, or **Bitap for Approximate String Matching**, is a string matching algorithm that efficiently finds patterns in a text with possible mismatches or errors. The algorithm leverages bitwise operations to perform both exact and approximate string matching, making it ideal for fuzzy searching.

### Video Explanation

<LiteYouTubeEmbed
  id="jXNj27TMQRU"
  params="autoplay=1&autohide=1&showinfo=0&rel=0"
  title="Bitap algorithm for fuzzy matching explained with example"
  poster="maxresdefault"
  lazyLoad={true}
  webp
/>

### Characteristics:

- **Bitwise Matching**:
  - The Bitap algorithm uses bitwise operations to compare the pattern against the text. Each bit represents whether a character in the text matches a position in the pattern.

- **Approximate Matching**:
  - It supports approximate matching, where the pattern may have a certain number of mismatches, insertions, or deletions. This is especially useful in fields like text retrieval or DNA sequence matching.

- **Pattern Masking**:
  - The pattern is preprocessed into bitmasks, which are then used during the text scan to track how much of the pattern has been matched, including the handling of allowed errors.

- **Linear Search with Errors**:
  - The algorithm scans the text linearly, and the number of allowed errors (insertions, deletions, substitutions) is parameterized, allowing for flexible search criteria.

### Time Complexity:

- **Best Case: $O\left(\frac{n}{w}\right)$**  
  The best-case complexity is linear, as the algorithm processes `w` characters in parallel per word size `w` of the machine.

- **Average Case: $O(n)$**  
  On average, the algorithm performs in linear time with respect to the text size `n`, especially for small patterns or when only a few errors are allowed.

- **Worst Case: $O(n \times m)$**  
  In the worst case, if the pattern is large or if there are many errors allowed, the time complexity can degrade to quadratic, where `m` is the pattern length.

### Space Complexity:

- **Space Complexity: $O(m)$**  
  The algorithm requires space proportional to the pattern length `m` for storing bitmasks, making it efficient in terms of memory usage.

### C++ Implementation:

**Approximate Matching with `k` Allowed Errors**
```cpp
#include <iostream>
#include <vector>
#include <string>
using namespace std;

#define CHAR_SIZE 256 // Extended ASCII

void preprocessPattern(const string& pattern, vector<int>& patternMask) {
    int m = pattern.size();
    for (int i = 0; i < CHAR_SIZE; ++i) {
        patternMask[i] = ~0;
    }
    for (int i = 0; i < m; ++i) {
        patternMask[pattern[i]] &= ~(1 << i);
    }
}

void bitapSearch(const string& text, const string& pattern, int maxErrors) {
    int n = text.size();
    int m = pattern.size();

    if (m > n) return;

    vector<int> patternMask(CHAR_SIZE);
    preprocessPattern(pattern, patternMask);

    vector<int> R(maxErrors + 1, ~0);
    for (int i = 0; i <= maxErrors; ++i) {
        R[i] = ~1; // All bits set except the least significant bit
    }

    for (int i = 0; i < n; ++i) {
        int oldR_jMinus1 = ~0;
        for (int j = 0; j <= maxErrors; ++j) {
            int temp = R[j];
            R[j] = ((R[j] << 1) | patternMask[text[i]]);
            if (j > 0) {
                R[j] &= (oldR_jMinus1 << 1) | (R[j - 1] << 1) | oldR_jMinus1;
            }
            oldR_jMinus1 = temp;
        }
        if ((R[maxErrors] & (1 << (m - 1))) == 0) {
            cout << "Pattern found at index " << i - m + 1 << " with " << maxErrors << " allowed errors." << endl;
        }
    }
}

int main() {
    // Worked example: pattern sits at index 17 in the text.
    // With maxErrors = 1 the search still finds it (zero substitutions needed).
    string text = "this is a simple example";
    string pattern = "example";
    int maxErrors = 1; // Allow 1 error (insertion, deletion, or substitution)

    cout << "=== Worked example (1 error allowed) ===" << endl;
    bitapSearch(text, pattern, maxErrors);
    // Expected output:
    //   Pattern found at index 17 with 1 allowed errors.

    // Boundary example: exact match only, 0 errors allowed.
    // "ell" appears at index 1 inside "hello".
    cout << "=== Boundary example (0 errors, exact match) ===" << endl;
    bitapSearch("hello", "ell", 0);
    // Expected output:
    //   Pattern found at index 1 with 0 allowed errors.

    // Boundary example: pattern absent, no output expected.
    cout << "=== Boundary example (0 errors, no match) ===" << endl;
    bitapSearch("hello", "xyz", 0);
    // Expected output: (none)

    return 0;
}
```

**Worked example trace**

For `text = "this is a simple example"` and `pattern = "example"` (length 7):

- `preprocessPattern` builds a bitmask for each character.  For character `'e'`, bit 0 is cleared (position 0 in pattern); for `'x'`, bit 1 is cleared; and so on.
- During the scan, `R[j]` tracks how many characters of the pattern have been matched with at most `j` errors.  A match is signalled when bit `m-1` (bit 6 for a 7-character pattern) of `R[maxErrors]` is 0.
- At text position `i = 23` (last character `'e'` of `"example"`), `R[1]` satisfies `(R[1] & (1 << 6)) == 0`, so the match is reported starting at index `23 - 7 + 1 = 17`.

**Boundary example trace**

For `text = "hello"` and `pattern = "ell"` with `maxErrors = 0`:

- An exact match is required (no errors).
- At `i = 3` (character `'l'`, end of `"ell"`), the check passes and the match is reported at index `3 - 3 + 1 = 1`.
- For `pattern = "xyz"` there is no position where three consecutive characters match, so nothing is printed.

### Summary:

The Bitap algorithm is a highly efficient string matching technique that supports approximate matching, making it ideal for applications requiring fuzzy search capabilities. Its use of bitwise operations allows for fast text scanning, while its flexibility in handling errors sets it apart from other exact matching algorithms. Despite its quadratic worst-case complexity, it performs well for small patterns and a limited number of errors.