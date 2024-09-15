import time

class RadarData:
    def __init__(self, max_points):
        self.distance = []
        self.angle = []
        self.creation_time = []
        self.max_points = max_points

    def append(self, incoming_bytes):
        try:
            incoming_numbers = incoming_bytes.decode("utf-8").split(",")
        except Exception as e:
            print(f"Error in parsing the incoming data: {e}")
            return

        if(len(incoming_numbers) != 2):
            print("Invalid data received")
            return

        angle = float(incoming_numbers[0])
        distance = float(incoming_numbers[1])
        creation_time = time.time()

        self.distance.append(distance)
        self.angle.append(angle)
        self.creation_time.append(creation_time)

        if len(self.distance) > self.max_points:
            self.distance.pop(0)
            self.angle.pop(0)
            self.creation_time.pop(0)