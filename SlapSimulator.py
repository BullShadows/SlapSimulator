from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Mesh
from kivy.core.image import Image as CoreImage
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout  # Import FloatLayout
from kivy.graphics import Rectangle
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader
slap_sound = SoundLoader.load('slap.mp3')
menu_sound = SoundLoader.load('jeff_song.mp3')

class StretchableImage(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Image source
        self.image_source = "hand.png"
        
        # Define the initial vertices dynamically based on screen size
        self.image_width = Window.width * 0.2  # 20% of screen width
        self.image_height = Window.height * 0.4  # 40% of screen height
        
        # Initial vertices
        self.vertices = [
            (Window.width / 2) - (self.image_width / 2), Window.height / 2 + self.image_height / 2,  # Top-left
            (Window.width / 2) + (self.image_width / 2), Window.height / 2 + self.image_height / 2,  # Top-right
            (Window.width / 1.2) + (self.image_width / 2), Window.height / 2 - self.image_height / 2,  # Bottom-right
            (Window.width / 1.2) - (self.image_width / 2), Window.height / 2 - self.image_height / 2   # Bottom-left
        ]
        # Define the indices for the Mesh (a rectangle made of 2 triangles)
        self.indices = [0, 1, 2, 2, 3, 0]

        # Create the mesh to render the image
        with self.canvas:
            self.mesh = Mesh(
                vertices=self._format_vertices(),
                indices=self.indices,
                mode="triangle_fan",
                texture=self._load_texture(self.image_source),
            )
        # Bind mouse motion and window resizing
        Window.bind(mouse_pos=self.on_mouse_move)
        Window.bind(on_resize=self.on_window_resize)
    def update_mesh_texture(self, new_image_source):
        """Update the texture of the mesh."""
        self.image_source = new_image_source  # Update the image source
        self.mesh.texture = self._load_texture(new_image_source)  # Update the texture
    def _format_vertices(self):
        """Convert vertices into the format required by the Mesh widget."""
        formatted = [
            self.vertices[0], self.vertices[1], 0, 0,  # Top-left (u=0, v=0)
            self.vertices[2], self.vertices[3], 1, 0,  # Top-right (u=1, v=0)
            self.vertices[4], self.vertices[5], 1, 1,  # Bottom-right (u=1, v=1)
            self.vertices[6], self.vertices[7], 0, 1,  # Bottom-left (u=0, v=1)
        ]
        return formatted

    def _load_texture(self, source):
        """Load the texture for the image."""
        texture = CoreImage(source).texture
        print(source, texture)
        return texture

    def on_mouse_move(self, window, pos):
        """Update the top two vertices based on mouse position."""
        mouse_x, mouse_y = pos

        # Update top-left and top-right vertices
        self.vertices[0] = mouse_x - self.image_width / 2  # Top-left x
        self.vertices[1] = mouse_y + self.image_height / 2  # Top-left y
        self.vertices[2] = mouse_x + self.image_width / 2  # Top-right x
        self.vertices[3] = mouse_y + self.image_height / 2  # Top-right y
        self.vertices[4] = (window.width/1.3+self.image_width/2)+mouse_x/10
        self.vertices[6] = (window.width/1.3-self.image_width/2)+mouse_x/10
        # Update the mesh vertices
        self.mesh.vertices = self._format_vertices()

    def on_window_resize(self, instance, width, height):
        """Adjust image size and position on window resize."""
        self.image_width = width * 0.2  # Recalculate width (20% of screen width)
        self.image_height = height * 0.4  # Recalculate height (40% of screen height)

        # Recalculate the vertices
        self.vertices = [
            (width / 2) - (self.image_width / 2), height / 2 + self.image_height / 2,  # Top-left
            (width / 2) + (self.image_width / 2), height / 2 + self.image_height / 2,  # Top-right
            (width / 2) + (self.image_width / 2), height / 2 - self.image_height / 2,  # Bottom-right
            (width / 2) - (self.image_width / 2), height / 2 - self.image_height / 2   # Bottom-left
        ]

        # Update the mesh vertices
        self.mesh.vertices = self._format_vertices()

class CenteredImage(Widget):
    def __init__(self,stretchable_image, **kwargs):
        super().__init__(**kwargs)

        self.stretchable_image = stretchable_image
        
        # Access vertices from StretchableImage instance
        self.sound_condition = False
        self.slap_sound_played = False
        self.image_source = "MoldySanta.png"

        # Define the initial vertices dynamically based on screen size
        self.image_width = Window.width * 0.2  # 20% of screen width
        self.image_height = Window.height * 0.4  # 40% of screen height

        # Initial vertices
        self.vertices = [
            (Window.width / 2) - (self.image_width / 2), Window.height / 2 + self.image_height / 2,  # Top-left
            (Window.width / 2) + (self.image_width / 2), Window.height / 2 + self.image_height / 2,  # Top-right
            (Window.width / 2) + (self.image_width / 2), Window.height / 2 - self.image_height / 2,  # Bottom-right
            (Window.width / 2) - (self.image_width / 2), Window.height / 2 - self.image_height / 2   # Bottom-left
        ]
        # Define the indices for the Mesh (a rectangle made of 2 triangles)
        self.indices = [0, 1, 2, 2, 3, 0]

        # Create the mesh to render the image
        with self.canvas:
            self.mesh = Mesh(
                vertices=self._format_vertices(),
                indices=self.indices,
                mode="triangle_fan",
                texture=self._load_texture(self.image_source),
            )
        # Button setup
        self.bg_chooser_button = Button(
            text="Change Background",
            size_hint=(None, None),
            size=(Window.width / 8, Window.height / 6),  # Initial button size
            font_size=Window.height / 40,  # Initial font size
            text_size = (Window.width/10,None),
            background_normal = "brick.jpeg",
            color = (0,0,0,1),
            halign="center",
            valign="middle"
        )
        self.bg_chooser_button.bind(on_press=self.bg_chooser)

        self.add_widget(self.bg_chooser_button)

        self.hand_chooser_button = Button(
            background_normal = "hand.png",

            text="Change Hand",
            size_hint=(None, None),
            size=(Window.width / 8, Window.height / 6),  # Initial button size
            font_size=Window.height / 50,  # Initial font size
            text_size = (Window.width/10,None),
            pos = (Window.width-Window.width/8,0),
                        color = (0,0,0,1),

            halign="center",
            valign="middle"
        )
        self.hand_chooser_button.bind(on_press=self.hand_chooser)

        self.add_widget(self.hand_chooser_button)

        self.face_chooser_button = Button(
            background_normal = "MoldySanta.png",

            text="Change Face",
            size_hint=(None, None),
            size=(Window.width / 8, Window.height / 6),  # Initial button size
            font_size=Window.height / 40,  # Initial font size
            pos = (Window.width-Window.width/8,Window.height-Window.height/6),
            color = (0,0,0,1),
            halign="center",
            valign="middle"
        )
        self.face_chooser_button.bind(on_press=self.face_chooser)

        self.add_widget(self.face_chooser_button)
        # Bind mouse motion and window resizing
        Window.bind(mouse_pos=self.on_mouse_move)
        Window.bind(on_resize=self.on_window_resize)
    def bg_chooser(self, instance):
        if menu_sound:
                menu_sound.volume = 0.5
                menu_sound.play()

        self.parent.manager.current = "background_chooser_screen"
    def hand_chooser(self,instance):
        if menu_sound:
                menu_sound.volume = 0.5
                menu_sound.play()

        self.parent.manager.current = "hand_chooser_screen"
    def face_chooser(self,instance):
        if menu_sound:
                menu_sound.volume = 0.5
                menu_sound.play()

        self.parent.manager.current = "Face_Chooser_Screen"
    def update_mesh_texture(self, new_image_source):
        """Update the texture of the mesh."""
        self.image_source = new_image_source  # Update the image source
        self.mesh.texture = self._load_texture(new_image_source)  # Update the texture
    def _format_vertices(self):
        """Convert vertices into the format required by the Mesh widget."""
        formatted = [
            self.vertices[0], self.vertices[1], 0, 0,  # Top-left (u=0, v=0)
            self.vertices[2], self.vertices[3], 1, 0,  # Top-right (u=1, v=0)
            self.vertices[4], self.vertices[5], 1, 1,  # Bottom-right (u=1, v=1)
            self.vertices[6], self.vertices[7], 0, 1,  # Bottom-left (u=0, v=1)
        ]
        self.perm_vert0 = self.vertices[0]
        self.perm_vert4 = self.vertices[4]
        return formatted

    def _load_texture(self, source):
        """Load the texture for the image."""
        texture = CoreImage(source).texture
        return texture

    def on_mouse_move(self, window, pos):
        self.x_vertices = self.stretchable_image.vertices[0:8]  # Top-left vertex (x, y)

        """Update the top two vertices based on mouse position."""
        mouse_x, mouse_y = pos
        if ((Window.width / 2) - (self.image_width / 2))+10>=self.x_vertices[0]:
        # Update top-left and top-right vertices
            self.vertices[0] = mouse_x - self.image_width / 2  # Top-left x
            self.vertices[4] = (window.width/2+self.image_width/2)+mouse_x/10
            self.sound_condition  = True            # Update the mesh vertices
            self.play_sound()
            

        elif ((Window.width / 2) - (self.image_width / 2))<=self.x_vertices[0]:
            self.vertices[0] = (Window.width / 2) - (self.image_width / 2)
            self.vertices[4] = (Window.width / 2) + (self.image_width / 2)
            self.sound_condition = False
            self.slap_sound_played =False

        self.mesh.vertices = self._format_vertices()
        if ((Window.width / 2) - (self.image_width / 2))+10>=self.x_vertices[0] and self.x_vertices[1]>=(Window.height / 2 - self.image_height / 2)and self.x_vertices[1]<=(Window.height / 2 + self.image_height / 2):
            self.vertices[1] = self.x_vertices[1]
            self.vertices[3] = self.x_vertices[1]
        elif ((Window.width / 2) - (self.image_width / 2))+10<=self.x_vertices[0] or self.x_vertices[1]<=(Window.height / 2 - self.image_height / 2) or self.x_vertices[1]>=(Window.height / 2 + self.image_height / 2):
            self.vertices[1] = Window.height / 2 + self.image_height / 2
            self.vertices[3] = Window.height / 2 + self.image_height / 2


    def play_sound(self):
        if self.sound_condition and not self.slap_sound_played:

            if slap_sound:
                slap_sound.volume=0.5
                slap_sound.play()
            self.slap_sound_played = True
        
    def on_window_resize(self, instance, width, height):

        """Adjust image size and position on window resize."""
        self.image_width = width * 0.2  # Recalculate width (20% of screen width)
        self.image_height = height * 0.4  # Recalculate height (40% of screen height)
        # Recalculate the vertices
        self.vertices = [
            (width / 2) - (self.image_width / 2), height / 2 + self.image_height / 2,  # Top-left
            (width / 2) + (self.image_width / 2), height / 2 + self.image_height / 2,  # Top-right
            (width / 2) + (self.image_width / 2), height / 2 - self.image_height / 2,  # Bottom-right
            (width / 2) - (self.image_width / 2), height / 2 - self.image_height / 2   # Bottom-left
        ]

        # Update the mesh vertices
        self.mesh.vertices = self._format_vertices()
        # Update background size

        self.hand_chooser_button.size = (width/8, height/6)
        self.hand_chooser_button.font_size = 12
        self.hand_chooser_button.pos = (Window.width-Window.width/8,0)
        # Update button size and position
        self.bg_chooser_button.size = (width / 8, height / 6)  # Dynamically adjust size
        self.bg_chooser_button.font_size = 12  # Dynamically adjust font size
        


# CombinedScreen with StretchableImage and CenteredImage
class CombinedScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg_image = "brickw.jpeg"
        self.bg_width = Window.width
        self.bg_height = Window.height
        with self.canvas:
            self.bg_rect = Rectangle(source=self.bg_image, size=(self.bg_width, self.bg_height))
        
        # Create StretchableImage instance
        self.stretchable_image = StretchableImage()

        # Create CenteredImage instance, passing StretchableImage
        self.centered_image = CenteredImage(self.stretchable_image)
        # Add CenteredImage first so it is rendered below
        self.add_widget(self.centered_image)
        Window.bind(on_resize=self.on_window_resize)

        # Add StretchableImage on top
        self.add_widget(self.stretchable_image)
    def update_image(self, new_image_source):
        """Update the image with the new file."""
        self.bg_image = new_image_source
        self.bg_rect.source = self.bg_image  # Update the Rectangle texture
        if menu_sound:
                menu_sound.volume = 0.5
                menu_sound.stop()  
    def update_image2(self, new_image_source):
        """Update the image with the new file."""
        if menu_sound:
                menu_sound.volume = 0.5
                menu_sound.stop()
        self.stretchable_image.update_mesh_texture(new_image_source)
    def update_face(self,new_image_source):
        if menu_sound:
                menu_sound.volume = 0.5
                menu_sound.stop()
        self.centered_image.update_mesh_texture(new_image_source)
    
            
 




    def on_window_resize(self, instance, width, height):
        """Update background size dynamically on window resize."""
        self.bg_width = width
        self.bg_height = height
        self.bg_rect.size = (self.bg_width, self.bg_height)
        self.bg_rect.pos = (0, 0)  
class bg_choose_scrn(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create a BoxLayout
        layout = BoxLayout(orientation="horizontal", size_hint = (1,0.25),pos_hint={"x": 0, "y": 0.35})
        
        # Add buttons to the BoxLayout
        bg_button1 = Button(background_normal = "bg5.jpeg")
        bg_button2 = Button(background_normal = "bg4.jpeg")
        bg_button3 = Button(background_normal ="blackbg.jpeg")
        bg_button4 = Button(background_normal ="brickw.jpeg")
        bg_button5 = Button(background_normal ="brick.jpeg")
        bg_button6 = Button(text = "Custom Bg",background_normal ="custombg.jpeg")
        layout.add_widget(bg_button1)
        layout.add_widget(bg_button2)
        layout.add_widget(bg_button3)
        layout.add_widget(bg_button4)
        layout.add_widget(bg_button5)
        layout.add_widget(bg_button6)
        bg_button6.bind(on_press=self.main_menue)
        bg_button1.bind(on_press=self.bg_changer1)
        bg_button2.bind(on_press=self.bg_changer2)
        bg_button3.bind(on_press=self.bg_changer3)
        bg_button4.bind(on_press=self.bg_changer4)
        bg_button5.bind(on_press=self.bg_changer5)


        # Add the BoxLayout to the Screen
        self.add_widget(layout)

    def main_menue(self,instance):
        self.manager.current="File_Scrn"
    def bg_changer1(self,image_file,*args):
        self.manager.get_screen("combined_screen").update_image("bg5.jpeg")
        self.manager.current="combined_screen"
    def bg_changer2(self,image_file,*args):
        self.manager.get_screen("combined_screen").update_image("bg4.jpeg")
        self.manager.current="combined_screen"
    def bg_changer3(self,image_file,*args):
        self.manager.get_screen("combined_screen").update_image("blackbg.jpeg")
        self.manager.current="combined_screen"
    def bg_changer4(self,image_file,*args):
        self.manager.get_screen("combined_screen").update_image("brickw.jpeg")
        self.manager.current="combined_screen"
    def bg_changer5(self,image_file,*args):
        self.manager.get_screen("combined_screen").update_image("brick.jpeg")
        self.manager.current="combined_screen"
class hand_choose_scrn(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="horizontal", size_hint = (1,0.25),pos_hint={"x": 0, "y": 0.35})
        
        # Add buttons to the BoxLayout
        bg_button1 = Button(background_normal = "glue_hand.png")
        bg_button2 = Button(background_normal = "mult_hand.png")
        bg_button3 = Button(background_normal ="red_hand.png")
        bg_button4 = Button(background_normal ="plastic_hand.png")
        bg_button5 = Button(background_normal ="hand.png")
        bg_button6 = Button(text = "Custom Hand",background_normal ="custombg.jpeg")
        layout.add_widget(bg_button1)
        layout.add_widget(bg_button2)
        layout.add_widget(bg_button3)
        layout.add_widget(bg_button4)
        layout.add_widget(bg_button5)
        layout.add_widget(bg_button6)
        bg_button6.bind(on_press=self.main_menue)
        bg_button1.bind(on_press=self.bg_changer1)
        bg_button2.bind(on_press=self.bg_changer2)
        bg_button3.bind(on_press=self.bg_changer3)
        bg_button4.bind(on_press=self.bg_changer4)
        bg_button5.bind(on_press=self.bg_changer5)


        # Add the BoxLayout to the Screen
        self.add_widget(layout)

    def main_menue(self,instance):
        self.manager.current="File_Scrn2"
    def bg_changer1(self,image_file,*args):
        self.manager.get_screen("combined_screen").update_image2("glue_hand.png")
        self.manager.current="combined_screen"
    def bg_changer2(self,image_file,*args):
        self.manager.get_screen("combined_screen").update_image2("mult_hand.png")
        self.manager.current="combined_screen"
    def bg_changer3(self,image_file,*args):
        self.manager.get_screen("combined_screen").update_image2("red_hand.png")
        self.manager.current="combined_screen"
    def bg_changer4(self,image_file,*args):
        self.manager.get_screen("combined_screen").update_image2("plastic_hand.png")
        self.manager.current="combined_screen"
    def bg_changer5(self,image_file,*args):
        self.manager.get_screen("combined_screen").update_image2("hand.png")
        self.manager.current="combined_screen"

class Face_Chooser_Screen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Main layout
        layout = BoxLayout(orientation="vertical")

        # FileChooser for selecting image files
        self.filechooser = FileChooserListView(filters=["*.png", "*.jpg", "*.jpeg"])
        layout.add_widget(self.filechooser)

        # Buttons for confirming or canceling selection
        button_layout = BoxLayout(size_hint=(1, 0.1))
        select_button = Button(text="Select Image")
        select_button.bind(on_press=self.select_image)
        cancel_button = Button(text="Cancel")
        cancel_button.bind(on_press=self.cancel_selection)
        button_layout.add_widget(select_button)
        button_layout.add_widget(cancel_button)

        layout.add_widget(button_layout)
        self.add_widget(layout)
    def select_image(self, instance):
        """Handle image selection and return to the main screen."""
        selected = self.filechooser.selection
        if selected:
            self.manager.get_screen("combined_screen").update_face(selected[0])
        self.manager.current = "combined_screen"

    def cancel_selection(self, instance):
        """Return to the main screen without selecting an image."""
        self.manager.current = "combined_screen"


class File_Choose_Scrn2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Main layout
        layout = BoxLayout(orientation="vertical")

        # FileChooser for selecting image files
        self.filechooser = FileChooserListView(filters=["*.png", "*.jpg", "*.jpeg"])
        layout.add_widget(self.filechooser)

        # Buttons for confirming or canceling selection
        button_layout = BoxLayout(size_hint=(1, 0.1))
        select_button = Button(text="Select Image")
        select_button.bind(on_press=self.select_image)
        cancel_button = Button(text="Cancel")
        cancel_button.bind(on_press=self.cancel_selection)
        button_layout.add_widget(select_button)
        button_layout.add_widget(cancel_button)

        layout.add_widget(button_layout)
        self.add_widget(layout)
    def select_image(self, instance):
        """Handle image selection and return to the main screen."""
        selected = self.filechooser.selection
        if selected:
            self.manager.get_screen("combined_screen").update_image2(selected[0])
        self.manager.current = "combined_screen"

    def cancel_selection(self, instance):
        """Return to the main screen without selecting an image."""
        self.manager.current = "combined_screen"
# Another Screen for Example
class File_Choose_Scrn(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Main layout
        layout = BoxLayout(orientation="vertical")

        # FileChooser for selecting image files
        self.filechooser = FileChooserListView(filters=["*.png", "*.jpg", "*.jpeg"])
        layout.add_widget(self.filechooser)

        # Buttons for confirming or canceling selection
        button_layout = BoxLayout(size_hint=(1, 0.1))
        select_button = Button(text="Select Image")
        select_button.bind(on_press=self.select_image)
        cancel_button = Button(text="Cancel")
        cancel_button.bind(on_press=self.cancel_selection)
        button_layout.add_widget(select_button)
        button_layout.add_widget(cancel_button)

        layout.add_widget(button_layout)
        self.add_widget(layout)
    def select_image(self, instance):
        """Handle image selection and return to the main screen."""
        selected = self.filechooser.selection
        if selected:
            self.manager.get_screen("combined_screen").update_image(selected[0])
        self.manager.current = "combined_screen"

    def cancel_selection(self, instance):
        """Return to the main screen without selecting an image."""
        self.manager.current = "combined_screen"

# Main App with ScreenManager
class DynamicImageApp(App):
    def build(self):
        sm = ScreenManager()

        # Add CombinedScreen
        sm.add_widget(CombinedScreen(name="combined_screen"))

        # Add ExampleScreen
        sm.add_widget(File_Choose_Scrn(name="File_Scrn"))
        sm.add_widget(bg_choose_scrn(name = "background_chooser_screen"))
        sm.add_widget(hand_choose_scrn(name = "hand_chooser_screen"))
        sm.add_widget(File_Choose_Scrn2(name = "File_Scrn2"))
        sm.add_widget(Face_Chooser_Screen(name = "Face_Chooser_Screen"))
        # Set the initial screen

        sm.current = "combined_screen"

        return sm


if __name__ == "__main__":
    DynamicImageApp().run()

