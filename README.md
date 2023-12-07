# PyPhys2D
<p>PyPhys2D is a 2D physic engine framework written in python. This is a simple project for Intro to Game Programming Class. The framework depend on some of the Pygame&apos;s module for the Vector2 and the debug rendering.</p>

# Documentation
## Body
`Body` class represents a generic physics body in 2D space. This class act as a base class for circle and box class. You will not directly create this body class.

### Properties:

- `mass` : Mass of the body.
- `physictype` : Type of physics body (DYNAMIC or STATIC).
- `invmass` : Inverse of mass (1/mass).
- `elasticity` : Elasticity coefficient for collisions.
- `staticfriction` : Coefficient of static friction.
- `dynamicfriction` : Coefficient of dynamic friction.
- `inertia` : Moment of inertia of the body. (Resistance to rotate)
- `velocity` : Current velocity of the body.
- `force` : Accumulated force acting on the body.
- `position` : Current center position of the body.
- `angle` : Current orientation angle.
- `angularvel` : Angular velocity.
- `color` : RGB tuple representing the color of the body for debugging purpose.

### Methods:

- move(xamount, yamount): Move the body by a specified amount.
- addforce(xforce,yforce): Add external force to the body.

## Circle
`Circle` class extends the body class to represent circle with additional properties

### Properties:

- `radius` : radius of the circle

## Box
`Box` class extends the body class to represent box with additional properties

### Properties:

- `width` : width of the box
- `height` : height of the box
- `vertices` : A list of vertices of the box in local coordinate in order of left top clockwise
- `transvertices` : A list of transformed vertices of the box in global coordinate in order of left top clockwise

## World
The `World` class represents a simulation world for 2D physics. It manages physics bodies, performs collision detection, and resolves collisions.

### Properties:

- `gravity` : A 2D vector representing the gravitational force applied in the world.
- `bodylist` : A list containing physics bodies in the world.

### Methods:

### `step(substep, dt)`

```python
def step(self, substep, dt):
    """
    Advances the simulation by taking multiple substeps.

    Parameters:
    - substep: The number of substeps to take.
    - dt: The time difference between substep.
    """
```
### `debugdraw(window)`

```python
def debugdraw(self, window):
    """
    Draws the physics bodies in the world for debugging purposes.

    Parameters:
    - window: Pygame window surface.
    """
```
### `setgravity(value)`

```python
def setgravity(self, value):
    """
    Sets the gravitational force in the world.

    Parameters:
    - value: The magnitude of the gravitational force in float.
    """
```
### `addbody(body)`

```python
def addbody(self, body):
    """
    Adds a physics body to the world.

    Parameters:
    - body: An instance of the Body class to be added to the world.
    """
```
### `removebody(body)`

```python
def removebody(self, body):
    """
    Removes a physics body from the world.

    Parameters:
    - body: An instance of the Body class to be removed from the world.
    """
```

# Demo
I also include a demo on how to use the module.
