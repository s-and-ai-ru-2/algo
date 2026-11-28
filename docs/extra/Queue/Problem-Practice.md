---
id: Practice-Problems-on-queue
title: Queue Practice Problems
sidebar_label: Queue Practice Problems
sidebar_position: 9
Description: Here are some practice problems for queuing data structure divided into topic and width.
tags: [DSA, algorithms, Queue, dsa]
---

### Basic Queue Problems:

- [Implement Queue using Stacks](https://leetcode.com/problems/implement-queue-using-stacks/description)
- [Stack using two Queues](https://www.geeksforgeeks.org/problems/stack-using-two-queues/1)
- [Queue Reversal](https://www.geeksforgeeks.org/problems/queue-reversal/1)
- [Flatten Nested List Iterator](https://leetcode.com/problems/flatten-nested-list-iterator/description/)

#### Worked example — Implement Queue using Stacks

The classic approach uses two stacks (`inbox` and `outbox`).  New items are pushed onto `inbox`; when `outbox` is empty on a dequeue, the entire `inbox` is reversed into `outbox`. This lazy reversal gives **amortised O(1)** dequeue because each element crosses from `inbox` to `outbox` exactly once.

```python
from collections import deque

# ── Method 1: Two-stack queue (amortised O(1) per operation) ─────────────────
class QueueViaStacks:
    def __init__(self):
        self.inbox  = []   # new items land here
        self.outbox = []   # items leave from here (reversed order)

    def enqueue(self, val):
        self.inbox.append(val)          # O(1)

    def dequeue(self):
        if not self.outbox:             # lazy transfer: O(n) amortised O(1)
            while self.inbox:
                self.outbox.append(self.inbox.pop())
        return self.outbox.pop()

    def peek(self):
        if not self.outbox:
            while self.inbox:
                self.outbox.append(self.inbox.pop())
        return self.outbox[-1]

    def empty(self):
        return not self.inbox and not self.outbox


# ── Method 2: Single deque baseline (direct O(1) comparison) ─────────────────
# Uses Python's built-in deque for a direct O(1) append/popleft.
# Intermediate state: a single ordered sequence — no reversal step ever needed.
# The two-stack method trades one extra reversal pass for the ability to use
# only stack (LIFO) primitives, as required by the problem constraint.
class QueueViaDeque:
    def __init__(self):
        self.d = deque()

    def enqueue(self, val):
        self.d.append(val)              # O(1)

    def dequeue(self):
        return self.d.popleft()         # O(1), no reversal needed

    def peek(self):
        return self.d[0]

    def empty(self):
        return len(self.d) == 0


# ── Worked example: enqueue 1, 2, 3 then dequeue all ────────────────────────
print("=== Worked example ===")
for name, q in [("Two-stack", QueueViaStacks()), ("Deque", QueueViaDeque())]:
    q.enqueue(1); q.enqueue(2); q.enqueue(3)
    out = []
    while not q.empty():
        out.append(q.dequeue())
    print(f"{name}: {out}")
# Expected output:
#   Two-stack: [1, 2, 3]
#   Deque: [1, 2, 3]

# ── Boundary example: single element ─────────────────────────────────────────
print("=== Boundary: single element ===")
for name, q in [("Two-stack", QueueViaStacks()), ("Deque", QueueViaDeque())]:
    q.enqueue(42)
    print(f"{name}: {q.dequeue()}")
# Expected output:
#   Two-stack: 42
#   Deque: 42

# ── Boundary example: interleaved enqueue / dequeue ─────────────────────────
print("=== Boundary: interleaved ops ===")
for name, q in [("Two-stack", QueueViaStacks()), ("Deque", QueueViaDeque())]:
    q.enqueue(10); q.enqueue(20)
    a = q.dequeue()
    q.enqueue(30)
    b = q.dequeue()
    c = q.dequeue()
    print(f"{name}: {a}, {b}, {c}")
# Expected output:
#   Two-stack: 10, 20, 30
#   Deque: 10, 20, 30
```

**Comparison of intermediate representations**

| Step | Two-stack (`inbox` / `outbox`) | Single deque |
|------|-------------------------------|--------------|
| After `enqueue(1,2,3)` | inbox=`[1,2,3]`, outbox=`[]` | `[1,2,3]` |
| First `dequeue()` | transfer: inbox=`[]`, outbox=`[3,2,1]`; pop → `1` | popleft → `1` |
| Second `dequeue()` | outbox=`[3,2]`; pop → `2` (no transfer) | popleft → `2` |
| Third `dequeue()` | outbox=`[3]`; pop → `3` | popleft → `3` |

The key difference: the two-stack method pays a one-time O(n) reversal cost the first time `outbox` runs dry, then serves subsequent dequeues in O(1) until `outbox` empties again. The deque baseline never needs a reversal because `popleft` directly accesses the front. Both produce FIFO order; the two-stack approach just achieves it with only LIFO (stack) primitives.

### Circular Queue Problems:

- [Design Circular Queue](https://leetcode.com/problems/design-circular-queue/description/)
- [Design Circular Deque](https://leetcode.com/problems/design-circular-deque/description/)
- [Maximum Sum Circular Subarray](https://leetcode.com/problems/maximum-sum-circular-subarray/description/)

### Priority Queue Problems:

- [K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/description/)
- [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/description/)
- [Path with Maximum Probability](https://leetcode.com/problems/path-with-maximum-probability/description/)
- [Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/description/)
- [Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/description/)

### Deque (Double-Ended Queue) Problems:

- [Deque Implementations](https://www.geeksforgeeks.org/problems/deque-implementations/1)
- [Palindrome Check Using Deque](https://leetcode.com/problems/valid-palindrome/description/)
- [Shortest Subarray with Sum at Least K](https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/description/)
- [Design Front Middle Back Queue](https://leetcode.com/problems/design-front-middle-back-queue/description/)
- [First negative in every window of size k](https://www.geeksforgeeks.org/problems/first-negative-integer-in-every-window-of-size-k3345/1)
- [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/description/)

### Easy

- [Stack using two queues](https://www.geeksforgeeks.org/problems/stack-using-two-queues/1?page=1&category=Queue&sortBy=difficulty)
- [Queue using stack](https://www.geeksforgeeks.org/problems/queue-using-stack/1?page=1&category=Queue&sortBy=difficulty)
- [Reverse First K elements of Queue](https://www.geeksforgeeks.org/problems/reverse-first-k-elements-of-queue/1?page=1&category=Queue&sortBy=difficulty)
- [Generate Binary Numbers](https://www.geeksforgeeks.org/problems/generate-binary-numbers-1587115620/1?page=1&category=Queue&sortBy=difficulty)
- [Minimum Cost of ropes](https://www.geeksforgeeks.org/problems/minimum-cost-of-ropes-1587115620/1?page=1&category=Queue&sortBy=difficulty)

### Medium

- [IPL 2021 - Match Day 2](https://www.geeksforgeeks.org/problems/ipl-2021-match-day-2--141634/1?page=1&category=Queue&sortBy=difficulty)
- [First negative in every window of size k](https://www.geeksforgeeks.org/problems/first-negative-integer-in-every-window-of-size-k3345/1?page=1&category=Queue&sortBy=difficulty)
- [Print Binary Tree levels in sorted order
  ](https://www.geeksforgeeks.org/problems/print-binary-tree-levels-in-sorted-order3241/1?page=2&category=Queue&sortBy=difficulty)
- [Restricted Pacman](https://www.geeksforgeeks.org/problems/restricted-pacman--141631/1?page=2&category=Queue&sortBy=difficulty)
- [Count the Reversals](https://www.geeksforgeeks.org/problems/count-the-reversals0401/1?page=2&category=Queue&sortBy=difficulty)

### Hard

- [LRU Cache](https://www.geeksforgeeks.org/problems/lru-cache/1?page=2&category=Queue&sortBy=difficulty)
- [Steps by Knight](https://www.geeksforgeeks.org/problems/steps-by-knight5927/1?page=2&category=Queue&sortBy=difficulty)
- [Complete Binary Tree](https://www.geeksforgeeks.org/problems/complete-binary-tree/1?page=2&category=Queue&sortBy=difficulty)
- [Card Rotation](https://www.geeksforgeeks.org/problems/card-rotation5834/1?page=2&category=Queue&sortBy=difficulty)
- [Police and Thieves](https://www.geeksforgeeks.org/problems/police-and-thieves--141631/1?page=2&category=Queue&sortBy=difficulty)
