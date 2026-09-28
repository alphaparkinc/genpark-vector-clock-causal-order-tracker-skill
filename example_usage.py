from client import VectorClock

c_a = VectorClock("NodeA")
c_b = VectorClock("NodeB")

c_a.tick()
c_b.tick()
print("Concurrent relationship:", c_a.compare(c_b))

c_a.merge(c_b.clock)
print("After message delivery from B to A:", c_b.compare(c_a))
