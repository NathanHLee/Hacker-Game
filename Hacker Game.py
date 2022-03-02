import arcade

# ---- Global Variables ----
# Screen
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Hacker Game"

# Placement of status bars
STATUS_NUMBER_OFFSET_X = 210  # Percent placement
STATUS_NUMBER_OFFSET_Y = -17  # ""
STATUS_WIDTH = 400            # Bar placement
STATUS_HEIGHT = 15            # ""
STATUS_OFFSET_Y = -10         # Bars behind the colours

# Game functions
SPEED_MODIFIER = 2            # Change the speed of the status progression
PLAYER_MOVEMENT_SPEED = 3
# Flip the player sprite
TEXTURE_LEFT = 0              # Looking left
TEXTURE_RIGHT = 1             # Looking right

# ---- ----
class InstructionsView(arcade.View):
    def on_show(self):
        """ Set Background Colour """
        arcade.set_background_color(arcade.color.CHARLESTON_GREEN)
        
    def on_draw(self):
        """ Draw introduction with controls """
        self.clear()
        # Introduction text with controls
        arcade.draw_text("Code Monkey has a project due tonight and hasn't even started yet! "
                         "Help him finish the project, but make sure that he is "
                         "taken care of. Any further delay will cause Code Monkey to fail.", 
                        SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100,
                        arcade.color.WHITE, 
                        font_size=20, font_name="Kenney Pixel Square",
                        anchor_x="center", multiline=True, width=800)
        arcade.draw_text("     Use 'SPACE' when on an object to interact",
                        SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 60,
                        arcade.color.WHITE, 
                        font_size=20, font_name="Kenney Pixel Square",
                        anchor_x="center", multiline=True, width=800)
        arcade.draw_text("  Use the 'LEFT' and 'RIGHT' arrow keys to move.",
                        SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 130,
                        arcade.color.WHITE, 
                        font_size=20, font_name="Kenney Pixel Square",
                        anchor_x="center", multiline=True, width=800)
        arcade.draw_text("Press 'SPACE' to advance", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4 - 100,
                        arcade.color.WHITE, font_size=20, anchor_x="center")
        
    def on_key_press(self, key, modifiers):
        """ Press Space To Continue """
        # Start the game if the user preses space
        if key == arcade.key.SPACE:
            game_view = MainGameView()
            game_view.setup()
            self.window.show_view(game_view)



class EndingView(arcade.View):
    def __init__(self, condition, texture):
        """ Gather Which Ending Screen To Display """
        super().__init__()
        self.condition = condition  # 'condition' is which win/loss ending they finished with. 0 = win screen, 1-3 = different loss screens
        self.texture = texture      # A specific texture appended to the win/loss
        
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)
    
    def on_draw(self):
        """ Draw Which Ending The User Had """
        self.clear()
        # The user had bathroom go to 0%
        if self.condition == 1:
            text = "It's OK. Accidents happen. If we look at the pros, Code Monkey has fresh sheets for his room not covered in Fritos."
            self.texture.draw_sized(SCREEN_WIDTH / 5, SCREEN_HEIGHT / 2, SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100)
            self.condition_text_draw(text, SCREEN_WIDTH / 2)
        # The user had hunger go to 0%
        elif self.condition == 2:
            text = "Code Monkey has stomach pains from not eating, and now is too hungry to eat. He can't continue the project and fails..."
            self.texture.draw_sized(SCREEN_WIDTH / 6, SCREEN_HEIGHT / 6, SCREEN_WIDTH / 3, SCREEN_HEIGHT / 3)
            self.condition_text_draw(text, SCREEN_WIDTH / 2 - 30)
        # The user had sleep go to 0%
        elif self.condition == 3:
            text = "The lack of sleep has caused Code Monkey to be paranoid and develop night terrors."
            self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT)
            self.condition_text_draw(text, SCREEN_WIDTH / 2 - 30)
        # The user completed the project
        elif self.condition == 0:
            text = "Congratulations!"
            self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT)
            self.condition_text_draw(text, SCREEN_WIDTH / 2 - 100)

    
    def condition_text_draw(self, text, placement_x):
        """ Display The Unique Text With Appropriate Image """
        arcade.draw_text(text, placement_x, SCREEN_HEIGHT - 60,
                        arcade.color.WHITE, 
                        font_size=20, anchor_x="center", multiline=True, width=600)
        arcade.draw_text("Press 'SPACE' to replay", 
                        SCREEN_WIDTH + 50, SCREEN_HEIGHT / 6,
                        arcade.color.WHITE, 
                        font_size=15, anchor_x="center", multiline=True, width=600)

    def on_key_press(self, key, modifiers):
        """ Press Space To Continue """
        # Restart the game if the user presses space
        if key == arcade.key.SPACE:
            game_view = InstructionsView()
            game_view.on_show()
            self.window.show_view(game_view)



class StatusBar(arcade.Sprite):
    def __init__(self, colour, cur_progress, max_progress):
        """ Design The Status Bars """
        super().__init__()
        self.colour = colour
        self.cur_progress = cur_progress
        self.max_progress = max_progress

    def draw_progress_number(self):
        """ Draw Current Percent Remaining On The Status """
        percent_string = f"{self.cur_progress:.0f}%"
        arcade.draw_text(percent_string,
                         start_x=self.center_x + STATUS_NUMBER_OFFSET_X,
                         start_y=self.center_y + STATUS_NUMBER_OFFSET_Y,
                         font_size=14,
                         color=arcade.color.WHITE)
    
    def draw_progress_bar(self):
        """ Draw The Progress Bar """
        # Background bar
        if self.cur_progress < self.max_progress:
            arcade.draw_rectangle_filled(center_x=self.center_x,
                                         center_y=self.center_y + STATUS_OFFSET_Y,
                                         width=STATUS_WIDTH,
                                         height=3,
                                         color=arcade.color.BLACK)
        # Main bar
        status_width = STATUS_WIDTH * (self.cur_progress / self.max_progress)
        arcade.draw_rectangle_filled(center_x=self.center_x - 0.5 * (STATUS_WIDTH - status_width),
                                     center_y=self.center_y - 10,
                                     width=status_width,
                                     height=STATUS_HEIGHT,
                                     color=self.colour)
    
class Player(arcade.Sprite):
    def __init__(self, sprite, scale):
        """ Collect Character Information """
        super().__init__()
        self.sprite = sprite
        self.scale = scale
        self.textures = []

        # Create the left and right moving character sprites
        texture = arcade.load_texture(sprite)
        self.textures.append(texture)
        texture = arcade.load_texture(sprite, flipped_horizontally=True)
        self.textures.append(texture)
        # Set default player facing right
        self.texture = texture

    def update(self):
        """ Move The Player """
        self.center_x += self.change_x

        # Change sprite direction on movement
        if self.change_x < 0:
            self.texture = self.textures[TEXTURE_LEFT]
        elif self.change_x > 0:
            self.texture = self.textures[TEXTURE_RIGHT]

        # Check for 'out-of-bounds'
        if self.left < 390:
            self.left = 390
        elif self.right > 1980:
            self.right = 1980
        


class MainGameView(arcade.View):
    def __init__(self):
        """ Create Empty Variables """
        super().__init__()
        # Set up scene
        self.scene = None

        # Set up sprite list
        self.status_bar_list = None          # Status bars
        self.room_objects_list = None        # Objects in the room (unused)
        self.using_room_objects_list = None  # Objects in the room (used)

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

        # Set up a physics engine
        self.physics_engine = None

        # Set up the camera
        self.camera = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        # Check if the player can move
        self.space_pressed = False       # Set to 'if space is pressed, stop moving'

        # Set the background color
        arcade.set_background_color(arcade.color.CHARLESTON_GREEN)
    
    def setup(self):
        """ Set Up Value To Variables """
        # Initialize Scene
        self.scene = arcade.Scene()
        self.status_bar_list = arcade.SpriteList()
        self.room_objects_list = arcade.SpriteList()
        self.using_room_objects_list = arcade.SpriteList()
        
        # Set up the camera
        self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Create the scene so the player doesn't fall throug the floor
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)

        # Set up the player
        self.player_sprite = Player("CodeMonkey.png", .8)
        self.player_sprite.center_x = 1800
        self.player_sprite.center_y = SCREEN_HEIGHT / 2 - 48
        self.scene.add_sprite("Player", self.player_sprite)
        
        # Place the floor
        for x in range(0, 3000, 480):
            wall = arcade.Sprite("Floorboards.png", .25)
            wall.center_x = x
            wall.center_y = SCREEN_HEIGHT / 8
            self.scene.add_sprite("Walls", wall)
        
        # Create the physics engine
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.scene.get_sprite_list("Walls"))
            
        # Set up computer table to hack
        self.computer_sprite = arcade.Sprite("Computer.png", .3)
        self.computer_sprite.center_x = 2000
        self.computer_sprite.center_y = SCREEN_HEIGHT / 2 - 50
        self.room_objects_list.append(self.computer_sprite)
        self.using_computer_sprite = arcade.Sprite("Using_Computer.png", .3)
        self.using_computer_sprite.center_x = 2000
        self.using_computer_sprite.center_y = SCREEN_HEIGHT / 2 - 50
        self.using_room_objects_list.append(self.using_computer_sprite)

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
        self.using_fridge_sprite = arcade.Sprite("Using_Fridge.png", .4)
        self.using_fridge_sprite.center_x = 1000
        self.using_fridge_sprite.center_y = SCREEN_HEIGHT / 2 + 25
        self.using_room_objects_list.append(self.using_fridge_sprite)

        # Set up bed
        self.bed_sprite = arcade.Sprite("Bed.png", .28)
        self.bed_sprite.center_x = 550
        self.bed_sprite.center_y = SCREEN_WIDTH / 2 - 190
        self.room_objects_list.append(self.bed_sprite)
        self.using_bed_sprite = arcade.Sprite("Using_Bed.png", .28)
        self.using_bed_sprite.center_x = 550
        self.using_bed_sprite.center_y = SCREEN_WIDTH / 2 - 190
        self.room_objects_list.append(self.using_bed_sprite)

        # Set up status bars
        self.make_status_bar(arcade.color.YELLOW,     100, 100, 230, 320, 0) # Restroom
        self.make_status_bar(arcade.color.RED_ORANGE, 100, 100, 230, 320, 1) # Hunger
        self.make_status_bar(arcade.color.BLUE,       100, 100, 230, 320, 2) # Sleep
        self.make_status_bar(arcade.color.GREEN,        0, 100,   0,-170, 0) # Hacking Progress

    def append_sprite(self, room_sprite, placement_x, placement_y):
        """ Shorter method of writing 4 appends in the setup function """
        room_sprite.center_x = placement_x
        room_sprite.center_y = placement_y
    
    def make_status_bar(self, colour, cur_progress, max_progress, x, y, offset):
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
        self.status_bar_list.append(bar)
    
    def on_draw(self):
        """ Render The Screen """
        self.clear()
        # Activate the camera
        self.camera.use()

        # Draw the scene
        self.status_bar_list.draw()
        self.using_room_objects_list.draw()
        self.room_objects_list.draw()
        self.scene.draw()

        # Draw the progress bars
        for bar in self.status_bar_list:
            bar.draw_progress_number()
            bar.draw_progress_bar()
    
    def on_update(self, delta_time):
        """ Movement And Game Logic """
        # Move the player
        self.scene.update()
        self.physics_engine.update()
        # Position the camera
        self.center_camera_to_player()
        self.move_status_with_player()
        # Increase or decrease value of status
        self.update_status()

        # Check for an 'end game' condition
        if self.status_bar_list[0].cur_progress <= 0: # The user had bathroom go to 0%
            view = EndingView(1, arcade.load_texture("CodeMonkey_Laundry.png"))
            self.window.show_view(view)
        elif self.status_bar_list[1].cur_progress <= 0: # The user had hunger go to 0%
            view = EndingView(2, arcade.load_texture("CodeMonkey_Hungry.png"))
            self.window.show_view(view)
        elif self.status_bar_list[2].cur_progress <= 0: # The user had sleep go to 0%
            view = EndingView(3, arcade.load_texture("CodeMonkey_SleepDeprived.png"))
            self.window.show_view(view)
        elif self.status_bar_list[3].cur_progress >= 100: # The user completed the project
            view = EndingView(0, arcade.load_texture("Passed.png"))
            self.window.show_view(view)
        
    def update_status(self):
        """ Update The Status Bars """
        self.status_bar_list[0].cur_progress -= .12
        self.status_bar_list[1].cur_progress -= .08
        self.status_bar_list[2].cur_progress -= .04
        
        # Check for bathroom collision
        colliding_bathroom = arcade.check_for_collision(self.player_sprite, self.bathroom_sprite)
        if colliding_bathroom and self.space_pressed:
            # Change the sprites when the function is in use
            self.using_bathroom_sprite.visible = True
            self.bathroom_sprite.visible = False
            self.player_sprite.visible = False
            # Give the player more than what they lose, 12x as much
            self.status_bar_list[0].cur_progress += .72
            # Cap at 100
            if self.status_bar_list[0].cur_progress >= 100:
                self.status_bar_list[0].cur_progress = 100
        # Return sprites when function is not in use
        if (not self.space_pressed):
            self.using_bathroom_sprite.visible = False
            self.bathroom_sprite.visible = True
            self.player_sprite.visible = True

        # Check for fridge collision
        colliding_fridge = arcade.check_for_collision(self.player_sprite, self.fridge_sprite)
        if colliding_fridge and self.space_pressed:
            # Change the sprites when the function is in use
            self.using_fridge_sprite.visible = True
            self.fridge_sprite.visible = False
            self.player_sprite.visible = False
            # Give the player more than what they lose, 12x as much
            self.status_bar_list[1].cur_progress += .48
            # Cap at 100
            if self.status_bar_list[1].cur_progress >= 100:
                self.status_bar_list[1].cur_progress = 100
        # Return sprites when function is not in use
        if (not self.space_pressed):
            self.using_fridge_sprite.visible = False
            self.fridge_sprite.visible = True
            self.player_sprite.visible = True

        # Check for bed collision
        colliding_bed = arcade.check_for_collision(self.player_sprite, self.bed_sprite)
        if colliding_bed and self.space_pressed:
            # Change the sprites when the function is in use
            self.using_bed_sprite.visible = True
            self.bed_sprite.visible = False
            self.player_sprite.visible = False
            # Give the player more than what they lose, 12x as much
            self.status_bar_list[2].cur_progress += .24
            # Cap at 100
            if self.status_bar_list[2].cur_progress >= 100:
                self.status_bar_list[2].cur_progress = 100
        # Return sprites when function is not in use
        if (not self.space_pressed):
            self.using_bed_sprite.visible = False
            self.bed_sprite.visible = True
            self.player_sprite.visible = True

        # Check for computer collision 
        colliding_computer = arcade.check_for_collision(self.player_sprite, self.computer_sprite)
        if colliding_computer and self.space_pressed:
            # Change the sprites when the function is in use
            self.using_computer_sprite.visible = True
            self.computer_sprite.visible = False
            self.player_sprite.visible = False
            # Gain progression for using the computer
            self.status_bar_list[3].cur_progress += .06
            # Cap at 100
            if self.status_bar_list[3].cur_progress >= 100:
                self.status_bar_list[3].cur_progress = 100
        # Return sprites when function is not in use
        if (not self.space_pressed):
            self.using_computer_sprite.visible = False
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
            if self.status_bar_list.center[0] > 320:
                self.status_bar_list.move(-PLAYER_MOVEMENT_SPEED * 2, 0)
        if self.right_pressed == True:
            if self.status_bar_list.center[0] < 1712:
                self.status_bar_list.move(PLAYER_MOVEMENT_SPEED * 2, 0)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = InstructionsView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()