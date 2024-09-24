import qrcode
import qrcode.image.svg

from tkinter import *
from tkinter import ttk
from tkinter.filedialog import asksaveasfile

from PIL import ImageTk

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
        self.foreground_color = StringVar()
        self.background_color = StringVar()

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

        style_frame = ttk.Frame(main_frame, padding="12 12 12 12")

        self.qrcode_frame = ttk.Frame(main_frame, padding="12 12 12 12")

        save_gen_labelframe = ttk.LabelFrame(master=main_frame, padding="12 12 12 12")
        save_gen_frame = ttk.Frame(save_gen_labelframe, padding="12 12 12 12")
        save_button = ttk.Button(save_gen_frame, text="Save", width=15, command=self.save_button_func)
        generate_button = ttk.Button(save_gen_frame, text="Generate", width=15, command=self.generate_button_func)

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

        style_frame.grid(column=0, row=1, sticky=(E, S))

        self.qrcode_frame.grid(column=2, row=0, rowspan=2, sticky=(N, E))

        save_gen_labelframe.grid(column=2, row=2, sticky=(S, E))
        save_gen_frame.grid(column=0, row=0, stick=(N, W, S, E))
        save_button.grid(column=0, row=1, sticky=(E, W), padx=12)
        generate_button.grid(column=0, row=2, sticky=(E, W), padx=12)

        data_right_sep.grid(column=1, row=0, sticky=(N, S), rowspan=3)
        data_bottom_sep.grid(column=0, row=7, sticky=(E, W), pady="12")

        # column/row configures
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)

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

    def save_button_func(self, *args):
        """
        Save the qrcode image to a folder/directory user chooses
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
                image_factory=qrcode.image.svg.SvgImage,
                error_correction=self.error_correction[self.error_correction_choice.get()],
                box_size=10,
                border=4,
                )

                qr.add_data(self.data.get())
                qr.make(fit=True)

                if self.background_color.get().replace(" ", "") != "" and self.foreground_color.get().replace(" ", "") != "":
                    img = qr.make_image(fill_color=self.foreground_color.get(), back_color=self.background_color.get())
                else:
                    img = qr.make_image(fill_color="black", back_color="white")

                img.save(path_to_png)


    def generate_button_func(self, *args):
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

        if self.background_color.get().replace(" ", "") != "" and self.foreground_color.get().replace(" ", "") != "":
            img = qr.make_image(fill_color=self.foreground_color.get(), back_color=self.background_color.get())
        else:
            img = qr.make_image(fill_color="black", back_color="white")

        self.image_data = img
        img = ImageTk.PhotoImage(img)  # qrcode.image.pil.PilImage object
        self.img_label.configure(image=img)
        self.img_label.photo = img

        


if __name__ == "__main__":
    root = Tk()
    GenerateQR(root)
    root.mainloop()