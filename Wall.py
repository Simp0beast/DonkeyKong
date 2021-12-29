from OnBoard import OnBoard


class Wall(OnBoard):
    def __init__(self, raw_image, position):
        super(Wall, self).__init__(raw_image, position)
