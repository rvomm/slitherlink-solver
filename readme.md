It would be nice to denote (somewhere in this repository) which python environment is used during the development of this repository
If you use a conda environment, you can use: 

> conda env export > environment.yml

and add the environment.yml in the repository


# Tactics 

## Target squares

* If **N** edges are alive, kill the remaining unknown edges.
* If **N-M** edges are alive and only **M** edges are still unknown, make remaining unknown edges.

Completing a square by killing remaining edges: 

```
+   +   +---+   +---+   +---+
  0       1       2 |     3 |
+   +   +   +   +   +   +---+
```

``` 
+ x +   +---+   +---+   +---+
x 0 x   x 1 x   x 2 |   x 3 |
+ x +   + x +   + x +   +---+
```

Completing a square by making the remaining:

``` 
+ x +   +   +   +   +   +   +
x 0 x   x 1 x   x 2     x 3  
+ x +   + x +   + x +   +   +
```

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
* If three edges are known, deduce the remaining unknown edge:
    * If one edge is alive, make the unknown edge.
    * If no edge is alive, kill the unknown edge.

<pre>
+   +   +   +   +   +   +   +   +
                x           x
+   <b>+</b>---+   +   <b>+</b>---+   + x <b>+</b>   +
    |           x           x
+   +   +   +   +   +   +   +   +
</pre>

<pre>
+   +   +   +   +   +   +   +   +
    x           x           x
+ x <b>+</b>---+   +---<b>+</b>---+   + x <b>+</b> x +
    |           x           x
+   +   +   +   +   +   +   +   +
</pre>

## Adjacent squares

### Adjacent squares: 1 - 1

```
+   +   +   +   +
        x
+   +   +   +   + 
      1   1
+   +   +   +   + 

+   +   +   +   + 
```

```
+   +   +   +   +
        x
+   +   +   +   + 
      1 x 1
+   +   +   +   + 

+   +   +   +   + 
```

### Adjacent squares: 1 - 3

```
+   +   +   +   +
        x
+   +   +   +   + 
      1   3
+   +   +   +   + 

+   +   +   +   + 
```

```
+   +   +   +   +
        x
+   +   +---+   + 
      1   3
+   +   +   +   + 

+   +   +   +   + 
```

### Adjacent squares: 3 - 3

```
+   +   +   +   +
        
+   +   +   +   + 
      3   3
+   +   +   +   + 

+   +   +   +   + 
```

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
a neighbouring cross.  

```
+   +   +   +
    |
+---+---+   +
    | . |
+   +---+   +

+   +   +   +
```
### Cross + square: 1

```
+   +   +   +   +   +   +   +
    x               x
+---+   +   +   + x +   +   +
      1               1
+   +   +   +   +   +   +   +

+   +   +   +   +   +   +   +
```


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

```
+   +   +   +   +   +   +   +
                    
+---+   +   +   + x +   +   +
      3               3 |
+   +   +   +   +   +---+   +

+   +   +   +   +   +   +   +
```


```
+   +   +   +   +   +   +   +
    x               |
+---+   +   +   + x +   +   +
      3 |           x 3 |
+   +---+   +   +   +---+   +

+   +   +   +   +   +   +   +
```


