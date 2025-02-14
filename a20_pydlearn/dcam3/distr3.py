from dcam3 import TimeTrack


class Distributor:
    def __init__(self):
        self.tasks = []
        self.purchased = TimeTrack()
        self.classes = TimeTrack()
        self.master = TimeTrack()
        self.timing = TimeTrack()

    def 