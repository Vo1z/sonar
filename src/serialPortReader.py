from threading import Thread, Event
import serial

class SerialPortReader(Thread):
    def __init__(self, port_id, baud_rate, timeout, max_buffer_size):
        Thread.__init__(self)
        self.serial_port = serial.Serial(port_id, baud_rate, timeout=timeout)
        self.stop_event = Event()
        self.lines = []
        self.max_buffer_size = max_buffer_size

    def run(self):
        while not self.stop_event.is_set():
            if self.serial_port.in_waiting < 1:
                continue
        
            try:
                incoming_bytes = self.serial_port.readline()
            except Exception as e:
                print(f"Error in reading from the serial port: {e}")
                continue

            self.lines.append(incoming_bytes)

            if len(self.lines) > self.max_buffer_size:
                self.lines.pop(0)

            if self.serial_port.in_waiting > self.max_buffer_size:
                self.serial_port.reset_input_buffer()

    def stop(self):
        self.stop_event.set()
        self.join()
        self.serial_port.close()

    def get_last_line_of_bytes(self):
        return self.lines.pop() if len(self.lines) > 0 else None
    
    def is_connected(self):
        return self.serial_port.is_open