# Assignment 1: Environment Exploration

## Task 1: Environment Testing

### Environments Explored

#### 1. MountainCar-v0
A control problem where an underpowered car must build momentum to reach the goal.

**Key Characteristics:**
- **Observation Space**: Position and velocity (2D continuous)
- **Action Space**: 3 discrete actions (left, neutral, right)  
- **Challenge**: Car lacks power to drive directly up the hill
- **Strategy Required**: Build momentum by rocking back and forth

#### 2. Acrobot-v1
An underactuated double pendulum swing-up problem.

**Key Characteristics:**
- **Observation Space**: Joint angles and velocities (6D continuous)
- **Action Space**: 3 discrete torque actions (-1, 0, +1)
- **Challenge**: Only one joint is actuated, must use physics cleverly
- **Strategy Required**: Coordinate swinging motions to reach target height

## Task 2: Environment Analysis

### Comparative Analysis

| Environment | Obs Space | Action Space | Episode Length | Main Challenge |
|-------------|-----------|--------------|----------------|----------------|
| MountainCar | Box(2) | Discrete(3) | ~200 steps | Energy management |
| Acrobot | Box(6) | Discrete(3) | 200-500 steps | Underactuation |

### Key Insights

1. **Sparse Reward Structure**: Both environments provide rewards only upon goal achievement, creating a needle-in-haystack learning problem where random exploration rarely succeeds
2. **Physics-Driven Dynamics**: Success demands understanding momentum conservation, energy transfer, and gravitational effects rather than simple action-reward associations
3. **Strategic Exploration Required**: Random policies achieve <1% success rate, highlighting the need for intelligent exploration strategies that exploit environmental structure
4. **Scalable Complexity**: MountainCar's 2D state space teaches fundamental concepts, while Acrobot's 6D space introduces multi-joint coordination challenges typical of real robotics