# Brick Kreaber
## Game Guide
The objective of the game is to break all the bricks as fast as possible and
beat the highest score! You have five lives, and the game ends if all breakable bricks are lost
or you have lost all five of your lives.

The game includes a paddle and a ball initially and the objective
is to break the bricks using the ball by bouncing the ball
off of the paddle. There are five kinds of bricks -
* Three breakable bricks with health 3, 2, 1 that contribute
3, 2, 1 points of scores respectively.
* Unbreakable brick that contributes 10 points to the score.
* Explosive bricks (!) that cause chain reactions (!) and are worth
one points each.

Use `a` and `d` on your keyboard to move the paddle, `e` to 
shoot the ball if a ball is held by the paddle, and `q` to abort the game.

There is a 75% chance to spawn one of six **exciting** powerups
on breaking a brick.

PowerUps (as described in the requirements document)-
* Paddle Expand: Symbol `E`.
* Paddle Shrink: Symbol `S`.
* Ball Multiplier: Symbol `B`.
* Fast Ball: Symbol `F`
* Thru-ball: Symbol `T`
* Paddle Grab: Symbol `G`. 

---
## Rules
1. Player has five lives
2. Player loses a life if there are no balls currently active
3. Game ends when player destroys all breakable bricks,
or has lost all five of his lives.
4. On losing a life, the board is cleared and reset.
5. On a game end, the highest score achieved in the run is displayed.
6. Bricks are destroyed by forcing a ball to collide with it.
7. Direction of ball is controlled using intelligent positioning of the paddle.

---
## Classes involved
* `Component` The most basic class from which all other elements of the game inherits from.
It describes the position of the object, and methods to render/clear the element from screen.
* `Ball` The ball class is responsible for one instance of a ball element.
It stores relevant attributes like `speed` and direction of motion.
* `Balls` This controls a set of balls active at any time of the game.
It abstracts out details such as movement and collisions of individual balls.
* `Paddle` The paddle class describes the paddle element.
* `Board` The board is essentially a wrapper for a display matrix
which is rendered ever 0.7 seconds on screen.
* `Brick` The brick class describes type, location and score
of a brick instance.
  * `ExplodingBrick` The exploding brick handles explosions and is responsible for initiating chain reactions.
* `PowerUp` The powerup class is the parent class for several other powerup classes.
    * `ExpandPaddle` The class, whose object on activation expands the paddle width
    * `ShrinkPaddle` Shrinks the paddle width
    * ... and so on for all other powerups. These classes inherit from `PowerUp` and override
    the `activate` and `deactivate` functions as defined in their parent `PowerUp` class.
* `Player` The player class just stores information about the player.

---
## OOPS concepts

### Inheritance
We have one `Component` class from which other game
components are inherited from
```python
class Component:
    def __init__(self, x, y, representation):
        ...
```
where the component class stores the representation of the game.
It also describes render and clear methods `render()`, `clear()`,
as well as relevant getters and setters for the location variables (`get_x()`, `get_y()`, `set_x()`, `set_y()`)

```python
class Ball(Component):
    def __init__(self, x, y, xvel, 
                 yvel, representation=[['o']], 
                 free=0, speed=1):
        ...
```
Components (like the ball) inherit from the `Component` class. Thus, they also
inherit attributes and functions defined in the `Component` class, like so
```
ball = Ball(...)
ball.render(<matrix>)
ball.get_x()
```
and so on.

### Polymorphism
There is a `PowerUp` class and other powerups override the 
`activate` and `deactivate` functionality defined in it.

```python
class PowerUp(Component):
    def __init__(self, x, y, 
                 representation, 
                 p_type, 
                 deactivation_time=10):
        ...
    def activate(self):
        ...
    def deactivate(self):
        ...
...
class ExpandPaddle(PowerUp):
    def __init__(self, x, y):
        ...
    def activate(self):
        ...  # override
    def deactivate(self):
        ...  # override
...
class ShrinkPaddle(PowerUp):
    def __init__(self, x, y):
        ...
    def activate(self):
        ...  # override
    def deactivate(self):
        ...  # override
...
...
```
The `activate` and `deactivate` functions are overriden by `ExpandPaddle` and `ShrinkPaddle`.

### Encapsulation
Class and objects are used. Private variables like `_x` are 
defined to contain them within classes and prevents direct access and modification
of data.

### Abstraction
Abstraction is implemented through methods such as `ball.move_relative(...)` etc...

---
## Instructions
```
> pip install -r requirements.txt
> python main.py
```

## Dependencies and requirements
* Python 3

Packages used:
* colorama