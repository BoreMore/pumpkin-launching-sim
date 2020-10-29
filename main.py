import pygame
import os
import math

# init pygame
pygame.init()
pygame.font.init()
pygame.display.set_caption("Virtual Pumpkin Launching Simulation")


    
# window width and height
WIN_WIDTH = 800
WIN_HEIGHT = 600
NEW_WIDTH = WIN_WIDTH
NEW_HEIGHT = WIN_HEIGHT


# bg colors for screens
BG_COLOR = pygame.Color("#ff914d")

# load home screen image
HOME_IMG = pygame.transform.scale(pygame.image.load(os.path.join("images", "PFling_edited.png")), (800, 600))
CANNON_IMG = pygame.transform.scale(pygame.image.load(os.path.join("images", "cannon.png")), (350, 250))
PUMPKIN_IMG = pygame.transform.scale(pygame.image.load(os.path.join("images", "pumpkin.png")), (50, 50))
CANNON_TOP = pygame.transform.scale(pygame.image.load(os.path.join("images", "cannontop.png")), (171, 93))
CANNON_BOTTOM = pygame.transform.scale(pygame.image.load(os.path.join("images", "cannonbottom.png")), (171, 119))

class Button():
    def __init__(self, x, y, w, h, text=''):
        self.btn = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('white')
        self.background_color = pygame.Color('black')
        self.text = text
        self.btn_text = FONT.render(self.text, True, self.color)
        self.clicked = False

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.btn.collidepoint(event.pos):
                self.clicked = True
        else:
            self.clicked = False

        return self.clicked

    def render_button(self, win):
        pygame.draw.rect(win, self.background_color, self.btn)
        win.blit(self.btn_text, self.btn_text.get_rect(center=(self.btn.centerx, self.btn.centery)))


FONT = pygame.font.Font(None, 40)
SMALL_FONT = pygame.font.Font(None, 30)
TITLE_FONT = pygame.font.SysFont("Corbel", 50, bold=True)
COLOR_INACTIVE = pygame.Color('white')
COLOR_ACTIVE = pygame.Color('black')

# input box code adapted from https://stackoverflow.com/questions/46390231/how-to-create-a-text-input-box-with-pygame
class InputBox():

    def __init__(self, x, y, w, h, description='', text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.description = description

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def get_input_text(self):
        return self.text

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, win):
        # blit description text
        self.description_surface = SMALL_FONT.render(self.description, True, (0,0,0))
        win.blit(self.description_surface, self.description_surface.get_rect(right=self.rect.x-10, centery=self.rect.centery))

        # Blit the text.
        win.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(win, self.color, self.rect, 2)

    def reset_text(self):
        self.text = ''
        self.txt_surface = FONT.render('', True, self.color)


# 1 - home screen class
class Homescreen():
    def __init__(self, win):
        # window
        self.win = win

    # fills background with orange and makes background the loaded image
    def fill_bg(self):
        self.win.fill(BG_COLOR)
        self.win.blit(HOME_IMG, [0, 0])

        # create title object and set render title text
        self.title = TITLE_FONT.render("Virtual Pumpkin Launching Sim", True, (0,0,0))
        self.win.blit(self.title, self.title.get_rect(center=(WIN_WIDTH/2, 50)))

    def render_button(self):
        start_button = Button(3*WIN_WIDTH/4-140, 3*WIN_HEIGHT/4-40, 140, 40, text='Start!')
        btns = [start_button]
        return btns

# 2 - pumpkin picking screen
class PumpkinPicking():
    def __init__(self, win):
        # window
        self.win = win
        
    # blank demo background fill
    def blank_bg(self):
        self.win.fill(BG_COLOR)
       
# 3 - initial values screen
class InitialValsScreen():
    def __init__(self, win):
        # window
        self.win = win

    def fill_bg(self):
        self.win.fill(BG_COLOR)
        self.win.blit(CANNON_IMG, CANNON_IMG.get_rect(x=0, centery=(WIN_HEIGHT/2)))

        #title
        self.title = TITLE_FONT.render("Launch Time!", True, (0,0,0))
        self.win.blit(self.title, self.title.get_rect(center=(WIN_WIDTH/2, 50)))

    def launch_button(self):
        launch_btn = Button(3*WIN_WIDTH/4-70, 3*WIN_HEIGHT/4+50, 140, 40, text='Launch')
        return launch_btn

    def reset_button(self):
        reset_btn = Button(WIN_WIDTH/4-70, 3*WIN_HEIGHT/4+50, 140, 40, text='Reset')
        return reset_btn

    def create_textboxes(self):
        launch_angle_input = InputBox(WIN_WIDTH-225, WIN_HEIGHT/4, 140, 40, 'Launch Angle (degrees)')
        launch_vel_input = InputBox(WIN_WIDTH-225, WIN_HEIGHT/4+75, 140, 40, 'Initial Velocity (m/s)')
        mass_input = InputBox(WIN_WIDTH-225, WIN_HEIGHT/4+150, 140, 40, 'Pumpkin Mass (kg)')
        air_resis_coeff_input = InputBox(WIN_WIDTH-225, WIN_HEIGHT/4+225, 140, 40, 'Air Resistance Constant (kg/m)')
        self.input_boxes = [launch_angle_input, launch_vel_input, mass_input, air_resis_coeff_input]

        return self.input_boxes

# 4 - simulation screen
class Simulation():
    def __init__(self, angle, vel, mass, air_resis_coeff):
        self.theta = angle
        self.vel = vel
        self.mass = mass
        self.air_resis_coeff = air_resis_coeff
        self.g = 9.81
        self.tick_count = 0

        self.v_x = self.vel*math.cos(self.theta*math.pi/180)
        self.v_y = self.vel*math.sin(self.theta*math.pi/180)

        self.orig_ticks = int(pygame.time.get_ticks())

        # equations from http://farside.ph.utexas.edu/teaching/336k/lectures/node29.html
        # basically, they're derived using F=ma, integrating to get velocity as a function of time, and integrating that to get position as a function of time
        # do this separately for forces in the x and y direction to get x position and y position as a function of time
        self.v_t = self.mass*self.g/self.air_resis_coeff
        self.x_t = lambda t: (self.v_t*self.v_x/self.g)*(1-math.exp(-self.g*t/self.v_t))
        self.y_t = lambda t: ((self.v_t)/self.g)*(self.v_y+self.v_t)*(1-math.exp(-self.g*t/self.v_t)) - self.v_t*t

        self.img = PUMPKIN_IMG

        self.CANNON_BOTTOM = CANNON_BOTTOM        
        self.CANNON_TOP = pygame.transform.rotate(CANNON_TOP, self.theta)

    def fill_bg(self, win):
        win.fill((135, 206, 250), rect=(0, 0, NEW_WIDTH, WIN_HEIGHT))
        win.fill((96, 128, 56), rect=(0, WIN_HEIGHT, NEW_WIDTH, NEW_HEIGHT-WIN_HEIGHT))

        #title
        self.title = TITLE_FONT.render("time = " + str(round(self.tick_count, 2)) + "s", True, (0,0,0))
        win.blit(self.title, self.title.get_rect(center=(WIN_WIDTH/2, 50)))

    def update_position(self, pumpkin, win):
        self.x_x = self.x_t(self.tick_count)
        self.x_y = self.y_t(self.tick_count)
        win.blit(self.img, self.img.get_rect(centerx=self.CANNON_BOTTOM.get_rect().centerx + (2.5*self.x_x), bottom=(WIN_HEIGHT-(2.5*self.x_y + self.CANNON_TOP.get_rect().centery))))
        win.blit(self.CANNON_TOP, self.CANNON_TOP.get_rect(centerx=self.CANNON_BOTTOM.get_rect().centerx, centery=WIN_HEIGHT-self.CANNON_BOTTOM.get_rect().h))
        win.blit(self.CANNON_BOTTOM, self.CANNON_BOTTOM.get_rect(left=0, bottom=WIN_HEIGHT))
        
        self.new_ticks = pygame.time.get_ticks()
        delta_ticks = (self.new_ticks - self.orig_ticks) / 1000
        self.orig_ticks = self.new_ticks
        self.tick_count += delta_ticks

    def draw_ground(self, win):
        self.ground_line = pygame.Rect(0, WIN_HEIGHT, NEW_WIDTH, 2)
        pygame.draw.rect(win, COLOR_ACTIVE, self.ground_line)
       
    #check for collision with ground
    def collision_with_ground(self):
        return WIN_HEIGHT-(2.5*self.x_y + self.CANNON_TOP.get_rect().centery) > WIN_HEIGHT

# initializes simulation
def init_game():

    global WIN_WIDTH
    global WIN_HEIGHT
    global NEW_WIDTH
    global NEW_HEIGHT

    # initializes window and clock
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    # initialize screen variables
    homescreen_bool = True
    pumpkin_picking_bool = False
    initial_values_screen_bool = False
    simulation_screen_bool = False

    homescreen = Homescreen(win)
    btns = homescreen.render_button()

    vals_screen = InitialValsScreen(win)
    input_boxes = vals_screen.create_textboxes()
    launch_btn = vals_screen.launch_button()
    reset_btn = vals_screen.reset_button()

    # runs game loop
    run = True
    while run:
        # gets all events
        for event in pygame.event.get():
            # quits game
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.VIDEORESIZE:               
                NEW_WIDTH = event.w
                NEW_HEIGHT = event.h
                win = pygame.display.set_mode((NEW_WIDTH, NEW_HEIGHT), pygame.RESIZABLE)
                
            # draw homescreen
            if homescreen_bool:
                homescreen.fill_bg()
                for btn in btns:
                    if btn.check_click(event):
                        # set previous screen to False and next screen to True
                        # this means that the screen set to True will be rendered now
                        homescreen_bool = False
                        initial_values_screen_bool = True

                    btn.render_button(win)
            # draw pumpkin picking screen
            elif pumpkin_picking_bool:
                pumpkin_screen = PumpkinPicking(win)
                pumpkin_screen.blank_bg()
            # draw initial values screen
            elif initial_values_screen_bool:
                vals_screen.fill_bg()
                launch_btn.render_button(win)
                reset_btn.render_button(win)
                for box in input_boxes:
                    box.handle_event(event)
                if launch_btn.check_click(event):
                    
                    # get vals from inputs
                    angle = float(input_boxes[0].get_input_text())
                    vel = float(input_boxes[1].get_input_text())
                    mass = float(input_boxes[2].get_input_text())
                    air_resis_coeff = float(input_boxes[3].get_input_text())
                    simulation = Simulation(angle, vel, mass, air_resis_coeff)
                    initial_values_screen_bool = False
                    simulation_screen_bool = True
                if reset_btn.check_click(event):
                    for box in input_boxes:
                        box.reset_text()
                        box.update()
                        box.draw(win)

        if initial_values_screen_bool:
            vals_screen.fill_bg()
            launch_btn.render_button(win)
            reset_btn.render_button(win)
            for box in input_boxes:
                box.update()
                box.draw(win)
        # draw simulation screen
        elif simulation_screen_bool:
            simulation.fill_bg(win)
            simulation.draw_ground(win)
            simulation.update_position(PUMPKIN_IMG, win)
            if (simulation.collision_with_ground()):
                simulation_screen_bool = False
                initial_values_screen_bool = True
                for box in input_boxes:
                    box.reset_text()
                    box.update()
                    box.draw(win)

        # updates display
        pygame.display.update()
        clock.tick(60)

# runs when program is run
if __name__ == '__main__':
    init_game()