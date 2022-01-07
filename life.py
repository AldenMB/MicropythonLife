from random import choice
import framebuf

window = [(i, j) for i in [-1, 0, 1] for j in [-1, 0, 1] if (i, j) != (0, 0)]


class Life:
    def __init__(self, size, buffer):
        self.size = size
        I, J = self.size
        self.buffer = buffer
        self.frame = framebuf.FrameBuffer(self.buffer, I, J, framebuf.MONO_VLSB)
        self.neighbors = bytearray(I * J)
        self.active = None

    def reinitialize(self):
        I, J = self.size
        self.initialize_neighbors()
        self.active = bytearray(1 for __ in range(I * J))

    def step(self):
        I, J = self.size
        next_neighbors = bytearray(I * J)
        next_neighbors[:] = self.neighbors
        next_active = bytearray(I * J)
        for i in range(I):
            for j in range(J):
                if not self.active[i + j * I]:
                    continue
                neigh = self.neighbors[i + j * I]
                if neigh == 2:
                    continue
                old_value = self.frame.pixel(i, j)
                new_value = neigh == 3
                if old_value == new_value:
                    continue
                self.frame.pixel(i, j, new_value)
                next_active[i + j * I] = 1
                nudge = 2 * new_value - 1
                for dx, dy in window:
                    x = (i + dx) % I
                    y = (j + dy) % J
                    next_neighbors[x + y * I] += nudge
                    next_active[x + y * I] = 1
        self.neighbors = next_neighbors
        self.active = next_active
        return self

    def initialize_neighbors(self):
        I, J = self.size
        n = bytearray((I + 2) * (J + 2))
        for i in range(I):
            for j in range(J):
                if self.frame.pixel(i, j):
                    for x, y in window:
                        n[x + i + 1 + (y + j + 1) * (I + 2)] += 1
        for i in range(I + 2):
            n[i + I + 2] += n[i + (I + 2) * (J + 1)]
            n[i + (I + 2) * (J)] += n[i]
        for j in range(1, J + 1):
            n[1 + j * (I + 2)] += n[I + 1 + j * (I + 2)]
            n[I + j * (I + 2)] += n[j * (I + 2)]
        for j in range(J):
            self.neighbors[I * j : I * (j + 1)] = n[
                1 + (I + 2) * (j + 1) : (I + 2) * (j + 2) - 1
            ]

    def randomize(self):
        I, J = self.size
        for i in range(I):
            for j in range(J):
                self.frame.pixel(i, j, choice([False, True]))
        self.reinitialize()
