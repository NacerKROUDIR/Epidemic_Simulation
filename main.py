import pygame
import pymunk
import numpy as np
import matplotlib.pyplot as plt
import Interactive_Tools as it
import matplotlib
import matplotlib.backends.backend_agg as agg
matplotlib.use("Agg")
plt.rcParams['axes.facecolor'] = (0.67,0.67,0.67)

"""tutrial video: https://www.youtube.com/watch?v=yJK5J8a7NFs"""
pygame.init()
pygame.display.set_caption("Epidemic Simulation Tool")
font = pygame.font.Font(None, 25)
font2 = pygame.font.Font(None, 20)
BACKGROUND_COLOR = (170, 170, 170)
WIDTH, HEIGHT = 1400, 800
width, height = 900, 500
display = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
space = pymunk.Space()
min_speed, max_speed = -80, 80
FPS = 30
day_length_in_frames = 30
two_days = day_length_in_frames*2
day = 0
infection_radius = 16  # 4 to 30
radius = infection_radius/2
drawing_radius = 4
population = 300
percentage_initially_infected = 1  # %
initially_infected = int(np.ceil(population * percentage_initially_infected/100))
probability_of_infection = 100     # %
probability_of_symptoms = 100      # %
recovery_time = 10  # seconds
social_distancing = False
quarantine = False
quarantine_after = 5  # seconds
mode = 0
enable_traveling = True
wall1_x, wall2_x = width//3 + 1, 2*width//3 + 1
wall1_y, wall2_y = height//3 + 1, 2*height//3 + 1
community1_x, community1_y = width//6, height//6
community2_x, community2_y = width//2, community1_y
community3_x, community3_y = 5*width//6, community1_y
community4_x, community4_y = community1_x, height//2
community5_x, community5_y = community2_x, community4_y
community6_x, community6_y = community3_x, community4_y
community7_x, community7_y = community1_x, 5*height//6
community8_x, community8_y = community2_x, community7_y
community9_x, community9_y = community3_x, community7_y
communities_coor = [(community1_x, community1_y), (community2_x, community2_y), (community3_x, community3_y),
                    (community4_x, community4_y), (community5_x, community5_y), (community6_x, community6_y),
                    (community7_x, community7_y), (community8_x, community8_y), (community9_x, community9_y)]
practical_probability_of_infection = 0
R0 = 0


class Particle:
    # susceptible_icon = pygame.image.load("/Users/nacerkroudir/Documents/Master's Project/Icons/Susceptible_icon.png")
    # susceptible_icon = pygame.transform.smoothscale(susceptible_icon, (12,12))
    def __init__(self):
        self.radius = radius
        self.body = pymunk.Body()
        self.body.position = np.random.randint(3,width-3), np.random.randint(3,height-3)
        self.body.velocity = np.random.uniform(min_speed, max_speed), np.random.uniform(min_speed, max_speed)
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.density = 1
        self.shape.elasticity = 1
        # libgen sci-hub
        self.probability_of_infection = probability_of_infection/100
        self.infected = False
        self.probability_of_symptoms = probability_of_symptoms/100
        self.symptomatic = False
        self.infected_time = 0
        self.recovered = False
        self.recovery_time = recovery_time*FPS
        space.add(self.body, self.shape)
        self.interaction_with_infected_count = 0
        self.traveling = False
        self.quarantined = False
        x, y = self.body.position
        if mode == 1:
            self.traveling = False
            if x < wall1_x:
                if y < wall1_y:
                    self.community = 1
                elif y < wall2_y:
                    self.community = 4
                else:
                    self.community = 7
            elif x < wall2_x:
                if y < wall1_y:
                    self.community = 2
                elif y < wall2_y:
                    self.community = 5
                else:
                    self.community = 8
            else:
                if y < wall1_y:
                    self.community = 3
                elif y < wall2_y:
                    self.community = 6
                else:
                    self.community = 9

    def draw(self):
        x, y = self.body.position
        if particle.traveling:
            pygame.draw.circle(display, (186, 18, 252), (int(x), int(y)), drawing_radius)
        elif self.infected:
            if self.symptomatic:
                pygame.draw.circle(display, (250,20,20), (int(x), int(y)), drawing_radius)
                pygame.draw.circle(display, (252, 100, 100), (int(x), int(y)), infection_radius, 1)
            else:
                pygame.draw.circle(display, (240, 240, 41), (int(x), int(y)), drawing_radius)
                pygame.draw.circle(display, (245, 245, 91), (int(x), int(y)), infection_radius, 1)
        elif self.recovered:
            pygame.draw.circle(display, (30, 30, 200), (int(x), int(y)), drawing_radius)
        else:
            # display.blit(self.susceptible_icon, (int(x), int(y)))
            pygame.draw.circle(display, (50, 250, 80), (int(x), int(y)), drawing_radius)
        """
        if self.community == 1:
            pygame.draw.circle(display, (30, 30, 200), (int(x), int(y)), drawing_radius)
        elif self.community == 2:
            pygame.draw.circle(display, (200, 30, 200), (int(x), int(y)), drawing_radius)
        elif self.community == 3:
            pygame.draw.circle(display, (30, 200, 200), (int(x), int(y)), drawing_radius)
        elif self.community == 4:
            pygame.draw.circle(display, (30, 30, 30), (int(x), int(y)), drawing_radius)
        elif self.community == 5:
            pygame.draw.circle(display, (150, 150, 30), (int(x), int(y)), drawing_radius)
        elif self.community == 6:
            pygame.draw.circle(display, (30, 100, 0), (int(x), int(y)), drawing_radius)
        elif self.community == 7:
            pygame.draw.circle(display, (200, 20, 50), (int(x), int(y)), drawing_radius)
        elif self.community == 8:
            pygame.draw.circle(display, (60, 150, 6), (int(x), int(y)), drawing_radius)
        else:
            pygame.draw.circle(display, (9, 255, 58), (int(x), int(y)), drawing_radius)
        """

    def initial_infect(self, arbitor=0, space=0, data=0):
        self.infected = True
        decision = np.random.uniform()
        if decision < self.probability_of_symptoms:
            self.symptomatic = True
        self.shape.collision_type = 1
        return False

    def infect(self, arbitor=0, space=0, data=0):
        self.interaction_with_infected_count += 1
        decision = np.random.uniform()
        if decision < self.probability_of_infection:
            self.infected = True
            decision = np.random.uniform()
            if decision < self.probability_of_symptoms:
                self.symptomatic = True
            self.shape.collision_type = 1
        return False

    def pass_time(self):
        self.infected_time += 1
        if self.infected_time >= self.recovery_time:
            if not self.traveling:
                self.shape.collision_type = 2
            self.recovered = True
            self.infected = False
            self.symptomatic = False

    def travel_init(self, destination_x, destination_y):
        self.traveling = True
        self.destination_x = destination_x
        self.destination_y = destination_y
        self.temp_collision_type = self.shape.collision_type
        self.shape.collision_type = 3

    def travel(self):
        self.body.velocity = self.destination_x - self.body.position[0], self.destination_y - self.body.position[1]

    def arrive(self):
        self.traveling = False
        self.shape.collision_type = self.temp_collision_type


class Wall:
    def __init__(self, p1, p2, width=8):
        self.p1 = p1
        self.p2 = p2
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, p1, p2, 2)
        self.shape.elasticity = 1
        self.shape.collision_type = 0
        space.add(self.body, self.shape)
        self.width = width

    def draw(self):
        pygame.draw.lines(display, (0, 0, 0), False, [self.p1, self.p2], self.width)


def disable_collision(arbitor=0, space=0, data=0):
    return False


def initial_infect(particle):
    return particle.initial_infect()


def build_wall(mode):
    if mode == 0:
        # Normal Layout
        walls = np.array((Wall((width + 100, 0), (width + 100, height + 4)),       # right wall
                          Wall((0, 0), (0, height)),                               # left wall
                          Wall((0, 0), (width + 100, 0)),                          # top wall
                          Wall((0, height), (width + 100, height)),                # bottom wall
                          Wall((width, 0), (width, height)),
                          Wall((width, height - 100), (width + 100, height - 100))
                  ))
    elif mode == 1:
        # Communities Layout
        walls = np.array((Wall((width + 100, 0), (width + 100, height + 4)),          # right wall
                          Wall((0, 0), (0, height)),                                  # left wall
                          Wall((0, 0), (width+100, 0)),                               # top wall
                          Wall((0, height), (width+100, height)),                     # bottom wall
                          Wall((width, 0), (width, height)),
                          Wall((width, height-100), (width+100, height-100)),
                          Wall((0, height//3), (width, height//3), 4),
                          Wall((0, 2*height//3), (width, 2*height//3), 4),
                          Wall((width//3, 0), (width//3, height), 4),
                          Wall((2*width//3, 0), (2*width//3, height), 4)
                          ))
    else:
        walls = None
    return walls


def draw_wall(wall):
    return wall.draw()


def populate(population=population, initially_infected=initially_infected):
    particles = [Particle() for _ in range(population)]
    for i in range(4, population+4):
        particles[i-4].shape.collision_type = i
        handler = space.add_collision_handler(i, 1)
        handler.begin = particles[i - 4].infect
        space.add_collision_handler(i, 0)
    space.add_collision_handler(1, 0)
    space.add_collision_handler(2, 0)
    # space.add_collision_handler(3, 0)
    handler = space.add_default_collision_handler()
    handler.begin = disable_collision
    if initially_infected<population:
        np.vectorize(initial_infect)(np.random.choice(particles, initially_infected, replace=False))
    else:
        np.vectorize(initial_infect)(particles)
    return particles


def plot_result(susceptible_count, infected_count, recovered_count):
    number_of_frames = len(susceptible_count)
    colors = ['#ff4c4c', '#34bf49', '#0099e5']
    labels = ['Infected', 'Susceptible', 'Removed']
    fig = plt.figure(figsize=[11.4, 3], dpi=100)
    fig.patch.set_facecolor((0.67,0.67,0.67))
    ax = fig.gca()
    ax.stackplot(range(number_of_frames), infected_count, susceptible_count, recovered_count,
                  colors=colors, labels=labels)
    number_of_days = number_of_frames // day_length_in_frames
    if number_of_days < 10:
        ticks = np.arange(0, number_of_frames + 1, day_length_in_frames).astype(int)
        labels = ['{}'.format(v // day_length_in_frames) for v in ticks]
    elif number_of_days < 50:
        ticks = np.arange(0, number_of_frames + 1, day_length_in_frames*5).astype(int)
        labels = ['{}'.format(v // day_length_in_frames) for v in ticks]
    elif number_of_days < 100:
        ticks = np.arange(0, number_of_frames + 1, day_length_in_frames*10).astype(int)
        labels = ['{}'.format(v // day_length_in_frames) for v in ticks]
    elif number_of_days < 200:
        ticks = np.arange(0, number_of_frames + 1, day_length_in_frames*20).astype(int)
        labels = ['{}'.format(v // day_length_in_frames) for v in ticks]
    elif number_of_days < 500:
        ticks = np.arange(0, number_of_frames + 1, day_length_in_frames * 50).astype(int)
        labels = ['{}'.format(v // day_length_in_frames) for v in ticks]
    else:
        ticks = np.arange(0, number_of_frames + 1, day_length_in_frames * 100).astype(int)
        labels = ['{}'.format(v // day_length_in_frames) for v in ticks]
    plt.xticks(ticks, labels)
    # plt.xlabel('Days')
    plt.ylabel('Population')
    plt.legend()
    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()
    surf = pygame.image.fromstring(raw_data, size, "RGB")
    return surf


# Interactive tools
start_button = it.StartButton(display, font, 'Simulate', 'Pause', 100, 40, (1050, 25))
reset_button = it.ResetButton(display, font, 'Reset', 100, 40, (1250, 25), populate)
active_button = it.ActiveButton(display, font2, ['Normal', 'Communities', 'Central Place'], [100,100,100], 40, (1050,85))
population_slider = it.Slider(display, font, 'Population', (1150, 145), valueRange=(2,1000), initial_value=population, textBGColor=BACKGROUND_COLOR)
percentage_initially_infected_slider = it.Slider(display, font, 'Initially Infected', (1150, 190), valueRange=(1,100), initial_value=percentage_initially_infected, textBGColor=BACKGROUND_COLOR, append_text="%")
infection_radius_slider = it.Slider(display, font, 'Infection Radius', (1150, 235), valueRange=(4, 30), initial_value=infection_radius, textBGColor=BACKGROUND_COLOR)
probability_of_infection_slider = it.Slider(display, font, 'Infection Prob', (1150, 280), valueRange=(0, 100), initial_value=probability_of_infection, textBGColor=BACKGROUND_COLOR, append_text="%")
probability_of_symptoms_slider = it.Slider(display, font, 'Symptoms Prob', (1150, 325), valueRange=(0, 100), initial_value=probability_of_symptoms, textBGColor=BACKGROUND_COLOR, append_text="%")
recovery_time_slider = it.Slider(display, font, 'Recovery Time', (1150, 370), valueRange=(1, 30), initial_value=recovery_time, textBGColor=BACKGROUND_COLOR, append_text="s")
quarantine_toggle = it.Toggle(display, font, 'Quarantine', (1310, 415), initial_value=quarantine, textBGColor=BACKGROUND_COLOR)
quarantine_after_slider = it.Slider(display, font, 'Quarantine After', (1150, 460), valueRange=(1, 30), initial_value=quarantine_after, textBGColor=BACKGROUND_COLOR, append_text="s")
enable_traveling_toggle = it.Toggle(display, font, 'Traveling', (1310, 505), initial_value=enable_traveling, textBGColor=BACKGROUND_COLOR)

# Labels
day_label = it.Label(display, font, 'Day', day, (910, 25), background_color=BACKGROUND_COLOR)
practical_probability_of_infection_label = it.Label(display, font, 'Prob', practical_probability_of_infection, (910, 45), background_color=BACKGROUND_COLOR)
R0_label = it.Label(display, font, 'R0', R0, (910, 65), background_color=BACKGROUND_COLOR)

particles = populate()
free_particles = particles[:]
walls = build_wall(mode)
quarantine_center_x, quarantine_center_y = width+50, height-50
susceptible_count, infected_count, recovered_count = [], [], []
total_infected = initially_infected
quarantine_after = quarantine_after*FPS
infected_count_two_days_ago = initially_infected
i = 1

surf = plot_result(susceptible_count, infected_count, recovered_count)

while True:
    display.fill(BACKGROUND_COLOR)
    display.blit(surf, (-40,500))
    np.vectorize(draw_wall)(walls)

    # Draw Interactive Tools
    if active_button.draw():
        for wall in walls:
            space.remove(wall.body, wall.shape)
        mode = active_button.mode
        walls = build_wall(active_button.mode)
        initially_infected = int(np.ceil(population * percentage_initially_infected / 100))
        particles = reset_button.reset(space, particles, population, initially_infected)
        free_particles = particles[:]
        susceptible_count, infected_count, recovered_count = [], [], []
        total_infected = initially_infected
        practical_probability_of_infection = 0
        day = 0
        infected_count_two_days_ago = initially_infected
        R0 = 0
        if not start_button.paused:
            start_button.pause()
    if population_slider.draw():
        population = population_slider.value
    if percentage_initially_infected_slider.draw():
        percentage_initially_infected = percentage_initially_infected_slider.value
    if infection_radius_slider.draw():
        infection_radius = infection_radius_slider.value
    if probability_of_infection_slider.draw():
        probability_of_infection = probability_of_infection_slider.value
    if probability_of_symptoms_slider.draw():
        probability_of_symptoms = probability_of_symptoms_slider.value
    if recovery_time_slider.draw():
        recovery_time = recovery_time_slider.value
    if quarantine_toggle.draw():
        quarantine = quarantine_toggle.value
    if quarantine_after_slider.draw():
        quarantine_after = quarantine_after_slider.value * FPS
    if enable_traveling_toggle.draw():
        enable_traveling = enable_traveling_toggle.value
    if reset_button.draw():
        initially_infected = int(np.ceil(population * percentage_initially_infected / 100))
        particles = reset_button.reset(space, particles, population, initially_infected)
        free_particles = particles[:]
        susceptible_count, infected_count, recovered_count = [], [], []
        total_infected = initially_infected
        practical_probability_of_infection = 0
        day = 0
        infected_count_two_days_ago = initially_infected
        R0 = 0
        if not start_button.paused:
            start_button.pause()
    start_button.draw()

    # Draw Labels
    practical_probability_of_infection_label.draw(practical_probability_of_infection*100)
    R0_label.draw(R0)
    day_label.draw(day)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            total_interactions_with_infected = 0
            for particle in particles:
                total_interactions_with_infected += particle.interaction_with_infected_count
            print(f"total number of interactions with infected: {total_interactions_with_infected}")
            print(f"practical probability of infection: {practical_probability_of_infection}")
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start_button.pause()
    if not start_button.paused:
        susceptible_count_this_frame = 0
        infected_count_this_frame = 0
        recovered_count_this_frame = 0
        randomness = np.random.uniform(-10, 10, size=population//2)
        total_interactions_with_infected = 0
        for index, particle in enumerate(particles):
            particle.body.velocity = np.clip(particle.body.velocity[0] + randomness[index % (population // 2)], min_speed, max_speed), \
                                     np.clip(particle.body.velocity[1] + randomness[(population - index - 1) % (population // 2)], min_speed, max_speed)
            particle.draw()
            if particle.infected:
                particle.pass_time()
                infected_count_this_frame += 1
                if quarantine:
                    if particle.symptomatic:
                        if not particle.traveling:
                            if not ((width+100 > particle.body.position[0] > width) and (height > particle.body.position[1] > height-100)):
                                if particle.infected_time > quarantine_after:
                                    particle.travel_init(quarantine_center_x, quarantine_center_y)
                                    particle.travel()
                            else:
                                free_particles = [x for x in free_particles if x != particle]
                                particle.quarantined = True
                                particle.arrive()
            elif particle.recovered:
                recovered_count_this_frame += 1
            else:
                susceptible_count_this_frame += 1

            # Disable interruptions when particle is traveling
            if particle.traveling:
                if not ((particle.destination_x + 45 > particle.body.position[0] > particle.destination_x - 45) and (
                        particle.destination_y + 45 > particle.body.position[1] > particle.destination_y - 45)):
                    particle.travel()
                else:
                    if particle.destination_x == quarantine_center_x:
                        particle.quarantined = True
                    particle.arrive()
            total_interactions_with_infected += particle.interaction_with_infected_count

        # Some Statistics
        total_infected = recovered_count_this_frame + infected_count_this_frame - initially_infected
        try:
            practical_probability_of_infection = total_infected / total_interactions_with_infected
        except ZeroDivisionError:
            practical_probability_of_infection = 0
        if i%two_days==0:
            day+=1
            surf = plot_result(susceptible_count, infected_count, recovered_count)
            try:
                R0 = infected_count_this_frame / infected_count_two_days_ago
                infected_count_two_days_ago = infected_count_this_frame
            except ZeroDivisionError:
                infected_count_two_days_ago = infected_count_this_frame
        elif i%day_length_in_frames==0:
            day+=1
            surf = plot_result(susceptible_count, infected_count, recovered_count)
            
        if mode == 1:
            if enable_traveling:
                if i % 90 == 0:
                    particle = np.random.choice(free_particles)
                    if not particle.traveling:
                        destination = np.random.randint(1, 10)
                        while destination == particle.community:
                            destination = np.random.randint(1, 10)
                        particle.travel_init(communities_coor[destination-1][0], communities_coor[destination-1][1])

        if len(susceptible_count) < 20000:
            susceptible_count.append(susceptible_count_this_frame)
            infected_count.append(infected_count_this_frame)
            recovered_count.append(recovered_count_this_frame)
        space.step(1/FPS)
        clock.tick(FPS)
        i += 1
    else:
        for particle in particles:
            particle.draw()
    pygame.display.update()
