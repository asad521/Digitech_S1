

class Section:

    def __init__(self, x1, y1, x2, y2, unit, min, max, name, type, desc):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.unit = unit
        self.min = min
        self.max = max
        self.name = name
        self.type = type
        self.desc = desc

    def set_x1(self, x1):
        self.x1 = x1

    def get_x1(self):
        return self.x1

    def set_y1(self, y1):
        self.y1 = y1

    def get_y1(self):
        return self.y1

    def set_x2(self, x2):
        self.x2 = x2

    def get_x2(self):
        return self.x2

    def set_y2(self, y2):
        self.y2 = y2

    def get_y2(self):
        return self.y2

    def set_unit(self, unit):
        self.unit = unit

    def get_unit(self):
        return self.unit

    def set_min(self, min):
        self.min = min

    def get_min(self):
        return self.min

    def set_max(self, max):
        self.max = max

    def get_max(self):
        return self.max

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_type(self, type):
        self.type = type

    def get_type(self):
        return self.type

    def set_desc(self, desc):
        self.desc = desc

    def get_desc(self):
        return self.desc

    def getAllValues(self):
        return self.x1, self.y1, self.x2, self.y2, self.unit, self.min, self.max, self.name, self.type, self.desc

    def setAllValues(self, x1, y1, x2, y2, unit, min, max, name, type, desc):
        self.x1, self.y1, self.x2, self.y2, self.unit, self.min, self.max, self.name, self.type, self.desc = x1, y1, x2, y2, unit, min, max, name, type, desc