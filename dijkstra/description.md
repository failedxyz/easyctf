This is a high-level programming challenge. Given a set of vertices corresponding to the map below, your program must output the shortest path from `a` to `z`.

![image](`{dijkstra_map_svg}`)

The length of the line segments is randomized such that the length (`l`) satisfies `20 <= l <= 120`.

Input will consist of 49 lines in the format `vertex1 vertex2 distanceBetween`

Here are a few lines of example input:
```shell
h i 94
h o 40
i l 95
l k 65
l t 63
t u 47
```

The output should be written to a file named "dijkstra.out" in the current directory. Output will consist of the entire path, with `->` in between vertices. Print the current distance traveled in parenthesis after each vertex, as shown below.
```
a -> b(113) -> c(210) -> f(262) -> h(291) -> i(326) -> m(381) -> s(409) -> x(444) -> y(534) -> z(557)
```