import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os
import threading


class ASCIIArtGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Luxury ASCII Art Generator")
        self.root.geometry("800x600")
        self.root.configure(bg="#1a1a1a")

        # Luxury UI Styling
        self.font_title = ("Helvetica", 24, "bold")
        self.font_button = ("Helvetica", 12)
        self.bg_color = "#1a1a1a"
        self.fg_color = "#ffffff"
        self.accent_color = "#d4a373"
        self.button_style = {
            "bg": self.accent_color,
            "fg": self.bg_color,
            "font": self.font_button,
            "activebackground": "#b38b5a",
            "relief": "flat",
            "cursor": "hand2"
        }

        self.setup_ui()
        self.ascii_chars = "Hesam "

    def setup_ui(self):
        # Title
        title_label = tk.Label(
            self.root,
            text="ASCII Art Generator",
            font=self.font_title,
            bg=self.bg_color,
            fg=self.accent_color
        )
        title_label.pack(pady=20)

        # Image Selection
        self.image_path_var = tk.StringVar()
        image_frame = tk.Frame(self.root, bg=self.bg_color)
        image_frame.pack(pady=10, fill="x", padx=20)
        tk.Entry(
            image_frame,
            textvariable=self.image_path_var,
            font=self.font_button,
            bg="#2c2c2c",
            fg=self.fg_color,
            insertbackground=self.fg_color,
            relief="flat"
        ).pack(side="left", fill="x", expand=True, padx=5)
        tk.Button(
            image_frame,
            text="Browse",
            command=self.browse_image,
            **self.button_style
        ).pack(side="right")

        # Width Entry
        width_frame = tk.Frame(self.root, bg=self.bg_color)
        width_frame.pack(pady=10)
        tk.Label(
            width_frame,
            text="Width (chars):",
            font=self.font_button,
            bg=self.bg_color,
            fg=self.fg_color
        ).pack(side="left")
        self.width_var = tk.StringVar(value="80")
        tk.Entry(
            width_frame,
            textvariable=self.width_var,
            width=10,
            font=self.font_button,
            bg="#2c2c2c",
            fg=self.fg_color,
            insertbackground=self.fg_color,
            relief="flat"
        ).pack(side="left", padx=5)

        # Generate Button
        tk.Button(
            self.root,
            text="Generate ASCII Art",
            command=self.start_generation,
            **self.button_style
        ).pack(pady=20)

        # Output Text Area
        self.output_text = tk.Text(
            self.root,
            height=15,
            font=("Courier", 10),
            bg="#2c2c2c",
            fg=self.fg_color,
            relief="flat",
            wrap="none"
        )
        self.output_text.pack(pady=10, padx=20, fill="both", expand=True)

        # Save Button
        tk.Button(
            self.root,
            text="Save ASCII Art",
            command=self.save_ascii,
            **self.button_style
        ).pack(pady=10)

        # Progress Label
        self.progress_var = tk.StringVar(value="")
        tk.Label(
            self.root,
            textvariable=self.progress_var,
            font=self.font_button,
            bg=self.bg_color,
            fg=self.accent_color
        ).pack(pady=5)

    def browse_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if file_path:
            self.image_path_var.set(file_path)

    def start_generation(self):
        image_path = self.image_path_var.get()
        try:
            width = int(self.width_var.get())
            if width <= 0:
                raise ValueError("Width must be positive")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid width")
            return

        if not image_path or not os.path.exists(image_path):
            messagebox.showerror("Error", "Please select a valid image")
            return

        self.output_text.delete(1.0, tk.END)
        self.progress_var.set("Generating...")
        self.root.config(cursor="wait")
        threading.Thread(target=self.generate_ascii, args=(image_path, width), daemon=True).start()

    def generate_ascii(self, image_path, width):
        try:
            img = Image.open(image_path).convert("L")
            aspect_ratio = img.height / img.width
            height = int(width * aspect_ratio * 0.55)  # Adjust for character aspect ratio
            img = img.resize((width, height), Image.LANCZOS) # type: ignore

            pixels = img.getdata()
            ascii_art = ""
            for i, pixel in enumerate(pixels):
                ascii_art += self.ascii_chars[pixel // (256 // len(self.ascii_chars))]
                if (i + 1) % width == 0:
                    ascii_art += "\n"

            self.root.after(0, self.update_output, ascii_art)
        except Exception as e:
            self.root.after(0, self.show_error, str(e))
        finally:
            self.root.after(0, self.reset_progress)

    def update_output(self, ascii_art):
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, ascii_art)
        self.progress_var.set("Generation Complete!")

    def show_error(self, error):
        messagebox.showerror("Error", f"Failed to generate ASCII art: {error}")
        self.progress_var.set("")

    def reset_progress(self):
        self.root.config(cursor="")
        if self.progress_var.get() != "Generation Complete!":
            self.progress_var.set("")

    def save_ascii(self):
        ascii_text = self.output_text.get(1.0, tk.END).strip()
        if not ascii_text:
            messagebox.showwarning("Warning", "No ASCII art to save")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")]
        )
        if file_path:
            try:
                with open(file_path, "w") as f:
                    f.write(ascii_text)
                messagebox.showinfo("Success", "ASCII art saved successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ASCIIArtGenerator(root)
    root.mainloop()
