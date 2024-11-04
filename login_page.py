from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage

import pyttsx3

import useful_methods




class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("735x470")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)

        self.output_path = Path(__file__).parent
        self.assets_path = self.output_path / "assets" / "frame0"

        self.setup_ui()
        self.engine = pyttsx3.init()  # Initialize the TTS engine

    def relative_to_assets(self, path: str) -> Path:
        return self.assets_path / Path(path)

    def setup_ui(self):
        # Create Canvas
        self.canvas = Canvas(
            self.root,
            bg="#FFFFFF",
            height=470,
            width=735,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Load images and create canvas items
        self.create_images()
        self.create_text()
        self.create_entries()
        self.create_button()

    def create_images(self):
        # Displaying images on canvas
        self.image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.canvas.create_image(367.0, 235.0, image=self.image_image_1)

        self.image_image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.canvas.create_image(363.0, 229.0, image=self.image_image_2)

        self.image_image_3 = PhotoImage(file=self.relative_to_assets("image_3.png"))
        self.canvas.create_image(368.0, 235.0, image=self.image_image_3)

        self.image_image_4 = PhotoImage(file=self.relative_to_assets("image_4.png"))
        self.canvas.create_image(653.0, 420.0, image=self.image_image_4)

    def create_text(self):
        # Adding text to canvas
        self.canvas.create_text(
            192.0, 64.0, anchor="nw", text="Log in", fill="#FFFFFF", font=("Montserrat Regular", 40 * -1)
        )
        self.canvas.create_text(
            192.0, 123.0, anchor="nw", text="Productivity starts here", fill="#FFFFFF",
            font=("Montserrat Regular", 24 * -1)
        )
        self.canvas.create_text(
            192.0, 171.0, anchor="nw", text="Username", fill="#FFFFFF", font=("Montserrat Regular", 12 * -1)
        )
        self.canvas.create_text(
            192.0, 261.0, anchor="nw", text="Password", fill="#FFFFFF", font=("Montserrat Regular", 12 * -1)
        )

    def create_entries(self):
        # Username Entry
        self.entry_image_1 = PhotoImage(file=self.relative_to_assets("entry_1.png"))
        self.canvas.create_image(367.5, 211.0, image=self.entry_image_1)
        self.entry_1 = Entry(bd=0, bg="#8E84B7", fg="#000716", highlightthickness=0)
        self.entry_1.place(x=197.0, y=192.0, width=341.0, height=36.0)

        # Password Entry
        self.entry_image_2 = PhotoImage(file=self.relative_to_assets("entry_2.png"))
        self.canvas.create_image(367.5, 301.0, image=self.entry_image_2)
        self.entry_2 = Entry(bd=0, bg="#8E84B7", fg="#000716", highlightthickness=0)
        self.entry_2.place(x=197.0, y=282.0, width=341.0, height=36.0)

    def create_button(self):
        # Button with hover effect
        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_image_hover_1 = PhotoImage(file=self.relative_to_assets("button_hover_1.png"))

        self.button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.on_button_click,
            relief="flat"
        )
        self.button_1.place(x=260.0, y=338.0, width=215.0, height=59.0)

        # Hover binding
        self.button_1.bind('<Enter>', self.on_button_hover)
        self.button_1.bind('<Leave>', self.on_button_leave)

    def on_button_click(self):
        useful_methods.speak_text("Logging in...")

    def on_button_hover(self, event):
        self.button_1.config(image=self.button_image_hover_1)

    def on_button_leave(self, event):
        self.button_1.config(image=self.button_image_1)


# Run the app
if __name__ == "__main__":
    root = Tk()
    app = LoginApp(root)
    root.mainloop()




