class Arc:
    def __init__(self, left, right, priority):
        self.left = left
        self.right = right

    def is_sufficient(self):
        return self.left.value != self.right.value