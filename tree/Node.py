class Node:
    def __init__(self, left_node=None, right_node=None, value=None, nested_tree=None, av_aod=None):
        self.left_node = left_node
        self.right_node = right_node
        self.value = value
        self.av_aod = av_aod
        self.nested_tree = nested_tree

    def __str__(self):
        return str(self.value)

    def add_node(self, new_node):
        if not self.value:
            self.value = new_node.value
            self.nested_tree = new_node.nested_tree
            self.av_aod = new_node.av_aod

        if new_node.value == self.value:
            return

        if new_node.value < self.value:
            if self.left_node:
                self.left_node.add_node(new_node)
                return
            self.left_node = new_node
            return

        if new_node.value > self.value:
            if self.right_node:
                self.right_node.add_node(new_node)
                return
            self.right_node = new_node
            return

    def search(self, gender: str, occupation: str) -> float:
        node = self.search_gender(gender)
        if not node:
            return
        occupation_node = None
        while not occupation_node:
            occupation_node = node.nested_tree.search_occupation(occupation)

            if not occupation_node:
                break

        if occupation_node:
            return occupation_node
        else:
            return None

    def search_occupation(self, occupation: str):
        if self.value == occupation:
            return self.av_aod

        if occupation < self.value:
            if not self.left_node:
                return
            return self.left_node.search_occupation(occupation)

        if occupation > self.value:
            if not self.right_node:
                return
            return self.right_node.search_occupation(occupation)

    def search_gender(self, gender: str):
        if self.value == gender:
            return self

        if gender < self.value:
            if not self.left_node:
                return
            return self.left_node.search_gender(gender)

        if gender > self.value:
            if not self.right_node:
                return
            return self.right_node.search_gender(gender)
