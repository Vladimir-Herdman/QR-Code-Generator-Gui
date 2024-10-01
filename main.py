import qrcode
import qrcode.image.svg

from tkinter import *
from tkinter import ttk
from tkinter import colorchooser
from tkinter.filedialog import asksaveasfile

from PIL import ImageTk
from math import sqrt

class GenerateQR:
    def __init__(self, root_original):

        self.root = root_original

        self.error_correction = {
            '' : qrcode.constants.ERROR_CORRECT_M,
            
            'L': qrcode.constants.ERROR_CORRECT_L,
            'M': qrcode.constants.ERROR_CORRECT_M,
            'Q': qrcode.constants.ERROR_CORRECT_Q,
            'H': qrcode.constants.ERROR_CORRECT_H
        }

        self.create_window()
        self.temp_qrcode_placeholder()

    def create_window(self):
        """
        Create the standard window that will be used to view and interact with 
        the qrcode generator
        """
        self.root.title("QR Code Generator GUI")
        
        # make variables
        self.data = StringVar()
        self.error_correction_choice = StringVar()
        
        self.foreground_color = (0, 0, 0)
        self.foreground_R = StringVar()
        self.foreground_G = StringVar()
        self.foreground_B = StringVar()
        
        self.background_color = (255, 255, 255)
        self.background_R = StringVar()
        self.background_G = StringVar()
        self.background_B = StringVar()

        # set any variables
        self.error_correction_choice.set('M')

        self.foreground_R.set(self.foreground_color[0])
        self.foreground_G.set(self.foreground_color[1])
        self.foreground_B.set(self.foreground_color[2])
        self.background_R.set(self.background_color[0])
        self.background_G.set(self.background_color[1])
        self.background_B.set(self.background_color[2])

        # make widgets
        main_frame = ttk.Frame(self.root, padding="12 12 12 12")

        data_frame = ttk.Frame(main_frame, padding="12 12 12 12")
        data_label = ttk.Label(data_frame, text="Data to QR-Code-ify:")
        data_entry = ttk.Entry(data_frame, width=30, textvariable=self.data)
        error_correction_label = ttk.Label(data_frame, text="Set Error Correction:", padding="0 12 0 0")
        error_correction_radial_L = ttk.Radiobutton(data_frame, text="Low (7%)", value='L', variable=self.error_correction_choice)
        error_correction_radial_M = ttk.Radiobutton(data_frame, text="Medium (15%)", value='M', variable=self.error_correction_choice)
        error_correction_radial_Q = ttk.Radiobutton(data_frame, text="Quartile (25%)", value='Q', variable=self.error_correction_choice)
        error_correction_radial_H = ttk.Radiobutton(data_frame, text="High (30%)", value='H', variable=self.error_correction_choice)

        style_frame = ttk.Frame(data_frame, padding="12 12 12 12")
        foreground_label = ttk.Label(style_frame, text="Set Foreground:  ")
        foreground_R_label = ttk.Label(style_frame, text='R', padding="48 0 0 0", foreground="red")
        foreground_R_entry = ttk.Entry(style_frame, width=4, textvariable=self.foreground_R)
        foreground_G_label = ttk.Label(style_frame, text='G', padding="48 0 0 0", foreground="green")
        foreground_G_entry = ttk.Entry(style_frame, width=4, textvariable=self.foreground_G)
        foreground_B_label = ttk.Label(style_frame, text='B', padding="48 0 0 0", foreground="blue")
        foreground_B_entry = ttk.Entry(style_frame, width=4, textvariable=self.foreground_B)
        foreground_button = ttk.Button(style_frame, text="Color Chooser", width=15, command=self.f_color_chooser_func)
        self.foreground_color_show = Label(style_frame, background="black")
        background_label = ttk.Label(style_frame, text="Set Background:  ")
        background_R_label = ttk.Label(style_frame, text='R', padding="48 0 0 0", foreground="red")
        background_R_entry = ttk.Entry(style_frame, width=4, textvariable=self.background_R)
        background_G_label = ttk.Label(style_frame, text='G', padding="48 0 0 0", foreground="green")
        background_G_entry = ttk.Entry(style_frame, width=4, textvariable=self.background_G)
        background_B_label = ttk.Label(style_frame, text='B', padding="48 0 0 0", foreground="blue")
        background_B_entry = ttk.Entry(style_frame, width=4, textvariable=self.background_B)
        background_button = ttk.Button(style_frame, text="Color Chooser", width=15, command=self.b_color_chooser_func)
        self.background_color_show = Label(style_frame, background="white")

        self.qrcode_frame = ttk.Frame(main_frame, padding="12 12 12 12")

        save_gen_labelframe = ttk.LabelFrame(master=main_frame, padding="12 12 12 12")
        save_gen_frame = ttk.Frame(save_gen_labelframe, padding="12 12 12 12")
        save_button = ttk.Button(save_gen_frame, text="Save", width=15, command=self.save_button_func)

        data_right_sep = ttk.Separator(main_frame, orient=VERTICAL)
        data_bottom_sep = ttk.Separator(data_frame, orient=HORIZONTAL)

        # grid widgets
        main_frame.grid(column=0, row=0, sticky=(N, E, S, W))

        data_frame.grid(column=0, row=0, sticky=(N, E))
        data_label.grid(column=0, row=0, sticky=W)
        data_entry.grid(column=0, row=1, sticky=(E, W), padx=24)
        error_correction_label.grid(column=0, row=2, sticky=W)
        error_correction_radial_L.grid(column=0, row=3, sticky=(E, W), padx=24)
        error_correction_radial_M.grid(column=0, row=4, sticky=(E, W), padx=24)
        error_correction_radial_Q.grid(column=0, row=5, sticky=(E, W), padx=24)
        error_correction_radial_H.grid(column=0, row=6, sticky=(E, W), padx=24)

        style_frame.grid(column=0, row=8, sticky=(E, S))
        foreground_label.grid(column=0, row=0, sticky=W)
        foreground_R_label.grid(column=0, row=1, sticky=W)
        foreground_R_entry.grid(column=0, row=1, sticky=E)
        foreground_G_label.grid(column=0, row=2, sticky=W)
        foreground_G_entry.grid(column=0, row=2, sticky=E)
        foreground_B_label.grid(column=0, row=3, sticky=W)
        foreground_B_entry.grid(column=0, row=3, sticky=E)
        foreground_button.grid(column=1, row=0, sticky=W)
        self.foreground_color_show.grid(column=1, row=1, sticky=(N, E, S, W), rowspan=3)
        background_label.grid(column=0, row=4, sticky=W)
        background_R_label.grid(column=0, row=5, sticky=W)
        background_R_entry.grid(column=0, row=5, sticky=E)
        background_G_label.grid(column=0, row=6, sticky=W)
        background_G_entry.grid(column=0, row=6, sticky=E)
        background_B_label.grid(column=0, row=7, sticky=W)
        background_B_entry.grid(column=0, row=7, sticky=E)
        background_button.grid(column=1, row=4, sticky=W)
        self.background_color_show.grid(column=1, row=5, sticky=(N, E, S, W), rowspan=3)

        self.qrcode_frame.grid(column=2, row=0, rowspan=2, sticky=(N, E))

        save_gen_labelframe.grid(column=2, row=2, sticky=(S, E))
        save_gen_frame.grid(column=0, row=0, stick=(N, W, S, E))
        save_button.grid(column=0, row=1, sticky=(E, W), padx=12)

        data_right_sep.grid(column=1, row=0, sticky=(N, S), rowspan=3)
        data_bottom_sep.grid(column=0, row=7, sticky=(E, W), pady="12")

        # column/row configures
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # bindings
        foreground_G_entry.bind("<KeyRelease>", self.f_entry_change)
        foreground_R_entry.bind("<KeyRelease>", self.f_entry_change)
        foreground_B_entry.bind("<KeyRelease>", self.f_entry_change)

        background_R_entry.bind("<KeyRelease>", self.b_entry_change)
        background_G_entry.bind("<KeyRelease>", self.b_entry_change)
        background_B_entry.bind("<KeyRelease>", self.b_entry_change)

        data_entry.bind("<KeyPress>", self.generate_func)

        error_correction_radial_L.bind("<ButtonRelease-1>", self.on_radial_release)
        error_correction_radial_M.bind("<ButtonRelease-1>", self.on_radial_release)
        error_correction_radial_Q.bind("<ButtonRelease-1>", self.on_radial_release)
        error_correction_radial_H.bind("<ButtonRelease-1>", self.on_radial_release)

    def on_radial_release(self, *args):
        self.root.after(10, self.generate_func)

    def temp_qrcode_placeholder(self):
        """
        Place temporary qrcode image in place of original qrcode spot so space
        is used and rest of menu format is made consistent.  Use personal 
        LinkedIn for self promo if ever scanned
        """
        img = qrcode.make("https://www.linkedin.com/in/vladimir-herdman/")
        self.image_data = img
        img = ImageTk.PhotoImage(img)

        self.img_label = Label(self.qrcode_frame, image=img)
        self.img_label.photo = img
        self.img_label.grid(column=0, row=0, sticky=(N, W, E, S))

    def f_color_chooser_func(self, *args):
        color_code = colorchooser.askcolor(title ="Choose color")
        self.foreground_color = color_code[0]

        self.foreground_R.set(self.foreground_color[0])
        self.foreground_G.set(self.foreground_color[1])
        self.foreground_B.set(self.foreground_color[2])

        self.f_entry_change()
        self.generate_func()

    def f_entry_change(self, *args):
        if self.foreground_R.get() != "":
            red_F = int(self.foreground_R.get())
        else:
            red_F = 0
        if self.foreground_G.get() != "":
            green_F = int(self.foreground_G.get())
        else:
            green_F = 0
        if self.foreground_B.get() != "":
            blue_F = int(self.foreground_B.get())
        else:
            blue_F = 0

        red_F = max(0, min(red_F, 255))
        green_F = max(0, min(green_F, 255))
        blue_F = max(0, min(blue_F, 255))

        red_F = f"{red_F:#0{4}x}".split('x')[1]
        green_F = f"{green_F:#0{4}x}".split('x')[1]
        blue_F = f"{blue_F:#0{4}x}".split('x')[1]
        foreground_color_hex = "#" + red_F + green_F + blue_F

        self.foreground_color_show.configure(background=foreground_color_hex)

        self.generate_func()

    def b_color_chooser_func(self, *args):
        color_code = colorchooser.askcolor(title ="Choose color") 
        self.background_color = color_code[0]

        self.background_R.set(self.background_color[0])
        self.background_G.set(self.background_color[1])
        self.background_B.set(self.background_color[2])

        self.b_entry_change()
        self.generate_func()

    def b_entry_change(self, *args):
        if self.background_R.get() != "":
            red_B = int(self.background_R.get())
        else:
            red_B = 0
        if self.background_G.get() != "":
            green_B = int(self.background_G.get())
        else:
            green_B = 0
        if self.background_B.get() != "":
            blue_B = int(self.background_B.get())
        else:
            blue_B = 0

        red_B = max(0, min(red_B, 255))
        green_B = max(0, min(green_B, 255))
        blue_B = max(0, min(blue_B, 255))   

        red_B = f"{red_B:#0{4}x}".split('x')[1]
        green_B = f"{green_B:#0{4}x}".split('x')[1]
        blue_B = f"{blue_B:#0{4}x}".split('x')[1]
        background_color_hex = "#" + red_B + green_B + blue_B

        self.background_color_show.configure(background=background_color_hex)

        self.generate_func()
    
    def save_button_func(self, *args):
        """
        Save the qrcode image to a folder/directory user chooses.  Allow file 
        creation of png or svg
        """
        path_to_png = asksaveasfile(initialfile = "qrcode.png", defaultextension=".png", filetypes=[("PNG Files", "*.png"), ("SVG Files", "*.svg")])
        if path_to_png:
            path_to_png = path_to_png.name

            try:
                file_type = path_to_png.split(".")[1]
            except Exception:
                raise Exception("filetype split failure")

            if file_type == "png":  # save image, already png
                self.image_data.save(path_to_png)
            elif file_type == "svg": # recreate image as svg, and then save
                qr = qrcode.QRCode(
                version=None,
                image_factory=qrcode.image.svg.SvgPathImage,
                error_correction=self.error_correction[self.error_correction_choice.get()],
                box_size=10,
                border=4,
                )

                qr.add_data(self.data.get())
                qr.make(fit=True)

                if self.foreground_R.get() != "":
                    red_F = int(self.foreground_R.get())
                else:
                    red_F = 0
                if self.foreground_G.get() != "":
                    green_F = int(self.foreground_G.get())
                else:
                    green_F = 0
                if self.foreground_B.get() != "":
                    blue_F = int(self.foreground_B.get())
                else:
                    blue_F = 0
                red_F = max(0, min(red_F, 255))
                green_F = max(0, min(green_F, 255))
                blue_F = max(0, min(blue_F, 255))  
                red_F = f"{red_F:#0{4}x}".split('x')[1]
                green_F = f"{green_F:#0{4}x}".split('x')[1]
                blue_F = f"{blue_F:#0{4}x}".split('x')[1]
                foreground_color_hex = "#" + red_F + green_F + blue_F

                if self.background_R.get() != "":
                    red_B = int(self.background_R.get())
                else:
                    red_B = 0
                if self.background_G.get() != "":
                    green_B = int(self.background_G.get())
                else:
                    green_B = 0
                if self.background_B.get() != "":
                    blue_B = int(self.background_B.get())
                else:
                    blue_B = 0
                red_B = max(0, min(red_B, 255))
                green_B = max(0, min(green_B, 255))
                blue_B = max(0, min(blue_B, 255))  
                red_B = f"{red_B:#0{4}x}".split('x')[1]
                green_B = f"{green_B:#0{4}x}".split('x')[1]
                blue_B = f"{blue_B:#0{4}x}".split('x')[1]
                background_color_hex = "#" + red_B + green_B + blue_B

                img = qr.make_image(fill_color=foreground_color_hex, back_color=background_color_hex)

                img.save(path_to_png)


    def generate_func(self, *args):
        """
        Generate the qrcode image and show to screen in qrcode_frame
        """
        qr = qrcode.QRCode(
        version=None,
        error_correction=self.error_correction[self.error_correction_choice.get()],
        box_size=10,
        border=4,
        )
        qr.add_data(self.data.get())
        qr.make(fit=True)

        if self.foreground_R.get() != "":
            red_F = int(self.foreground_R.get())
        else:
            red_F = 0
        if self.foreground_G.get() != "":
            green_F = int(self.foreground_G.get())
        else:
            green_F = 0
        if self.foreground_B.get() != "":
            blue_F = int(self.foreground_B.get())
        else:
            blue_F = 0
        red_F = max(0, min(red_F, 255))
        green_F = max(0, min(green_F, 255))
        blue_F = max(0, min(blue_F, 255))  
        self.foreground_color = (red_F, green_F, blue_F)

        if self.background_R.get() != "":
            red_B = int(self.background_R.get())
        else:
            red_B = 0
        if self.background_G.get() != "":
            green_B = int(self.background_G.get())
        else:
            green_B = 0
        if self.background_B.get() != "":
            blue_B = int(self.background_B.get())
        else:
            blue_B = 0
        red_B = max(0, min(red_B, 255))
        green_B = max(0, min(green_B, 255))
        blue_B = max(0, min(blue_B, 255))  
        self.background_color = (red_B, green_B, blue_B)

        img = qr.make_image(fill_color=self.foreground_color, back_color=self.background_color)

        self.image_data = img
        img = ImageTk.PhotoImage(img)  # qrcode.image.pil.PilImage object
        self.img_label.configure(image=img)
        self.img_label.photo = img


if __name__ == "__main__":
    root = Tk()
    GenerateQR(root)
    root.mainloop()