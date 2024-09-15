from radarData import RadarData
import matplotlib.pyplot as plt
import time

class BoresightWindow: 
    def __init__(self, max_distance: float, max_angle: float, max_line_lifetime_in_seconds: float):
        self.max_distance = max_distance
        self.max_angle = max_angle
        self.max_line_lifetime_in_seconds = max_line_lifetime_in_seconds

        plt.rcParams["toolbar"] = "None"
        plt.rcParams["figure.facecolor"] = "black"

        self.fig, self.axis = plt.subplots()
        self.fig.canvas.manager.set_window_title("Boresight")
        self.axis.set_xlim(0, self.max_angle)
        self.axis.set_ylim(0, self.max_distance)
        self.axis.set_facecolor("black")
        self.axis.axhline(y=0, color="green", linewidth=1)
        self.axis.axvline(x=0, color="green", linewidth=1)
        self.axis.tick_params(axis="x", colors="green")
        self.axis.tick_params(axis="y", colors="green")
        self.axis.grid(True, which='both', color='gray', linestyle='--', linewidth=0.5)
        self.axis.set_xlabel("Angle (degrees)", color="green")
        self.axis.set_ylabel("Distance (centimeters)", color="green")
        self.fig.show()

    def update(self, radar_data: RadarData):
        current_time = time.time()

        [line.remove() for line in self.axis.lines]

        for angle, distance, creation_time in zip(radar_data.angle, radar_data.distance, radar_data.creation_time):
            age = current_time - creation_time
            alpha = max(0, 1 - age / self.max_line_lifetime_in_seconds)
            self.axis.plot([angle, angle], [distance, self.max_distance], color="green", linestyle="-", linewidth=10, alpha=alpha)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()