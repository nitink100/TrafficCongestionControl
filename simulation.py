# * IMAGE XY COOD IS TOP LEFT
import random
import math
import time
import threading
import pygame
import sys
import os

# Note: The vehicle detection logic is separated for clarity.
# This simulation uses a density calculation based on vehicle counts in the next lane.

# --- SIMULATION CONFIGURATION ---
SIMULATION_TIME_SECONDS = 300  # How long the simulation will run

# --- TRAFFIC SIGNAL TIMINGS (in seconds) ---
defaultRed = 150
defaultYellow = 5
defaultGreen = 20
defaultMinimumGreen = 10
defaultMaximumGreen = 60
detectionTime = 5  # Time before green light to detect vehicle density

# --- VEHICLE CHARACTERISTICS ---
VEHICLE_TYPES = {0: 'car', 1: 'bus', 2: 'truck', 3: 'rickshaw', 4: 'bike'}
VEHICLE_SPEEDS = {'car': 2.25, 'bus': 1.8, 'truck': 1.8, 'rickshaw': 2, 'bike': 2.5}
# Time it takes for each vehicle type to cross the intersection
TIME_TO_CROSS = {'car': 2, 'bike': 1, 'rickshaw': 2.25, 'bus': 2.5, 'truck': 2.5}
LANE_COUNT = 2

# --- GLOBAL VARIABLES ---
signals = []
timeElapsed = 0
currentGreen = 0  # Indicates which signal is green (0-3)
currentYellow = 0 # 0 for off, 1 for on
nextGreen = (currentGreen + 1) % 4

# --- ASSET PATHS (assuming an 'assets' folder) ---
IMAGE_PATH = "assets/images/"

# --- COORDINATES AND POSITIONS ---
# Vehicle start coordinates
x = {'right': [0, 0, 0], 'down': [755, 727, 697], 'left': [1400, 1400, 1400], 'up': [602, 627, 657]}
y = {'right': [348, 370, 398], 'down': [0, 0, 0], 'left': [498, 466, 436], 'up': [800, 800, 800]}

vehicles = {'right': {0: [], 1: [], 2: [], 'crossed': 0}, 'down': {0: [], 1: [], 2: [], 'crossed': 0},
            'left': {0: [], 1: [], 2: [], 'crossed': 0}, 'up': {0: [], 1: [], 2: [], 'crossed': 0}}
directionNumbers = {0: 'right', 1: 'down', 2: 'left', 3: 'up'}

# Signal, timer, and vehicle count coordinates
signalCoods = [(530, 230), (810, 230), (810, 570), (530, 570)]
signalTimerCoods = [(530, 210), (810, 210), (810, 550), (530, 550)]
vehicleCountCoods = [(480, 210), (880, 210), (880, 550), (480, 550)]

# Stop line coordinates
stopLines = {'right': 590, 'down': 330, 'left': 800, 'up': 535}
defaultStop = {'right': 580, 'down': 320, 'left': 810, 'up': 545}

# Mid-intersection coordinates for turning logic
mid = {'right': {'x': 705, 'y': 445}, 'down': {'x': 695, 'y': 450}, 'left': {'x': 695, 'y': 425}, 'up': {'x': 695, 'y': 400}}
rotationAngle = 3

# Gap between vehicles
gap = 15  # Stopping gap
gap2 = 15 # Moving gap

pygame.init()
simulation = pygame.sprite.Group()

class TrafficSignal:
    def __init__(self, red, yellow, green, minimum, maximum):
        self.red = red
        self.yellow = yellow
        self.green = green
        self.minimum = minimum
        self.maximum = maximum
        self.signalText = ""
        self.totalGreenTime = 0

class Vehicle(pygame.sprite.Sprite):
    def __init__(self, lane, vehicleClass, direction_number, direction, will_turn):
        super().__init__()
        self.lane = lane
        self.vehicleClass = vehicleClass
        self.speed = VEHICLE_SPEEDS[vehicleClass]
        self.direction_number = direction_number
        self.direction = direction
        self.x = x[direction][lane]
        self.y = y[direction][lane]
        self.crossed = 0
        self.willTurn = will_turn
        self.turned = 0
        self.rotateAngle = 0
        
        vehicles[direction][lane].append(self)
        self.index = len(vehicles[direction][lane]) - 1
        
        path = os.path.join(IMAGE_PATH, direction, f"{vehicleClass}.png")
        self.originalImage = pygame.image.load(path)
        self.currentImage = self.originalImage

        if direction == 'right':
            if self.index > 0 and not vehicles[direction][lane][self.index - 1].crossed:
                self.stop = vehicles[direction][lane][self.index - 1].stop - vehicles[direction][lane][self.index - 1].currentImage.get_rect().width - gap
            else:
                self.stop = defaultStop[direction]
            x[direction][lane] -= self.currentImage.get_rect().width + gap
        elif direction == 'left':
            if self.index > 0 and not vehicles[direction][lane][self.index - 1].crossed:
                self.stop = vehicles[direction][lane][self.index - 1].stop + vehicles[direction][lane][self.index - 1].currentImage.get_rect().width + gap
            else:
                self.stop = defaultStop[direction]
            x[direction][lane] += self.currentImage.get_rect().width + gap
        elif direction == 'down':
            if self.index > 0 and not vehicles[direction][lane][self.index - 1].crossed:
                self.stop = vehicles[direction][lane][self.index - 1].stop - vehicles[direction][lane][self.index - 1].currentImage.get_rect().height - gap
            else:
                self.stop = defaultStop[direction]
            y[direction][lane] -= self.currentImage.get_rect().height + gap
        elif direction == 'up':
            if self.index > 0 and not vehicles[direction][lane][self.index - 1].crossed:
                self.stop = vehicles[direction][lane][self.index - 1].stop + vehicles[direction][lane][self.index - 1].currentImage.get_rect().height + gap
            else:
                self.stop = defaultStop[direction]
            y[direction][lane] += self.currentImage.get_rect().height + gap
        
        simulation.add(self)

    def move(self):
        if self.direction == 'right':
            if self.crossed == 0 and self.x + self.currentImage.get_rect().width > stopLines[self.direction]:
                self.crossed = 1
                vehicles[self.direction]['crossed'] += 1
            if (self.x + self.currentImage.get_rect().width <= self.stop or self.crossed or (currentGreen == 0 and currentYellow == 0)):
                if self.index == 0 or self.x + self.currentImage.get_rect().width < vehicles[self.direction][self.lane][self.index - 1].x - gap2:
                    self.x += self.speed
        
        elif self.direction == 'down':
            if self.crossed == 0 and self.y + self.currentImage.get_rect().height > stopLines[self.direction]:
                self.crossed = 1
                vehicles[self.direction]['crossed'] += 1
            if (self.y + self.currentImage.get_rect().height <= self.stop or self.crossed or (currentGreen == 1 and currentYellow == 0)):
                if self.index == 0 or self.y + self.currentImage.get_rect().height < vehicles[self.direction][self.lane][self.index - 1].y - gap2:
                    self.y += self.speed
        
        elif self.direction == 'left':
            if self.crossed == 0 and self.x < stopLines[self.direction]:
                self.crossed = 1
                vehicles[self.direction]['crossed'] += 1
            if (self.x >= self.stop or self.crossed or (currentGreen == 2 and currentYellow == 0)):
                if self.index == 0 or self.x > vehicles[self.direction][self.lane][self.index - 1].x + vehicles[self.direction][self.lane][self.index - 1].currentImage.get_rect().width + gap2:
                    self.x -= self.speed
        
        elif self.direction == 'up':
            if self.crossed == 0 and self.y < stopLines[self.direction]:
                self.crossed = 1
                vehicles[self.direction]['crossed'] += 1
            if (self.y >= self.stop or self.crossed or (currentGreen == 3 and currentYellow == 0)):
                if self.index == 0 or self.y > vehicles[self.direction][self.lane][self.index - 1].y + vehicles[self.direction][self.lane][self.index - 1].currentImage.get_rect().height + gap2:
                    self.y -= self.speed


def initialize():
    signals.append(TrafficSignal(0, defaultYellow, defaultGreen, defaultMinimumGreen, defaultMaximumGreen))
    signals.append(TrafficSignal(defaultRed, defaultYellow, defaultGreen, defaultMinimumGreen, defaultMaximumGreen))
    signals.append(TrafficSignal(defaultRed, defaultYellow, defaultGreen, defaultMinimumGreen, defaultMaximumGreen))
    signals.append(TrafficSignal(defaultRed, defaultYellow, defaultGreen, defaultMinimumGreen, defaultMaximumGreen))
    repeat()


def set_time():
    vehicle_counts = {'car': 0, 'bus': 0, 'truck': 0, 'rickshaw': 0, 'bike': 0}
    for lane in range(3):
        for vehicle in vehicles[directionNumbers[nextGreen]][lane]:
            if not vehicle.crossed:
                vehicle_counts[vehicle.vehicleClass] += 1
    
    green_time = 0
    for v_type, count in vehicle_counts.items():
        green_time += count * TIME_TO_CROSS[v_type]
    
    green_time = math.ceil(green_time / LANE_COUNT)
    print(f'Calculated green time for signal {nextGreen + 1}: {green_time}s')
    
    if green_time < defaultMinimumGreen:
        green_time = defaultMinimumGreen
    elif green_time > defaultMaximumGreen:
        green_time = defaultMaximumGreen
        
    signals[nextGreen].green = green_time


def repeat():
    global currentGreen, currentYellow, nextGreen
    while signals[currentGreen].green > 0:
        update_values()
        if timeElapsed % 1 == 0:
            print_status()
        if signals[currentGreen].red == detectionTime: # Check for the next signal, not current
             if signals[(currentGreen + 1) % 4].red == detectionTime:
                thread = threading.Thread(name="setTime", target=set_time)
                thread.daemon = True
                thread.start()
        time.sleep(1)
    
    currentYellow = 1
    for i in range(3): # Reset stop lines
        vehicles[directionNumbers[currentGreen]][i].clear()

    while signals[currentGreen].yellow > 0:
        update_values()
        if timeElapsed % 1 == 0:
            print_status()
        time.sleep(1)
        
    currentYellow = 0
    
    signals[currentGreen].green = defaultGreen
    signals[currentGreen].yellow = defaultYellow
    signals[currentGreen].red = defaultRed
    
    currentGreen = nextGreen
    nextGreen = (currentGreen + 1) % 4
    signals[nextGreen].red = signals[currentGreen].green + signals[currentGreen].yellow
    repeat()


def print_status():
    status_string = ""
    for i, sig in enumerate(signals):
        if i == currentGreen:
            if currentYellow:
                status_string += f"YELLOW TS{i+1}: {sig.yellow}s  "
            else:
                status_string += f"GREEN  TS{i+1}: {sig.green}s  "
        else:
            status_string += f"RED    TS{i+1}: {sig.red}s  "
    print(f"Time: {timeElapsed}s | {status_string}")


def update_values():
    global timeElapsed
    timeElapsed += 1
    for i, sig in enumerate(signals):
        if i == currentGreen:
            if currentYellow:
                sig.yellow -= 1
            else:
                sig.green -= 1
        else:
            sig.red -= 1


def generate_vehicles():
    while True:
        direction_number = random.choices(range(4), weights=[40, 40, 10, 10])[0]
        direction = directionNumbers[direction_number]
        vehicle_type_num = random.randint(0, 4)
        vehicle_type = VEHICLE_TYPES[vehicle_type_num]
        
        lane_number = 0 if vehicle_type == 'bike' else random.randint(1, 2)
        will_turn = 1 if lane_number == 2 and random.random() < 0.4 else 0
        
        Vehicle(lane_number, vehicle_type, direction_number, direction, will_turn)
        time.sleep(random.uniform(0.5, 2.5))


def main():
    initialization_thread = threading.Thread(name="initialization", target=initialize)
    initialization_thread.daemon = True
    initialization_thread.start()

    vehicle_generation_thread = threading.Thread(name="generateVehicles", target=generate_vehicles)
    vehicle_generation_thread.daemon = True
    vehicle_generation_thread.start()

    # Screen setup
    screenWidth, screenHeight = 1400, 800
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("AI Traffic Simulation")
    
    # Load assets
    background = pygame.image.load(os.path.join(IMAGE_PATH, "intersection.png"))
    red_signal_img = pygame.image.load(os.path.join(IMAGE_PATH, "signals/red.png"))
    yellow_signal_img = pygame.image.load(os.path.join(IMAGE_PATH, "signals/yellow.png"))
    green_signal_img = pygame.image.load(os.path.join(IMAGE_PATH, "signals/green.png"))
    font = pygame.font.Font(None, 30)
    
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        screen.blit(background, (0, 0))
        
        # Display signals
        for i in range(4):
            if i == currentGreen:
                if currentYellow:
                    signals[i].signalText = str(signals[i].yellow)
                    screen.blit(yellow_signal_img, signalCoods[i])
                else:
                    signals[i].signalText = str(signals[i].green)
                    screen.blit(green_signal_img, signalCoods[i])
            else:
                signals[i].signalText = str(signals[i].red)
                screen.blit(red_signal_img, signalCoods[i])

        # Display timers and counts
        for i in range(4):
            text_surf = font.render(signals[i].signalText, True, (255, 255, 255))
            screen.blit(text_surf, signalTimerCoods[i])
            count_text = str(vehicles[directionNumbers[i]]['crossed'])
            count_surf = font.render(count_text, True, (0, 0, 0))
            screen.blit(count_surf, vehicleCountCoods[i])

        # Display elapsed time
        time_text = font.render(f"Time Elapsed: {timeElapsed}", True, (0, 0, 0))
        screen.blit(time_text, (10, 10))
        
        # Update and draw vehicles
        for vehicle in simulation:
            vehicle.move()
            screen.blit(vehicle.currentImage, (vehicle.x, vehicle.y))
        
        pygame.display.update()
        clock.tick(60) # Limit frame rate

if __name__ == "__main__":
    main()