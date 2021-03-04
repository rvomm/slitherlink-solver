It would be nice to denote (somewhere in this repository) which python environment is used during the development of this repository
If you use a conda environment, you can use: 

> conda env export > environment.yml

and add the environment.yml in the repository


# Tactics 

## Target squares

* If **N** edges are alive, kill the remaining unknown edges.
* If **N-M** edges are alive and only **M** edges remain unknown, make remaining unknown edges.

Completing a square by killing remaining edges: 

```
+   +   +---+   +---+   +---+
  0       1       2 |     3 |
+   +   +   +   +   +   +---+
```

**Solution:**
``` 
+ x +   +---+   +---+   +---+
x 0 x   x 1 x   x 2 |   x 3 |
+ x +   + x +   + x +   +---+
```

Completing a square by making remaining edges:

``` 
+ x +   +   +   +   +   +   +
x 0 x   x 1 x   x 2     x 3  
+ x +   + x +   + x +   +   +
```

**Solution:**
``` 
+ x +   +---+   +---+   +---+
x 0 x   x 1 x   x 2 |   x 3 |
+ x +   + x +   + x +   +---+
```

## Cross

```
    +

+   +   +

    +
```

* If two edges are alive, kill the remaining unknown edges. 

```
    +

+   +---+
    |
    +
```

**Solution:**
```
    +
    x
+ x +---+
    |
    +
```

* If three edges are known, complete the remaining unknown edge:
    * If one edge is alive, make the unknown edge alive.
    * If no edge is alive, kill the unknown edge.


```
    +               +
    |               x
+ x +   +   +   + x +   +
    x               x
    +               +
```

**Solution:**
```
    +               +
    |               x
+ x +---+   +   + x + x +
    x               x
    +               +
```

## Adjacent squares

### Adjacent squares: 1 - 1

Adjacent 1-1 squares are 1-squares either horizontally or vertically adjacent. 
A single edge between the squares can be killed when an incoming edge in the 
middle of the squares is dead.

```
+   +   +   +   +
        x
+   +   +   +   + 
      1   1
+   +   +   +   + 

+   +   +   +   + 
```

**Solution:**
```
+   +   +   +   +
        x
+   +   +   +   + 
      1 x 1
+   +   +   +   + 

+   +   +   +   + 
```

### Adjacent squares: 1 - 3

Adjacent 1-3 squares is composed of a 1-square, horizontally or vertically adjacent to a 
3-square. A single edge of the 3-square can be made when an incoming edge in the middle 
of the squares is dead.

```
+   +   +   +   +
        x
+   +   +   +   + 
      1   3
+   +   +   +   + 

+   +   +   +   + 
```

**Solution:**
```
+   +   +   +   +
        x
+   +   +---+   + 
      1   3
+   +   +   +   + 

+   +   +   +   + 
```

### Adjacent squares: 3 - 3

Adjacent 3-3 squares can be solved without knowing anything about the surrounding
edges.

```
+   +   +   +   +
        
+   +   +   +   + 
      3   3
+   +   +   +   + 

+   +   +   +   + 
```

**Solution:**
```
+   +   +   +   +
        x
+   +   +   +   + 
    | 3 | 3 |
+   +   +   +   + 
        x
+   +   +   +   + 
```

## Cross + square

A `cross + square` contains the union of the edges of a square with target and 
a neighbouring cross.  There are different tactics depending on the target 
value.

```
+   +   +   +
    |
+---+---+   +
    | . |
+   +---+   +

+   +   +   +
```
### Cross + square: 1

When both incoming edges (cross edges not part of the square) are known, when can 
solve part of the square edges. There are two different cases. Note that the third 
case, where both edges are alive, is already dealt with by the cross structure. 

```
+   +   +   +   +   +   +   +
    x               x
+---+   +   +   + x +   +   +
      1               1
+   +   +   +   +   +   +   +

+   +   +   +   +   +   +   +
```

**Solution:**
```
+   +   +   +   +   +   +   +
    x               x
+---+   +   +   + x + x +   +
      1 x           x 1
+   + x +   +   +   +   +   +

+   +   +   +   +   +   +   +
```

### Cross + square: 2

### Cross + square: 3

If there is a single incoming edge

```
+   +   +   +   +   +   +   +
                    
+---+   +   +   + x +   +   +
      3               3 |
+   +   +   +   +   +---+   +

+   +   +   +   +   +   +   +
```

**Solution:**
```
+   +   +   +   +   +   +   +
    x               |
+---+   +   +   + x +   +   +
      3 |             3 |
+   +---+   +   +   +---+   +

+   +   +   +   +   +   +   +
```


## Square + Diagonal crosses

For 2-squares, we need to consider pairs of crosses diagonally opposing
from the square. For every square there are two different tactics, formed
by the two pairs of diagonally opposing crosses.

```
+   +   +   +
        |  
+   +---+---+ 
    | . |
+---+---+   + 
    |   
+   +   +   + 
```

### Square + Diagonal crosses: 2-square

When both crosses have an incoming edge alive, the other incoming edges 
must be killed. 

```
+   +   +   +
           
+   +   +---+ 
      2
+   +   +   + 
    |   
+   +   +   + 
```

**Solution:**
```
+   +   +   +
        x  
+   +   +---+ 
      2
+ x +   +   + 
    |   
+   +   +   + 
```

### Square + Diagonal crosses: 2-square (uniqueness)

There is a special case of the Square + Diagonal crosses, arising when the 
2-square is not adjcacent (horizontally or vertically) by any other target
square. Here we can use the uniqueness of the solution to add another 
solving strategy.

If a cross has zero outgoing edges (both are dead edges), there are only
two solutions for the 2-square. The opposite cross (cross2) then either 
has zero or two edges alive. 

```
+   +   +   +
           
+   +   +   + 
      2
+ x +   +   + 
    x   
+   +   +   + 
```

To solve we reason by contradiction:
    
Suppose the opposite cross has zero incoming edges alive. Then the 
solution of the square is not restricted by the two opposing crosses. 
But there are also no constraints implied by any adjacent squares 
(because there are none!). This means that the square must have two 
solutions! One solution has a path along two edges of the first cross, 
the other solution has a path along the edges of second cross. 
This contradicts the uniqueness of the solution.

**Proposition:**
```
+   +   +   +
        x  
+   +   + x + 
      2
+ x +   +   + 
    x   
+   +   +   + 
```

**Solution 1:**
```
+   +   +   +
        x  
+   +   + x + 
    | 2
+ x +---+   + 
    x   
+   +   +   + 
```

**Solution 2:**
```
+   +   +   +
        x  
+   +---+ x + 
      2 |
+ x +   +   + 
    x   
+   +   +   + 
```

Hence, the incoming edges of the opposite cross must be be alive. The 
solution of the rest of the 2-square is dealt with by the relevant 
CrossSquare object.

**Solution:**
```
+   +   +   +
        |  
+   +   +---+ 
      2
+ x +   +   + 
    x   
+   +   +   + 
```

## Edge-pairs

### Opposite edge pairs

An opposite edge-pair is a set of two edges, where one edge must be alive and the 
other must be dead. If both edges belong the the same cross, the opposite edge pair
property is carried over the the remaining two edges of the cross. 

In the example below the remaining edges of the 3-square for an opposite edge pair.
The cross between the 3-square and 1-square carries over the opposite edge pair
property the the squares within the 1-square. As either one of these edges must 
be alive, all remaining edges of the 1-square can be killed.

**Example:**
```
+---+   +   +   +
| 3
+   +   +   +   +
      1
+   +   +   +   +
        
+   +   +   +   +
```

**Solution:**
```
+---+   +   +   +
| 3
+   +   +   +   +
      1 x
+   + x +   +   +
        
+   +   +   +   +
```

The other way around works similarly.


**Example:**
```
+ x +   +   +
x 1
+   +   +   +
      3 
+   +   +   +
        
+   +   +   +
```

**Solution:**
```
+ x +   +   +
x 1
+   +   +   +
      3 |
+   +---+   +
        
+   +   +   +
```

A 2-square can also carry over the opposite edge pair property. In the example
below, every two square has two opposite edge pairs (up, left) and (down, right).
Information is carried over across crosses and diagonal 2-squares until the 
information is *absorbed*, in this case by a 1-square.

**Example:**
```
+---+   +   +   +   +
| 3
+   +   +   +   +   +
      2  
+   +   +   +   +   +
          2  
+   +   +   +   +   +
              1
+   +   +   +   +   +

+   +   +   +   +   +
```

**Solution:**
```
+---+   +   +   +   +
| 3
+   +   +   +   +   +
      2  
+   +   +   +   +   +
          2  
+   +   +   +   +   +
              1 x
+   +   +   + x +   +

+   +   +   +   +   +
```

### Common edge pairs

A common edge pair is a set of two edges that must be either both alive or 
both dead. In the example below, the cross top-left of the 2-square TBD

**Example:**
```
+   +   +   +   +
    x
+ x +   +   +   +
      2 
+   +   +   +   +
      2   3
+   +   +   +   +

+   +   +   +   +
```

**Solution:**
```
+   +   +   +   +
    x
+ x +   +   +   +
      2 x
+   + x +   +   +
      2   3
+   +   +   +   +

+   +   +   +   +
```


















