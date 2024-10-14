#import "template.typ": *
#import "@preview/tablex:0.0.8": tablex, hlinex, vlinex, colspanx, rowspanx
#import "@preview/colorful-boxes:1.3.1": outline-colorbox
#import "@preview/gentle-clues:1.0.0": *

#set math.equation(numbering: "(1)")

#show: project.with(
  title: "Práctica 2",
  subtitle: [
    Algoritmos de Búsqueda Informada
  ],
  author: (
    "Pablo Hernández Jiménez",
  ),
  affiliation: "Universidad de La Laguna",
  date: datetime.today().display(),
  Licence: "Curso 2024-2025",
  UE: "Inteligencia Artificial",
  logo: "images/ull-logo.png",
  main_color: "#5c068c",
  toc_title: "Índice",
)

= Introducción

#notify(title: "Importante")[
  Para una mejor comprensión de la práctica, 
  se recomienda la lectura de la #link("https://hadronomy.github.io/PR1y2-IA-2425/")[documentación del proyecto]
  donde se explica en detalle la implementación y el diseño de la práctica.

  Además, en la documentación se encuentran las instrucciones de 
  #link("https://hadronomy.github.io/PR1y2-IA-2425/installation.html")[instalación y ejecución del programa].
]

En esta práctica se implementa el algoritmo de búsqueda $A*$ 
y se aplica a un problema de búsqueda de caminos en un laberinto.

Destacar que para el desarrollo de la práctica se ha utilizado el lenguaje de programación Python#footnote[
  #link("https://www.python.org/"): Python es un lenguaje de programación interpretado cuya filosofía hace hincapié en una sintaxis que favorezca un código legible.
]. Por tanto y al no ser un lenguaje de programación
compilado se darán
#link("https://hadronomy.github.io/PR1y2-IA-2425/installation.html")[instrucciones para su correcta instalación y ejecución.]

Se explicará la implementación del algoritmo y se mostrarán los resultados obtenidos,
comparando diferentes heurísticas y sus resultados.


#pagebreak()

= Diseño e Implementación

Dejando de para más adelante la explicación de la implementación de la *CLI*#footnote[
  #link("https://es.wikipedia.org/wiki/Interfaz_de_l%C3%ADnea_de_%C3%B3rdenes"): Interfaz de línea de órdenes o *CLI* (del inglés *Command Line Interface*) es un método que permite a los usuarios interactuar con algún programa informático por medio de líneas de texto.
]<cli>.
Empezemos con la estructura de ficheros y la *implementación de las 
clases* y/o *estructuras de datos* necesarias para el correcto funcionamiento
del programa y el algoritmo de búsqueda.

=== Estructura de Ficheros

La estructura de ficheros es la siguiente:

#figure(
  tablex(
    columns: (auto, auto),
    align: (left),
    [
      ```plaintext
      .
      ├── CHANGELOG.md
      ├── cliff.toml
      ├── ia
      │  ├── __init__.py
      │  ├── __main__.py
      │  ├── algorithm.py
      │  ├── cli
      │  │  ├── __init__.py
      │  │  ├── cmd.py
      │  │  ├── informed.py
      │  │  ├── uninformed.py
      │  │  └── utils.py
      │  ├── graph
      │  │  ├── __init__.py
      │  │  ├── parser
      │  │  └── undirected.py
      │  ├── main.py
      │  ├── maze
      │  │  ├── __init__.py
      │  │  ├── constants.py
      │  │  ├── euristics.py
      ```
    ],
    [
      ```plaintext
      │  │  ├── matrix.py
      │  │  ├── maze.py
      │  │  ├── parser.py
      │  │  ├── tile.py
      │  │  └── utils.py
      │  └── tree
      │     ├── __init__.py
      │     ├── basenode.py
      │     ├── constants.py
      │     ├── iterators.py
      │     ├── node.py
      │     └── utils.py
      ├── LICENSE
      ├── poetry.lock
      ├── pyproject.toml
      └── README.md
      ```
    ]
  ),
  caption: "Estructura de ficheros del proyecto"
) <project-structure>

Como se muestra en *@project-structure*, el proyecto está estructurado
siguiendo las *buenas prácticas de programación en Python*. 

Destacar que el proyecto contiene tanto el código de la *Práctica 1*
como el de la *Práctica 2*. Esto es debido a que comparten estructuras
de datos y funciones que son necesarias para el correcto funcionamiento
de la *Práctica 2*. Y gracias a la modularidad del diseño, se pueden
reutilizar estas estructuras y funciones sin tener que duplicar código.

En el *CLI*@cli la ejecución de ambas prácticas se encuentra
diferenciada en subcomandos.

- ia *uninformed*: Ejecuta la *Práctica 1*.
- ia *informed*: Ejecuta la *Práctica 2*.

#pagebreak()

=== Implementación

#notify(title: "Importante")[
  Para una mejor comprensión de la implementación *se recomienda
  la lectura* de la #link("https://hadronomy.github.io/PR1y2-IA-2425/")[documentación del proyecto]. 
  Puesto que en esta sección debido a la extensión del código 
  no se pueden explicar todos los detalles y se explicarán de forma
  muy simplifica.

  #linebreak()
  El código fuente se encuentra en el repositorio de
  #link("https://github.com/hadronomy/PR1y2-IA-2425")[GitHub].
]

Para el diseño e implementación de la práctica, se ha seguido un enfoque basado en la 
modularidad y los principios *SOLID*. La modularidad permite dividir el sistema en 
partes más pequeñas y manejables, facilitando el mantenimiento y la escalabilidad del código. 
Cada módulo se encarga de una funcionalidad específica, lo que reduce la complejidad y mejora la reutilización del código.

Los principios *SOLID*, que son cinco principios de diseño orientado a objetos, se han aplicado para asegurar que el código sea robusto y fácil de mantener:

1. *Single Responsibility Principle (SRP)*: Cada clase o módulo tiene una única responsabilidad
  o motivo para cambiar, lo que simplifica el desarrollo y el mantenimiento.
2. *Open/Closed Principle (OCP)*: Las clases y módulos están abiertos para extensión 
  pero cerrados para modificación, permitiendo agregar nuevas funcionalidades sin alterar el código existente.
3. *Liskov Substitution Principle (LSP)*: Las clases derivadas deben ser sustituibles
  por sus clases base sin alterar el comportamiento del programa, asegurando la correcta implementación de la herencia.
4. *Interface Segregation Principle (ISP)*: Se prefieren interfaces específicas y pequeñas 
  en lugar de interfaces generales y grandes, lo que reduce la dependencia entre módulos.
5. *Dependency Inversion Principle (DIP)*: Los módulos de alto nivel no deben 
  depender de módulos de bajo nivel, sino de abstracciones, promoviendo un diseño desacoplado y flexible.

Gracias a estos principios, el diseño de la práctica es más claro, mantenible y escalable, permitiendo que el código sea más fácil de entender y modificar.

#pagebreak()

==== MazeTile

Clase enum que contiene los posibles valores de una celda
de un laberinto. Los valores posibles son los siguientes:

*MazeTile* asocia los diferentes tipos de celda a una
cade para su fácil reconociento. También existe una constante
`DEFAULT_MAZE_MAPPINGS` que mapea cada
valor de la clase *MazeTile* a su representación numérica en los
ficheros de entrada, además de otra constante que mapea
cada valor del enum a su representación en la salida embellecida
del programa.

#figure(
  table(
    columns: (auto, auto),
    align: (left + horizon, right + horizon),
    [*Enum*], [*Value*],
    [WALL], [1],
    [EMPTY], [0],
    [START], [3],
    [END], [4],
  ),
  caption: "Valores posibles de una celda de un laberinto"
)


==== MatrixPosition

Representa la posición de una celda en una matriz bidimensional.
Contiene los atributos *row* y *col* que representan la fila y la columna
de la celda en la matriz.

Implementa todos los métodos necesarios para su uso en cualquier
posible situación. Además de los métodos mágicos#footnote()[
  #link("https://docs.python.org/3/reference/datamodel.html#special-method-names")[Magic Methods]: Los métodos mágicos son métodos especiales que permiten definir el comportamiento de los objetos en Python. Por ejemplo, el método `__eq__` se utiliza para comparar objetos.
]
necesarios para
su uso en operaciones, comparaciones y representación.

==== Node

Cada instancia de esta clase actua como un *nodo
y un árbol al mismo tiempo*. Implementa todas las funciones
necesarias para su uso como un árbol. Cada nodo conoce
sus sucesores y su padre. Esta clase hereda de la clase *BaseNode* que
define el comportamiento básico de un nodo y *Node*,
solo añade y modifica los métodos necesarios para su uso en un árbol de
búsqueda.

Gracias a la versatilidad de Python, esta clase
permite la adición en el momento de instanciación de un nodo
una cantidad arbitraria de atributos. Que serán útiles para
la implementación de los algoritmos de búsqueda y su uso
en general.

También permite definir en base a qué atributo se ordenarán
los nodos. Por defecto se ordenan por el atributo *name*.
Pero más adelante veremos que en el algoritmo $A*$ se ordenan
por el atributo *f_score*.

Los *setters* de los atributos de la clase *Node* comprueban
y aseguran la integridad del árbol.

#pagebreak()

==== Maze

Esta clase contiene la representación del laberinto en forma de matriz
y las funciones necesarias para su uso. Además, contiene
la implementación del algoritmo de búsqueda $A*$.

Hereda de la clase *Matrix* que contiene las funciones
necesarias para la representación de una matriz y su uso.

La clase *Maze* contiene las funciones necesarias para
la representación de un laberinto y su uso en el algoritmo
de búsqueda $A*$.

Cada elemento de la matriz representa una celda del laberinto.
Las celdas o "tiles" están representadas por la clase enum
*MazeTile* que contiene los posibles valores de una celda.

==== Algoritmo $A*$

El algoritmo $A*$ es un algoritmo de búsqueda informada que combina
la búsqueda en anchura con la búsqueda heurística. Utiliza una función
de evaluación que combina el coste de llegar a un nodo con una estimación
del coste de llegar al objetivo desde ese nodo.

El algoritmo $A*$ se basa en la siguiente fórmula de evaluación:

$ f(n) = g(n) + h(n) $

Donde: 

- $f(n)$ es el valor de evaluación del nodo $n$.
- $g(n)$ es el coste de llegar al nodo $n$ desde el nodo inicial.
- $h(n)$ es la estimación del coste de llegar al objetivo desde el nodo $n$.

El algoritmo $A*$ expande los nodos con menor valor de evaluación $f(n)$,
priorizando los nodos que tienen un menor coste de llegar al objetivo. 
Esto asegura que el algoritmo encuentre la solución óptima en términos
de coste.

#pagebreak()

#par(first-line-indent: 0em)[
La interfaz del algoritmo $A*$ es la siguiente:
]

#figure(
  ```python
  def a_star(
          self,
          start: MatrixPosition | None = None,
          goal: MatrixPosition | None = None,
          euristic_func: Callable[[MatrixPosition, MatrixPosition], int] | None = None,
          g_score_func: Callable[[MatrixPosition, MatrixPosition], int] | None = None,
          tiles_to_ignore: list[MazeTile] | None = None,
      ) -> list[MatrixPosition] | None:
  ```,
  caption: [Interfaz del algoritmo $A*$]
)


Donde:

- `start` es la posición de inicio.
- `goal` es la posición de destino.
- `euristic_func` es la función heurística a utilizar.
  Por defecto, se utiliza la distancia de Manhattan.
- `g_score_func` es la función de coste $g$ a utilizar.
  Por defecto, se utiliza la función de coste diagonal mayor.
- `tiles_to_ignore` es una lista de celdas a ignorar.
  Por defecto, se ignoran las celdas de tipo `WALL`.


Antes de empezar el bucle principal del algoritmo, se inicializan
las estructuras de datos necesarias para el correcto funcionamiento
del algoritmo.

#figure(
  ```python
      open_set = []
      heapq.heappush(
          open_set,
          Node(
              name=start,
              parent=None,
              position=start,
              compare_by="f_score",
              g_score=0,
              f_score=euristic_func(start, goal),
              h_score=euristic_func(start, goal),
          ),
      )
      came_from = {}
      g_score = {start: 0}
      f_score = {start: euristic_func(start, goal)}

      generated: list[MatrixPosition] = [start]
      inspected: list[MatrixPosition] = []

      history = AlgorithmHistory()
      history.add_step(inspected=inspected, generated=generated, path=[])
  ```,
  caption: [Inicialización del algoritmo $A*$]
) <a-star-init>

Como se puede observar en *@a-star-init*, se inicializan las estructuras
se initializa el `open_set` con el nodo inicial, los
diccionarios de la función de coste $g$ y la función de evaluación $f$,
además de las listas `generated` e `inspected` que contienen las celdas
generadas e inspeccionadas en cada iteración del algoritmo. Por último,
se inicializa el historial del algoritmo. Que contiene la información
sobre cada una de las iteraciones del algoritmo.

#figure(
  ```python
  while open_set:
      current_node: Node = heapq.heappop(open_set)
      current: MatrixPosition = current_node.position
      inspected.append(current)

      if current == goal:
          node_path = current_node.node_path
          position_path = [node.position for node in node_path]
          history.add_step(
              inspected=inspected, generated=generated, path=position_path
          )
          return TraversalResult(
              history,
              path=node_path,
              cost=current_node.f_score,
          )

      for neighbor in self.neighbors(current.row, current.col).values():
          if self[neighbor] in tiles_to_ignore:
              continue
          tentative_g_score = g_score[current] + g_score_func(current, neighbor)
          if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
              came_from[neighbor] = current
              g_score[neighbor] = tentative_g_score
              h_score = euristic_func(neighbor, goal)
              f_score[neighbor] = tentative_g_score + h_score
              new_node = (
                  Node(
                      name=neighbor,
                      parent=current_node,
                      compare_by="f_score",
                      position=neighbor,
                      g_score=tentative_g_score,
                      f_score=f_score[neighbor],
                      h_score=h_score,
                  ),
              )
              heapq.heappush(
                  open_set,
                  new_node[0],
              )
              generated.append(neighbor)
      position_path = [node.position for node in current_node.node_path]
      history.add_step(
          inspected=inspected, generated=generated, path=position_path
      )

      return TraversalResult(history, path=None, cost=None)
  ```,
  caption: [Bucle principal del algoritmo $A*$]
) <a-star-main-loop>

En *@a-star-main-loop* se muestra el bucle principal del algoritmo $A*$.
En cada iteración del bucle, se extrae el nodo con menor valor de evaluación
$f$ del `open_set` y se comprueba si es el nodo objetivo. Si es así, se
devuelve el camino y el coste de la solución. Como estamos empleando
una `heapq` para mantener el `open_set`, el nodo con menor valor de evaluación
se extrae en $O(log n)$. Además nos aseguramos de que si se extrajo el nodo
objetivo, no existen nodos con menor valor $f$ en el `open_set` y por tanto
la solución es óptima.

Cada vez que se extrae un nodo del `open_set`, se añade a la lista `inspected`.

Por cada vecino del `MazeTile` asociado al nodo actual, 
cuyo tipo de `MazeTile` no pertenezca a los ignorados, 
se calcula el coste $g$ y el valor de evaluación
$f$ y se añade a la `open_set`, unicamente si no ha sido visitado
o si se ha encontrado un camino más corto.
Se actualizan los diccionarios `came_from`, `g_score` y `f_score`
con la información del nuevo camino. Por último, se añade el vecino a la lista
`generated` y se actualiza el historial del algoritmo.

= Resultados

Para la evaluación de los resultados se han utilizado diferentes
laberintos, inicios y objetivos. Además, se han comparado diferentes
heurísticas.

== Heurística de la Distancia de Manhattan

// ╒════════════╤═════╤═════╤════════╤════════╤═══════════════════════════════╤════════╤══════════════════════╤══════════════════════╕
// │ Instance   │   n │   m │ S      │ E      │ Path                          │   Cost │   Nº Nodes generated │   Nº Nodes inspected │
// ╞════════════╪═════╪═════╪════════╪════════╪═══════════════════════════════╪════════╪══════════════════════╪══════════════════════╡
// │ M_1        │  11 │  10 │ (4, 0) │ (5, 9) │ (4, 0) -> (5, 1) -> (5, 2) -> │     47 │                   37 │                   25 │
// │            │     │     │        │        │ (5, 3) -> (5, 4) -> (5, 5) -> │        │                      │                      │
// │            │     │     │        │        │ (5, 6) -> (5, 7) -> (5, 8) -> │        │                      │                      │
// │            │     │     │        │        │ (5, 9)                        │        │                      │                      │
// ╞════════════╪═════╪═════╪════════╪═════════╪═══════════════════════════════╪════════╪══════════════════════╪══════════════════════╡
// │ M_1        │  11 │  10 │ (3, 5) │ (10, 3) │ (3, 5) -> (2, 6) -> (3, 7) -> │     60 │                   54 │                   42 │
// │            │     │     │        │         │ (4, 7) -> (5, 7) -> (6, 7) -> │        │                      │                      │
// │            │     │     │        │         │ (7, 7) -> (8, 6) -> (9, 5) -> │        │                      │                      │
// │            │     │     │        │         │ (9, 4) -> (10, 3)             │        │                      │                      │
// ╞════════════╪═════╪═════╪════════╪══════════╪════════════════════════════════╪════════╪══════════════════════╪══════════════════════╡
// │ M_2        │  17 │  17 │ (4, 0) │ (12, 16) │ (4, 0) -> (5, 1) -> (6, 2) ->  │    103 │                  158 │                  127 │
// │            │     │     │        │          │ (7, 3) -> (8, 3) -> (9, 4) ->  │        │                      │                      │
// │            │     │     │        │          │ (10, 5) -> (11, 6) -> (11, 7)  │        │                      │                      │
// │            │     │     │        │          │ -> (11, 8) -> (12, 9) -> (12,  │        │                      │                      │
// │            │     │     │        │          │ 10) -> (12, 11) -> (13, 12) -> │        │                      │                      │
// │            │     │     │        │          │ (12, 13) -> (12, 14) -> (12,   │        │                      │                      │
// │            │     │     │        │          │ 15) -> (12, 16)                │        │                      │                      │
// ╞════════════╪═════╪═════╪════════╪════════╪═══════════════════════════════╪════════╪══════════════════════╪══════════════════════╡
// │ M_3        │   5 │   5 │ (4, 4) │ (1, 0) │ (4, 4) -> (3, 4) -> (2, 4) -> │     36 │                   17 │                   15 │
// │            │     │     │        │        │ (1, 3) -> (0, 2) -> (1, 1) -> │        │                      │                      │
// │            │     │     │        │        │ (1, 0)                        │        │                      │                      │
// ╘════════════╧═════╧═════╧════════╧════════╧═══════════════════════════════╧════════╧══════════════════════╧══════════════════════╛
#figure(
  table(
    columns: (auto, auto, auto, auto, auto, 1fr, auto, auto, auto),
    align: (left, right, right, right, right, right, right, right),
    [*Instance*], [*n*], [*m*], [*S*], [*E*], [*Path*], [*Cost*], [*Nº G*], [*Nº I*],
    [$M_1$], [$11$], [$10$], [$(4, 0)$], [$(5, 9)$], [$(4, 0) -> (5, 1) -> (5, 2) -> (5, 3) -> (5, 4) -> (5, 5) -> (5, 6) -> (5, 7) -> (5, 8) -> (5, 9)$], [$47$], [$37$], [$25$],
    [$M_1$], [$11$], [$10$], [$(3, 5)$], [$(10, 3)$], [$(3, 5) -> (2, 6) -> (3, 7) -> (4, 7) -> (5, 7) -> (6, 7) -> (7, 7) -> (8, 6) -> (9, 5) -> (9, 4) -> (10, 3)$], [$60$], [$54$], [$42$],
    [$M_2$], [$17$], [$17$], [$(4, 0)$], [$(12, 16)$], [$(4, 0) -> (5, 1) -> (6, 2) -> (7, 3) -> (8, 3) -> (9, 4) -> (10, 5) -> (11, 6) -> (11, 7) -> (11, 8) -> (12, 9) -> (12, 10) -> (12, 11) -> (13, 12) -> (12, 13) -> (12, 14) -> (12, 15) -> (12, 16)$], [$103$], [$158$], [$127$],
    [$M_3$], [$5$], [$5$], [$(4, 4)$], [$(1, 0)$], [$(4, 4) -> (3, 4) -> (2, 4) -> (1, 3) -> (0, 2) -> (1, 1) -> (1, 0)$], [$36$], [$17$], [$15$],
  ),
  caption: [Resultados de la evaluación del algoritmo $A*$ con $h(n)$ Manhattan]
) <a-star-results-manhattan>

A continuación se muestra la representación de los resultados obtenidos en la 
*@a-star-results-manhattan*.

#pagebreak()

=== Representación Gráfica

#columns(2)[

#figure(
  image(
    "images/M_1_result.png",
  ),
  caption: [
    Resultado de la evaluación del algoritmo $A*$ con $h(n)$ Manhattan en el laberinto $M_1$
    desde la posición $(4, 0)$ hasta la posición $(5, 9)$.
  ]
)

#figure(
  image(
    "images/M_1_result2.png",
  ),
  caption: [
    Resultado de la evaluación del algoritmo $A*$ con $h(n)$ Manhattan en el laberinto $M_1$
    desde la posición $(3, 5)$ hasta la posición $(10, 3)$.
  ]
)

#figure(
  image(
    "images/M_2_result.png",
  ),
  caption: [
    Resultado de la evaluación del algoritmo $A*$ con $h(n)$ Manhattan en el laberinto $M_2$
    desde la posición $(4, 0)$ hasta la posición $(12, 16)$.
  ]
)

#linebreak()

#figure(
  image(
    "images/M_3_result.png",
  ),
  caption: [
    Resultado de la evaluación del algoritmo $A*$ con $h(n)$ Manhattan en el laberinto $M_3$
    desde la posición $(4, 4)$ hasta la posición $(1, 0)$.
  ]
)

]

#pagebreak()

== Heurística de la Distancia Euclídea

Entre las heurísticas alternativas implementadas en la práctica, se encuentra
la heurística de la distancia euclídea.

La distancia euclídea es una de las heurísticas más comunes en la resolución
de problemas de búsqueda. La distancia euclídea es la distancia más corta
entre dos puntos en un espacio euclídeo. En un espacio bidimensional,
la distancia euclídea entre dos puntos $(x_1, y_1)$ y $(x_2, y_2)$ se calcula
como:

$ d = sqrt((x_2 - x_1)^2 + (y_2 - y_1)^2) $

En este caso, se ha implementado como

$ d = sqrt((x_2 - x_1)^2 + (y_2 - y_1)^2) * W $

donde $W=3$.

// ╒════════════╤═════╤═════╤════════╤════════╤═══════════════════════════════╤════════╤══════════════════════╤══════════════════════╕
// │ Instance   │   n │   m │ S      │ E      │ Path                          │   Cost │   Nº Nodes generated │   Nº Nodes inspected │
// ╞════════════╪═════╪═════╪════════╪════════╪═══════════════════════════════╪════════╪══════════════════════╪══════════════════════╡
// │ M_1        │  11 │  10 │ (4, 0) │ (5, 9) │ (4, 0) -> (4, 1) -> (4, 2) -> │     47 │                   42 │                   32 │
// │            │     │     │        │        │ (5, 3) -> (5, 4) -> (5, 5) -> │        │                      │                      │
// │            │     │     │        │        │ (5, 6) -> (5, 7) -> (5, 8) -> │        │                      │                      │
// │            │     │     │        │        │ (5, 9)                        │        │                      │                      │
// ╞════════════╪═════╪═════╪════════╪═════════╪═══════════════════════════════╪════════╪══════════════════════╪══════════════════════╡
// │ M_1        │  11 │  10 │ (3, 5) │ (10, 3) │ (3, 5) -> (2, 6) -> (3, 7) -> │     60 │                   54 │                   42 │
// │            │     │     │        │         │ (4, 7) -> (5, 7) -> (6, 7) -> │        │                      │                      │
// │            │     │     │        │         │ (7, 7) -> (8, 6) -> (9, 5) -> │        │                      │                      │
// │            │     │     │        │         │ (9, 4) -> (10, 3)             │        │                      │                      │
// ╞════════════╪═════╪═════╪════════╪══════════╪═══════════════════════════════╪════════╪══════════════════════╪══════════════════════╡
// │ M_2        │  17 │  17 │ (4, 0) │ (12, 16) │ (4, 0) -> (5, 1) -> (6, 2) -> │    103 │                  148 │                  130 │
// │            │     │     │        │          │ (7, 3) -> (8, 3) -> (9, 4) -> │        │                      │                      │
// │            │     │     │        │          │ (9, 5) -> (9, 6) -> (9, 7) -> │        │                      │                      │
// │            │     │     │        │          │ (9, 8) -> (10, 9) -> (11, 10) │        │                      │                      │
// │            │     │     │        │          │ -> (12, 11) -> (13, 12) ->    │        │                      │                      │
// │            │     │     │        │          │ (13, 13) -> (13, 14) -> (13,  │        │                      │                      │
// │            │     │     │        │          │ 15) -> (12, 16)               │        │                      │                      │
// ╞════════════╪═════╪═════╪════════╪════════╪═══════════════════════════════╪════════╪══════════════════════╪══════════════════════╡
// │ M_3        │   5 │   5 │ (4, 4) │ (1, 0) │ (4, 4) -> (3, 4) -> (2, 4) -> │     36 │                   17 │                   16 │
// │            │     │     │        │        │ (1, 3) -> (0, 2) -> (0, 1) -> │        │                      │                      │
// │            │     │     │        │        │ (1, 0)                        │        │                      │                      │
// ╘════════════╧═════╧═════╧════════╧════════╧═══════════════════════════════╧════════╧══════════════════════╧══════════════════════╛
#figure(
  table(
    columns: (auto, auto, auto, auto, auto, 1fr, auto, auto, auto),
    align: (left, right, right, right, right, right, right, right),
    [*Instance*], [*n*], [*m*], [*S*], [*E*], [*Path*], [*Cost*], [*Nº G*], [*Nº I*],
    [$M_1$], [$11$], [$10$], [$(4, 0)$], [$(5, 9)$], [$(4, 0) -> (4, 1) -> (4, 2) -> (5, 3) -> (5, 4) -> (5, 5) -> (5, 6) -> (5, 7) -> (5, 8) -> (5, 9)$], [$47$], [$42$], [$32$],
    [$M_1$], [$11$], [$10$], [$(3, 5)$], [$(10, 3)$], [$(3, 5) -> (2, 6) -> (3, 7) -> (4, 7) -> (5, 7) -> (6, 7) -> (7, 7) -> (8, 6) -> (9, 5) -> (9, 4) -> (10, 3)$], [$60$], [$54$], [$42$],
    [$M_2$], [$17$], [$17$], [$(4, 0)$], [$(12, 16)$], [$(4, 0) -> (5, 1) -> (6, 2) -> (7, 3) -> (8, 3) -> (9, 4) -> (9, 5) -> (9, 6) -> (9, 7) -> (9, 8) -> (10, 9) -> (11, 10) -> (12, 11) -> (13, 12) -> (13, 13) -> (13, 14) -> (13, 15) -> (12, 16)$], [$103$], [$148$], [$130$],
    [$M_3$], [$5$], [$5$], [$(4, 4)$], [$(1, 0)$], [$(4, 4) -> (3, 4) -> (2, 4) -> (1, 3) -> (0, 2) -> (0, 1) -> (1, 0)$], [$36$], [$17$], [$16$],
  ),
  caption: [Resultados de la evaluación del algoritmo $A*$ con $h(n)$ Euclídea]
) <a-star-results-euclidean>

En terminos generales y comparando los resultados obtenidos con la heurística
de la distancia de Manhattan de la *@a-star-results-manhattan*, se puede observar
que la heurística de la distancia euclídea obtiene ligeramente peores resultados
en términos de nodos generados e inspeccionados.

A continuación se muestra la representación de los resultados obtenidos en la
*@a-star-results-euclidean*.

#pagebreak()

=== Representación Gráfica

#columns(2)[

#figure(
  image(
    "images/M_1_result_euclidean.png",
  ),
  caption: [
    Resultado de la evaluación del algoritmo $A*$ con $h(n)$ Euclídea en el laberinto $M_1$
    desde la posición $(4, 0)$ hasta la posición $(5, 9)$.
  ]
)

#figure(
  image(
    "images/M_1_result2_euclidean.png",
  ),
  caption: [
    Resultado de la evaluación del algoritmo $A*$ con $h(n)$ Euclídea en el laberinto $M_1$
    desde la posición $(3, 5)$ hasta la posición $(10, 3)$.
  ]
)

#figure(
  image(
    "images/M_2_result_euclidean.png",
  ),
  caption: [
    Resultado de la evaluación del algoritmo $A*$ con $h(n)$ Euclídea en el laberinto $M_2$
    desde la posición $(4, 0)$ hasta la posición $(12, 16)$.
  ]
)

#linebreak()

#figure(
  image(
    "images/M_3_result_euclidean.png",
  ),
  caption: [
    Resultado de la evaluación del algoritmo $A*$ con $h(n)$ Euclídea en el laberinto $M_3$
    desde la posición $(4, 4)$ hasta la posición $(1, 0)$.
  ]
)

]

#pagebreak()

= Conclusiones Generales

En esta práctica se ha implementado el algoritmo de búsqueda $A*$ en Python
para encontrar el camino más corto en un laberinto. Se han implementado
diferentes heurísticas para la estimación del coste de llegar al objetivo
desde un nodo. Además, se han evaluado los resultados obtenidos con diferentes
laberintos, inicios y objetivos.

En términos generales, el algoritmo $A*$ ha obtenido buenos resultados
en la resolución de los laberintos. La heurística de la distancia de Manhattan
ha obtenido mejores resultados en términos de nodos generados e inspeccionados
que la heurística de la distancia euclídea.

Por último, se ha aplicado el principio de diseño SOLID en la implementación
de la práctica. Gracias a la aplicación de estos principios, el diseño
de la práctica es más claro, mantenible y escalable, permitiendo que el código
sea más fácil de entender y modificar.
