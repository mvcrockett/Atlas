# Synfig fallback benchmark

Operation No Pants Sprint 2 fallback after the two-attempt Stretchy circuit breaker.

The scene is a synthetic articulated character, intentionally not production art. It tests:
- Synfig CLI unattended rendering
- 48 distinct frames at 24 fps
- blink
- smile widening
- subtle head motion
- subtle body breathing
- a lower-arm group rotating around an elbow pivot

The existing Farnebäck continuous_engine is untouched.
