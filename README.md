# HashTable Implementation with Conflict Resolution Strategies

## Overview


The available conflict resolution strategies include:
1. **Linear Probing Strategy O(n)**: Resolves conflicts by sequentially checking the next slots in the hash table. 
2. **Binary Search Tree (BST) Strategy O(log n)**: An unimplemented strategy for resolving conflicts using a binary search tree (left as a placeholder). 

## Usage

The following example demonstrates how to create a hash table with the `LinearProbingStrategy` for conflict resolution and insert key-value pairs.

```python
if __name__ == "__main__":
    linear_strategy = LinearProbingStrategy()
    h = HashTable(5, linear_strategy)
    
    print('Insert 11, 22, 33')
    h[11] = 11
    h[22] = 22
    
