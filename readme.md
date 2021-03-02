It would be nice to denote (somewhere in this repository) which python environment is used during the development of this repository
If you use a conda environment, you can use: 

> conda env export > environment.yml

and add the environment.yml in the repository


# Tactics 

## Target squares


## Cross

```
    +

+   <b>+</b>   +

    +
```

* If two edges are alive, kill the remaining unknown edges. 
* If three edges are known, deduce the remaining unknown edge:
    * If one edge is alive, make the unknown edge.
    * If no edge is alive, kill the unknown edge.

```
+   +   +   +   +   +   +   +   +
                x           x
+   +---+   +---+   +   +   + x +
    |           x           x
+   +   +   +   +   +   +   +   +
```

```
+   +   +   +   +   +   +   +   +
    x           x           x
+ x +---+   +---+---+   + x + x +
    |           x           x
+   +   +   +   +   +   +   +   +
```


## Adjacent squares

### Adjacent squares: 1-1

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

### Adjacent squares: 1-3

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

### Adjacent squares: 3-3

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