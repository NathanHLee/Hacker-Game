import arcade
from matplotlib.pyplot import bar

# --- Globals ---
SCREEN_WIDTH  = 900
SCREEN_HEIGHT = 600
DEFAULT_FONT_SIZE = 16
SCREEN_TITLE = "Hacker Game"

SPRITE_SCALING = 2
PLAYER_MOVEMENT_SPEED = 5

HEALTH_NUMBER_OFFSET_X = 210
HEALTH_NUMBER_OFFSET_Y = -17

HEALTHBAR_WIDTH = 400
HEALTHBAR_HEIGHT = 15
HEALTHBAR_OFFSET_Y = -10

# --- ---
class StatusBar(arcade.Sprite):
    """ Sprite with hit points """
    def __init__(self, colour, cur_progress, max_progress):
        super().__init__()

        # Add extra attributes for progress
        self.max_progress = max_progress
        self.cur_progress = cur_progress
        self.colour = colour

    def draw_progress_number(self):
        """ Draw how much percent remains on the status """
        percent_string = f"{self.cur_progress:.0f}%"
        arcade.draw_text(percent_string,
                         start_x=self.center_x + HEALTH_NUMBER_OFFSET_X,
                         start_y=self.center_y + HEALTH_NUMBER_OFFSET_Y,
                         font_size=14,
                         color=arcade.color.WHITE)

    def draw_progress_bar(self):
        """ Draw the progress bar """
        # Draw the 'unhealthy' background
        if self.cur_progress < self.max_progress:
            arcade.draw_rectangle_filled(center_x=self.center_x,
                                         center_y=self.center_y + HEALTHBAR_OFFSET_Y,
                                         width=HEALTHBAR_WIDTH,
                                         height=3,
                                         color=arcade.color.BLACK)

        # Calculate width based on health
        health_width = HEALTHBAR_WIDTH * (self.cur_progress / self.max_progress)
        arcade.draw_rectangle_filled(center_x=self.center_x - 0.5 * (HEALTHBAR_WIDTH - health_width),
                                     center_y=self.center_y - 10,
                                     width=health_width,
                                     height=HEALTHBAR_HEIGHT,
                                     color=self.colour)



class Player(arcade.Sprite):
    def update(self):
        """ Move the player """
        # Move player.
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Check for out-of-bounds
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1



class HackerGame(arcade.Window):
    def __init__(self):
        """ Variables """
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Our Scene Object
        self.scene = None

        # Set up the sprite list
        self.bar_list = None
        
        # Set up the sprite info
        self.player_sprite = None
        
        # Set the physics engine
        self.physics_engine = None

        # Set the camera
        self.camera = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False

        # Set the background color
        arcade.set_background_color(arcade.color.CHARLESTON_GREEN)


    def setup(self):
        """ Set up the variables. """
        # Initialize Scene
        self.scene = arcade.Scene()
        self.bar_list = arcade.SpriteList()
        # Create the camera
        self.camera = arcade.Camera(self.width, self.height)

        # Create the Sprite lists
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)

        # Set up the player
        self.player_sprite = Player(":resources:images/animated_characters/female_person/femalePerson_idle.png", SPRITE_SCALING)
        self.player_sprite.center_x = 1000
        self.player_sprite.center_y = SCREEN_WIDTH / 2 - 200 #70
        self.scene.add_sprite("Player", self.player_sprite)

        # Place the floor
        for x in range(0, 2000, 480):
            wall = arcade.Sprite("Floorboards.png", .25)
            wall.center_x = x
            wall.center_y = SCREEN_HEIGHT / 8
            self.scene.add_sprite("Walls", wall)

        # Put some crates on the ground
        # This shows using a coordinate list to place sprites
        coordinate_list = [[355, SCREEN_HEIGHT/3], [1800, SCREEN_HEIGHT/3]]
        for coordinate in coordinate_list:
            # Add a crate
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", 0.5)
            wall.position = coordinate
            self.scene.add_sprite("Walls", wall)
        
        # Set up status bars
        bar1 = self.make_status_bars(arcade.color.YELLOW,     100, 100, 230, 320, 0)
        bar2 = self.make_status_bars(arcade.color.RED_ORANGE, 100, 100, 230, 320, 1)
        bar3 = self.make_status_bars(arcade.color.BLUE,       100, 100, 230, 320, 2)
        progress_bar = self.make_status_bars(arcade.color.GREEN, 0, 100, 0, -170, 0)

        # Set those status bars to a list
        self.bar_list.append(bar1)
        self.bar_list.append(bar2)
        self.bar_list.append(bar3)
        self.bar_list.append(progress_bar)
        
        # Create the physics engine
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.scene.get_sprite_list("Walls"))
        

    def make_status_bars(self, colour, cur_progress, max_progress, x, y, offset):
        """ Shorter method of writing 4 progress bars in the setup function """
        self.colour = colour
        self.cur_progress = cur_progress
        self.max_progress = max_progress
        self.x = x
        self.y = y
        self.offset = offset

        # Create a status bar
        bar = StatusBar(self.colour, self.cur_progress, self.max_progress)
        # Position the bar
        bar.center_x = self.player_sprite.center_x - self.x
        bar.center_y = (self.player_sprite.center_y + self.y) - (30 * self.offset)
        return bar


    def on_draw(self):
        """ Render the screen. """
        # This command has to happen before we start drawing
        self.clear()

        # Activate the camera
        self.camera.use()

        # Draw our Scene
        self.scene.draw()
        self.bar_list.draw()

        # Draw the progress bars
        for bar in self.bar_list:
            bar.draw_progress_number()
            bar.draw_progress_bar()


    def on_update(self, delta_time):
        """ Movement and game logic """
        # Move the player
        self.physics_engine.update()
        # Position the camera
        self.center_camera_to_player()
        self.move_status_with_player()
        # Increase or decrease value of status
        self.update_status()


    def update_status(self):
        """ Update the status bars
            *TODO: make it so when the player interacts
                    with a specific object, the proper
                    bars fill back up.
        """
        self.bar_list[0].cur_progress -= .04
        self.bar_list[1].cur_progress -= .02
        self.bar_list[2].cur_progress -= .01

        self.bar_list[3].cur_progress += .01


    def update_player_speed(self):
        """ Allow player movement to flow better """
        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0

        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED


    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.LEFT :
            self.left_pressed = True
            self.update_player_speed()
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
            self.update_player_speed()


    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == arcade.key.LEFT:
            self.left_pressed = False
            self.update_player_speed()
        elif key == arcade.key.RIGHT:
            self.right_pressed = False
            self.update_player_speed()


    def center_camera_to_player(self):
        """ Camera follows the player """
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)

        # Don't let camera travel past 0 or 1300
        if screen_center_x < 0:
            screen_center_x = 0
        elif screen_center_x > 1300:
            screen_center_x = 1300
        player_centered = screen_center_x, 0

        self.camera.move_to(player_centered)

    
    def move_status_with_player(self):
        """ Primitive, but lets the progress bars stay within the screen """
        screen_center_x = self.bar_list[0] - (self.camera.viewport_width / 2)

        # Don't let camera travel past 0 or 1300
        if screen_center_x < 0:
            screen_center_x = 0
        elif screen_center_x > 1300:
            screen_center_x = 1300
        player_centered = screen_center_x, 0

        self.camera.move_to(player_centered)


def main():
    window = HackerGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()