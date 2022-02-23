import arcade
from matplotlib.pyplot import bar

# --- Globals ---
SCREEN_WIDTH  = 900
SCREEN_HEIGHT = 600
DEFAULT_FONT_SIZE = 16
SCREEN_TITLE = "Hacker Game"

SPRITE_SCALING = 2
SPEED_MODIFIER = 10 # Change to speed up the status progression
PLAYER_MOVEMENT_SPEED = 10

STATUS_NUMBER_OFFSET_X = 210
STATUS_NUMBER_OFFSET_Y = -17
STATUS_WIDTH = 400
STATUS_HEIGHT = 15
STATUS_OFFSET_Y = -10

# --- ---
class InstructionsView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.CHARLESTON_GREEN)
        arcade.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
    
    def on_draw(self):
        self.clear()
        arcade.draw_text("Instructions Screen", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                        arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 75,
                        arcade.color.WHITE, font_size=20, anchor_x="center")
    
    def on_mouse_press(self, x, y, button, modifiers):
        game_view = HackerGameView()
        game_view.setup()
        self.window.show_view(game_view)



class GameOverView(arcade.View):
    def __init__(self, condition):
        super().__init__()
        self.condition = condition
        self.texture = arcade.load_texture("computer.png")

        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_draw(self):
        self.clear()
        if self.condition == 1:
            self.texture.draw_sized(SCREEN_WIDTH / 4, SCREEN_HEIGHT / 2, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            arcade.draw_text("You didn't make it to the bathroom in time and created a mess in your room. "
                            "Mama didn't raise no child not to use the facilities properly, which in turn, got "
                            "you grounded from using the computer for 2 weeks, causing you to fail your project. " 
                            "You got the worst ending.", 
                            SCREEN_WIDTH / 2, SCREEN_HEIGHT - 60,
                            arcade.color.WHITE, 
                            font_size=20, 
                            anchor_x="center", multiline=True, width=600)

    def on_mouse_press(self, x, y, button, modifiers):
        game_view = InstructionsView()
        game_view.on_show()
        self.window.show_view(game_view)



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
                         start_x=self.center_x + STATUS_NUMBER_OFFSET_X,
                         start_y=self.center_y + STATUS_NUMBER_OFFSET_Y,
                         font_size=14,
                         color=arcade.color.WHITE)

    def draw_progress_bar(self):
        """ Draw the progress bar """
        # Draw the 'unhealthy' background
        if self.cur_progress < self.max_progress:
            arcade.draw_rectangle_filled(center_x=self.center_x,
                                         center_y=self.center_y + STATUS_OFFSET_Y,
                                         width=STATUS_WIDTH,
                                         height=3,
                                         color=arcade.color.BLACK)

        # Calculate width based on status
        status_width = STATUS_WIDTH * (self.cur_progress / self.max_progress)
        arcade.draw_rectangle_filled(center_x=self.center_x - 0.5 * (STATUS_WIDTH - status_width),
                                     center_y=self.center_y - 10,
                                     width=status_width,
                                     height=STATUS_HEIGHT,
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



class HackerGameView(arcade.View):
    def __init__(self):
        """ Variables """
        super().__init__()

        # Our Scene Object
        self.scene = None

        # Set up the sprite list
        self.bar_list = None                # Status bars
        self.room_objects_list = None       # Objects in the room
        self.using_room_objects_list = None # Objects being used in the room
        
        # Set up the sprite info
        self.player_sprite = None
        self.computer_sprite = None
        self.bathroom_sprite = None
        self.fridge_sprite = None
        self.bed_sprite = None
        # Set up the 'in-use' sprite info
        self.using_computer_sprite = None
        self.using_bathroom_sprite = None
        self.using_fridge_sprite = None
        self.using_bed_sprite = None
        
        # Set the physics engine
        self.physics_engine = None

        # Set the camera
        self.camera = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        # Check if the player can move
        self.space_pressed = False

        # Set the background color
        arcade.set_background_color(arcade.color.CHARLESTON_GREEN)


    def setup(self):
        """ Set up the variables. """
        # Initialize Scene
        self.scene = arcade.Scene()
        self.bar_list = arcade.SpriteList()
        self.room_objects_list = arcade.SpriteList()
        self.using_room_objects_list = arcade.SpriteList()
        # Create the camera
        self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Create the Sprite lists
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)

        # Set up the player
        self.player_sprite = Player(":resources:images/animated_characters/female_person/femalePerson_idle.png", SPRITE_SCALING)
        self.player_sprite.center_x = 1800
        self.player_sprite.center_y = SCREEN_HEIGHT / 2 - 53
        self.scene.add_sprite("Player", self.player_sprite)

        # Set up computer table to hack
        self.computer_sprite = arcade.Sprite("Computer.png", .3)
        self.computer_sprite.center_x = 2000
        self.computer_sprite.center_y = SCREEN_HEIGHT / 2 - 50
        self.room_objects_list.append(self.computer_sprite)

        # Set up bathroom
        self.bathroom_sprite = arcade.Sprite("Bathroom.png", .4)
        self.bathroom_sprite.center_x = 1400
        self.bathroom_sprite.center_y = SCREEN_HEIGHT / 2 + 20
        self.room_objects_list.append(self.bathroom_sprite)
        self.using_bathroom_sprite = arcade.Sprite("Using_Bathroom.png", .4)
        self.using_bathroom_sprite.center_x = 1400
        self.using_bathroom_sprite.center_y = SCREEN_HEIGHT / 2 + 20
        self.using_room_objects_list.append(self.using_bathroom_sprite)

        # Set up fridge
        self.fridge_sprite = arcade.Sprite("Fridge.png", .4)
        self.fridge_sprite.center_x = 1000
        self.fridge_sprite.center_y = SCREEN_HEIGHT / 2
        self.room_objects_list.append(self.fridge_sprite)

        # Set up bed
        self.bed_sprite = arcade.Sprite("Bed.png", .28)
        self.bed_sprite.center_x = 550
        self.bed_sprite.center_y = SCREEN_WIDTH / 2 - 190
        self.room_objects_list.append(self.bed_sprite)


        # Place the floor
        for x in range(0, 3000, 480):
            wall = arcade.Sprite("Floorboards.png", .25)
            wall.center_x = x
            wall.center_y = SCREEN_HEIGHT / 8
            self.scene.add_sprite("Walls", wall)

        # Put some crates on the ground
        # This shows using a coordinate list to place sprites
        coordinate_list = [[390, SCREEN_HEIGHT/4 + 1], [1980, SCREEN_HEIGHT/4 + 1]]
        for coordinate in coordinate_list:
            # Add a crate
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", 0.01)
            wall.position = coordinate
            self.scene.add_sprite("Walls", wall)
        
        # Set up status bars
        bar1 = self.make_status_bars(arcade.color.YELLOW,     100, 100, 230, 320, 0) # 
        bar2 = self.make_status_bars(arcade.color.RED_ORANGE, 100, 100, 230, 320, 1) # Hunger
        bar3 = self.make_status_bars(arcade.color.BLUE,       100, 100, 230, 320, 2) # Sleep
        progress_bar = self.make_status_bars(arcade.color.GREEN, 0, 100, 0, -170, 0) # Hacking Progress

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
        self.bar_list.draw()
        self.using_room_objects_list.draw()
        self.room_objects_list.draw()
        self.scene.draw()

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
        
        if self.bar_list[0].cur_progress <= 0:
            view = GameOverView(1)
            self.window.show_view(view)

    def update_status(self):
        """ Update the status bars
            *TODO: make it so when the player interacts
                    with a specific object, the proper
                    bars fill back up.
        """
        self.bar_list[0].cur_progress -= .05 * SPEED_MODIFIER
        self.bar_list[1].cur_progress -= .03 * SPEED_MODIFIER
        self.bar_list[2].cur_progress -= .01 * SPEED_MODIFIER

        # Check for bathroom collision
        colliding_bathroom = arcade.check_for_collision(self.player_sprite, self.bathroom_sprite)
        if colliding_bathroom and self.space_pressed:
            # Change the sprites when the function is in use
            self.using_bathroom_sprite.visible = True
            self.bathroom_sprite.visible = False
            self.player_sprite.visible = False
            # Give the player more than what they lose, 6x as much
            self.bar_list[0].cur_progress += .3 * SPEED_MODIFIER
            # Cap at 100
            if self.bar_list[0].cur_progress >= 100:
                self.bar_list[0].cur_progress = 100
        # Return sprites when function is not in use
        if (not self.space_pressed):
            self.using_bathroom_sprite.visible = False
            self.bathroom_sprite.visible = True
            self.player_sprite.visible = True

        # Check for fridge collision
        colliding_fridge = arcade.check_for_collision(self.player_sprite, self.fridge_sprite)
        if colliding_fridge and self.space_pressed:
            # Change the sprites when the function is in use
            self.fridge_sprite.visible = False
            self.player_sprite.visible = False
            # Give the player more than what they lose, 6x as much
            self.bar_list[1].cur_progress += .18 * SPEED_MODIFIER
            # Cap at 100
            if self.bar_list[1].cur_progress >= 100:
                self.bar_list[1].cur_progress = 100
        # Return sprites when function is not in use
        if (not self.space_pressed):
            self.fridge_sprite.visible = True
            self.player_sprite.visible = True

        # Check for bed collision
        colliding_bed = arcade.check_for_collision(self.player_sprite, self.bed_sprite)
        if colliding_bed and self.space_pressed:
            # Change the sprites when the function is in use
            self.bed_sprite.visible = False
            self.player_sprite.visible = False
            # Give the player more than what they lose, 6x as much
            self.bar_list[2].cur_progress += .06 * SPEED_MODIFIER
            # Cap at 100
            if self.bar_list[2].cur_progress >= 100:
                self.bar_list[2].cur_progress = 100
        # Return sprites when function is not in use
        if (not self.space_pressed):
            self.bed_sprite.visible = True
            self.player_sprite.visible = True

        # Check for computer collision 
        colliding_computer = arcade.check_for_collision(self.player_sprite, self.computer_sprite)
        if colliding_computer and self.space_pressed:
            # Change the sprites when the function is in use
            self.computer_sprite.visible = False
            self.player_sprite.visible = False
            # Give the player more than what they lose, 6x as much
            self.bar_list[3].cur_progress += .02 * SPEED_MODIFIER
            # Cap at 100
            if self.bar_list[3].cur_progress >= 100:
                self.bar_list[3].cur_progress = 100
        # Return sprites when function is not in use
        if (not self.space_pressed):
            self.computer_sprite.visible = True
            self.player_sprite.visible = True


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
        if key == arcade.key.SPACE:
            self.space_pressed = not self.space_pressed

        if key == arcade.key.LEFT and not self.space_pressed:
            self.left_pressed = True
            self.update_player_speed()
        elif key == arcade.key.RIGHT and not self.space_pressed:
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

        # Don't let camera travel past the bounds of the map
        if screen_center_x < 0:
            screen_center_x = 0
        elif screen_center_x > 1600:
            screen_center_x = 1600
        player_centered = screen_center_x, 0

        self.camera.move_to(player_centered)

    
    def move_status_with_player(self):
        """ Primitive, but lets the progress bars stay within the screen """
        
        if self.left_pressed == True:
            if self.bar_list.center[0] > 280:
                self.bar_list.move(-PLAYER_MOVEMENT_SPEED, 0)
        if self.right_pressed == True:
            if self.bar_list.center[0] < 1728:
                self.bar_list.move(PLAYER_MOVEMENT_SPEED, 0)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = InstructionsView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()