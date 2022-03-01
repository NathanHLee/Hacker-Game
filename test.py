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
    
    def on_draw(self):
        """ Draw Which Ending The User Had """
        self.clear()
        # The user had bathroom go to 0%
        if self.condition == 1:
            text = "It's OK. Accidents happen. If we look at the pros, Code Monkey has fresh sheets for his room not covered in Fritos."
            self.texture.draw_sized(SCREEN_WIDTH / 5, SCREEN_HEIGHT / 2, SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100)
            condition_text_draw(text)
        # The user had hunger go to 0%
        elif self.condition == 2:
            text = "Code Monkey has stomach pains from not eating, and now is too hungry to eat. He can't continue the project and fails..."
            self.texture.draw_sized(SCREEN_WIDTH / 4, SCREEN_HEIGHT / 4, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            condition_text_draw(text)
        # The user had sleep go to 0%
        elif self.condition == 3:
            text = "The lack of sleep has caused Code Monkey to be paranoid and develop night terrors."
            self.texture.draw_sized(SCREEN_WIDTH /2, SCREEN_HEIGHT /2, SCREEN_WIDTH, SCREEN_HEIGHT)
            condition_text_draw(text)
        # The user completed the project
        elif self.condition == 0:
            text = "Congratulations!"
            self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT)
            condition_text_draw(text)

    
    def condition_text_draw(self, text):
        """ Display The Unique Text With Appropriate Image """
        arcade.draw_text(text, SCREEN_WIDTH / 2, SCREEN_HEIGHT - 60,
                        arcade.color.WHITE, 
                        font_size=20, anchor_x="center", multiline=True, width=600)
        arcade.draw_text("Press 'SPACE' to replay", 
                        SCREEN_WIDTH + 100, SCREEN_HEIGHT / 6,
                        arcade.color.WHITE, 
                        font_size=15, anchor_x="center", multiline=True, width=600)

    def on_key_press(self, key, modifiers):
        """ Press Space To Continue """
        # Start the game if the user preses space
        if key == arcade.key.SPACE:
            game_view = InstructionsView()
            game_view.setup()
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
            
        # Append the image to the 'room_objects_list'    
        self.append_sprite(self.computer_sprite, "Computer.png", .3, 2000, SCREEN_HEIGHT / 2 - 50, self.room_objects_list)
        self.append_sprite(self.bathroom_sprite, "Bathroom.png", .4, 1400, SCREEN_HEIGHT / 2 + 20, self.room_objects_list)
        self.append_sprite(self.fridge_sprite,   "Fridge.png",   .4, 1000, SCREEN_HEIGHT / 2,      self.room_objects_list)
        self.append_sprite(self.bed_sprite,      "Bed.png",     .28,  550, SCREEN_HEIGHT / 2 - 40, self.room_objects_list)
        # Append the image to the 'using_room_objects_list'
        self.append_sprite(self.using_computer_sprite, "Using_Computer.png", .3, 2000, SCREEN_HEIGHT / 2 - 50, self.using_room_objects_list)
        self.append_sprite(self.using_bathroom_sprite, "Using_Bathroom.png", .4, 1400, SCREEN_HEIGHT / 2 + 20, self.using_room_objects_list)
        self.append_sprite(self.using_fridge_sprite,   "Using_Fridge.png",   .4, 1000, SCREEN_HEIGHT / 2,      self.using_room_objects_list)
        self.append_sprite(self.using_bed_sprite,      "Using_Bed.png",     .28,  550, SCREEN_HEIGHT / 2 - 40, self.using_room_objects_list)

        # Set up status bars
        self.make_status_bar(arcade.color.YELLOW,     100, 100, 230, 320, 0) # Restroom
        self.make_status_bar(arcade.color.RED_ORANGE, 100, 100, 230, 320, 1) # Hunger
        self.make_status_bar(arcade.color.BLUE,       100, 100, 230, 320, 2) # Sleep
        self.make_status_bar(arcade.color.GREEN,        0, 100,   0,-170, 0) # Hacking Progress

    def append_sprite(self, room_sprite, image, scale, placement_x, placement_y, list_type):
        """ Shorter method of writing 4 appends in the setup function """
        room_sprite = arcade.Sprite(image, scale)
        room_sprite.center_x = placement_x
        room_sprite.center_y = placement_y
        list_type.append(room_sprite)
    
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
        
        if self.bar_list[0].cur_progress <= 0: # The user had bathroom go to 0%
            view = GameOverView(1, arcade.load_texture("CodeMonkey_Laundry.png"))
            self.window.show_view(view)
        elif self.bar_list[1].cur_progress <= 0: # The user had hunger go to 0%
            view = GameOverView(2, arcade.load_texture("CodeMonkey_Hungry.png"))
            self.window.show_view(view)
        elif self.bar_list[2].cur_progress <= 0: # The user had sleep go to 0%
            view = GameOverView(3, arcade.load_texture("CodeMonkey_SleepDeprived.png"))
            self.window.show_view(view)
        elif self.bar_list[3].cur_progress >= 100: # The user completed the project
            view = GameOverView(0, arcade.load_texture("Passed.png"))
            self.window.show_view(view)
        
    def update_status(self):
        """ Update The Status Bars """
        self.status_bar_list[0].cur_progress -= .06
        self.status_bar_list[1].cur_progress -= .04
        self.status_bar_list[2].cur_progress -= .02

        self.collision_update_status(0, self.bathroom_sprite, self.using_bathroom_sprite, .06)
        self.collision_update_status(1, self.fridge_sprite,   self.using_fridge_sprite,   .04)
        self.collision_update_status(2, self.bed_sprite,      self.using_bed_sprite,      .02)

    def collision_update_status(self, sprite_index, sprite_object, sprite_object_using, sprite_value):
        """ Increase The Status When The Player Interacts """
        # Check for collision
        print(sprite_object_using)
        collision = arcade.check_for_collision(self.player_sprite, sprite_object)
        if collision and self.space_pressed:
            # Change the sprites when the function is in use
            self.player_sprite.visible = False
            sprite_object.visible = False
            sprite_object_using.visible = True
            # Give the player more than what they lose, 6x as much
            self.status_bar_list[sprite_index].cur_progress += (sprite_value * 6)
            # Cap at 100
            if self.status_bar_list[sprite_index].cur_progress >= 100:
                self.status_bar_list[sprite_index].cur_progress = 100
        # Return sprites when function is not in use
        if (not self.space_pressed):
            self.player_sprite.visible = True
            sprite_object.visible = True
            sprite_object_using.visible = False

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
            if self.bar_list.center[0] > 320:
                self.bar_list.move(-PLAYER_MOVEMENT_SPEED * 2, 0)
        if self.right_pressed == True:
            if self.bar_list.center[0] < 1712:
                self.bar_list.move(PLAYER_MOVEMENT_SPEED * 2, 0)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = InstructionsView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()