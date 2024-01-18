import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog, simpledialog, StringVar, IntVar
import threading
import subprocess
import importlib
from utils import scan_directory_for_images, open_ignore_file, write_ignore_file, list_modules_in_package

list_of_game_codes = list_modules_in_package('game_texture_code')

class TextureProcessingApp:
    # Function to append log messages to the ScrolledText widget

    def __init__(self, root):
        self.root = root
        self.root.title("Texture Processing Tool")

        # Initialize StringVar objects for path inputs
        self.upscale_metadata_path_var = StringVar()
        self.texture_dump_path_var = StringVar()
        self.texture_load_path_var = StringVar()
        self.real_esrgan_path_var = StringVar()

        # Set up the GUI components
        self.setup_path_input("Upscale Metadata Path:", self.upscale_metadata_path_var, is_directory=True)
        self.setup_path_input("Texture Dump Path:", self.texture_dump_path_var, is_directory=True)
        self.setup_path_input("Texture Load Path:", self.texture_load_path_var, is_directory=True)
        self.setup_path_input("Real-ESRGAN Executable Path:", self.real_esrgan_path_var, is_directory=False)

        # OptionMenu for texture filter code
        self.setup_texture_filter_code_menu()

        self.start_processing_button = tk.Button(root, text="Start Processing", command=self.process_textures)
        self.start_processing_button.pack(pady=10)


        self.stop_button = tk.Button(root, text="Stop", command=self.stop_task)
        self.stop_button.pack(pady=5)

        self.task_running = False


        self.log = scrolledtext.ScrolledText(root, state='disabled', height=10)
        self.log.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def stop_task(self):
        self.task_running = False

    def update_log(self, message):
        """Append a message to the log widget and keep only the last 1000 lines."""
        self.log.configure(state='normal')  # Enable editing of the widget

        # Append the message
        self.log.insert(tk.END, message + '\n')

        # Check if the line count exceeds 1000, and if so, trim the oldest lines
        lines = self.log.get('1.0', tk.END).splitlines()
        if len(lines) > 1000:
            self.log.delete('1.0', f'{len(lines)-1000 + 1}.0')

        self.log.configure(state='disabled')  # Disable editing of the widget
        self.log.yview(tk.END)  # Scroll to the end

    def setup_path_input(self, label_text, string_var, is_directory):
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=5)

        label = tk.Label(frame, text=label_text)
        label.pack(side=tk.LEFT)

        entry = tk.Entry(frame, textvariable=string_var, width=50)
        entry.pack(side=tk.LEFT)

        def browse():
            if is_directory:
                path = filedialog.askdirectory()
            else:
                path = filedialog.askopenfilename()
            if path:
                string_var.set(path)

        button = tk.Button(frame, text="Browse", command=browse)
        button.pack(side=tk.LEFT)

    def setup_texture_filter_code_menu(self):
        self.texture_filter_codes = list_of_game_codes
        self.texture_filter_code_var = StringVar(value=self.texture_filter_codes[0])
        texture_filter_code_menu = tk.OptionMenu(self.root, self.texture_filter_code_var, *self.texture_filter_codes)
        texture_filter_code_menu.pack(pady=10)

    def process_textures(self):
        # Retrieve the paths and selected texture filter code
        upscale_metadata_path = self.upscale_metadata_path_var.get()
        texture_dump_path = self.texture_dump_path_var.get()
        texture_load_path = self.texture_load_path_var.get()
        real_esrgan_path = self.real_esrgan_path_var.get()
        texture_filter_code = self.texture_filter_code_var.get()
        module = importlib.import_module(texture_filter_code)
        # Retrieve the desired function from the imported module
        check_texture = getattr(module, 'check_texture')
        self.task_running = True
        def background_task():
            while self.task_running:
                try:
                    # Dynamically import the module based on user input
                    module = importlib.import_module(texture_filter_code)
                    check_texture = getattr(module, 'check_texture')

                    files_to_ignore = open_ignore_file(f"{upscale_metadata_path}/ignore.json")
                    texture_files = scan_directory_for_images(texture_dump_path)
                    upscaled_files = scan_directory_for_images(texture_load_path)

                    textures_to_process = [f for f in texture_files if f not in upscaled_files and f not in files_to_ignore]
                    self.update_log("*" * 80)
                    self.update_log(f'Textures to process: {len(textures_to_process)}')

                    for i, texture_path in enumerate(textures_to_process, start=1):
                        if self.task_running == False:
                            break
                        self.update_log(f'Processing {i}/{len(textures_to_process)}: {texture_path}')
                        process = check_texture(texture_path)

                        if process is False:
                            self.update_log(f"Ignoring: {texture_path}")
                            files_to_ignore.add(texture_path)

                        if process == True:
                            output_path = texture_path.replace(texture_dump_path, texture_load_path)
                            command = [
                                real_esrgan_path,
                                '-i', texture_path,
                                '-s', '3',
                                '-o', output_path,
                                "j", "4:4:4"
                            ]
                            subprocess.call(command)
                            self.update_log(f"Completed: {texture_path}")

                    write_ignore_file(f"{upscale_metadata_path}/ignore.json", files_to_ignore)
                    self.root.after(0, messagebox.showinfo, "Process Complete", "All found textures have been processed(or you pressed stop).")
                except Exception as e:
                    self.root.after(0, messagebox.showerror, "Error", str(e))

        # Run the background task in a separate thread
        thread = threading.Thread(target=background_task)
        thread.start()

    def run(self):
        self.root.mainloop()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = TextureProcessingApp(root)
    app.run()
