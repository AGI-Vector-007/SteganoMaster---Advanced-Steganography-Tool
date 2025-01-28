import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from core.image_stego import hide_data, extract_data, detect_anomalies
from core.audio_stego import hide_data_lsb, extract_data_lsb, detect_anomalies_lsb
from core.video_stego import hide_data_frames, extract_data_frames, detect_anomalies_video
from core.encryption import encrypt_data, decrypt_data
import logging

class SteganoGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Steganography Tool")
        self.geometry("800x600")
        self._setup_ui()
        logging.basicConfig(level=logging.INFO)

    def _setup_ui(self):
        self.notebook = ttk.Notebook(self)
        
        # Hide Tab
        self.hide_frame = ttk.Frame(self.notebook)
        self._build_hide_tab(self.hide_frame)
        self.notebook.add(self.hide_frame, text="Hide")
        
        # Extract Tab
        self.extract_frame = ttk.Frame(self.notebook)
        self._build_extract_tab(self.extract_frame)
        self.notebook.add(self.extract_frame, text="Extract")
        
        # Detect Tab
        self.detect_frame = ttk.Frame(self.notebook)
        self._build_detect_tab(self.detect_frame)
        self.notebook.add(self.detect_frame, text="Detect")
        
        self.notebook.pack(expand=True, fill='both')

    def _build_hide_tab(self, frame):
        ttk.Label(frame, text="Cover File:").grid(row=0, column=0, padx=5, pady=5)
        self.hide_cover_entry = ttk.Entry(frame, width=50)
        self.hide_cover_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Browse", command=self._browse_hide_cover).grid(row=0, column=2)

        ttk.Label(frame, text="Secret File:").grid(row=1, column=0, padx=5, pady=5)
        self.hide_secret_entry = ttk.Entry(frame, width=50)
        self.hide_secret_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Browse", command=self._browse_hide_secret).grid(row=1, column=2)

        ttk.Label(frame, text="Password:").grid(row=2, column=0, padx=5, pady=5)
        self.hide_password_entry = ttk.Entry(frame, show="*", width=50)
        self.hide_password_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Output File:").grid(row=3, column=0, padx=5, pady=5)
        self.hide_output_entry = ttk.Entry(frame, width=50)
        self.hide_output_entry.grid(row=3, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Browse", command=self._browse_hide_output).grid(row=3, column=2)

        ttk.Button(frame, text="Hide Data", command=self._execute_hide).grid(row=4, column=1, pady=10)

    def _build_extract_tab(self, frame):
        ttk.Label(frame, text="Input File:").grid(row=0, column=0, padx=5, pady=5)
        self.extract_input_entry = ttk.Entry(frame, width=50)
        self.extract_input_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Browse", command=self._browse_extract_input).grid(row=0, column=2)

        ttk.Label(frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        self.extract_password_entry = ttk.Entry(frame, show="*", width=50)
        self.extract_password_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Output File:").grid(row=2, column=0, padx=5, pady=5)
        self.extract_output_entry = ttk.Entry(frame, width=50)
        self.extract_output_entry.grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Browse", command=self._browse_extract_output).grid(row=2, column=2)

        ttk.Button(frame, text="Extract Data", command=self._execute_extract).grid(row=3, column=1, pady=10)

    def _build_detect_tab(self, frame):
        ttk.Label(frame, text="File to Analyze:").grid(row=0, column=0, padx=5, pady=5)
        self.detect_file_entry = ttk.Entry(frame, width=50)
        self.detect_file_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Browse", command=self._browse_detect_file).grid(row=0, column=2)

        ttk.Button(frame, text="Detect Anomalies", command=self._execute_detect).grid(row=1, column=1, pady=10)
        self.detect_result_label = ttk.Label(frame, text="")
        self.detect_result_label.grid(row=2, column=1, pady=5)

    # File browsing methods
    def _browse_hide_cover(self):
        self._browse_file(self.hide_cover_entry, [("All Files", "*.*")])

    def _browse_hide_secret(self):
        self._browse_file(self.hide_secret_entry, [("All Files", "*.*")])

    def _browse_hide_output(self):
        self._browse_save_file(self.hide_output_entry, [("All Files", "*.*")])

    def _browse_extract_input(self):
        self._browse_file(self.extract_input_entry, [("All Files", "*.*")])

    def _browse_extract_output(self):
        self._browse_save_file(self.extract_output_entry, [("All Files", "*.*")])

    def _browse_detect_file(self):
        self._browse_file(self.detect_file_entry, [("All Files", "*.*")])

    def _browse_file(self, entry_widget, filetypes):
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, filename)

    def _browse_save_file(self, entry_widget, filetypes):
        filename = filedialog.asksaveasfilename(filetypes=filetypes)
        if filename:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, filename)

    # Execution methods
    def _execute_hide(self):
        try:
            cover_path = self.hide_cover_entry.get()
            secret_path = self.hide_secret_entry.get()
            output_path = self.hide_output_entry.get()
            password = self.hide_password_entry.get()

            with open(secret_path, 'rb') as f:
                secret_data = f.read()

            if cover_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                hide_data(cover_path, secret_data, output_path)
            elif cover_path.lower().endswith(('.wav', '.mp3')):
                hide_data_lsb(cover_path, secret_data, output_path, password)
            elif cover_path.lower().endswith(('.mp4', '.avi')):
                hide_data_frames(cover_path, secret_data, output_path, password)
            else:
                raise ValueError("Unsupported file format")

            messagebox.showinfo("Success", "Data hidden successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _execute_extract(self):
        try:
            input_path = self.extract_input_entry.get()
            output_path = self.extract_output_entry.get()
            password = self.extract_password_entry.get()

            if input_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                data = extract_data(input_path)
            elif input_path.lower().endswith(('.wav', '.mp3')):
                data = extract_data_lsb(input_path, password)
            elif input_path.lower().endswith(('.mp4', '.avi')):
                data = extract_data_frames(input_path, password)
            else:
                raise ValueError("Unsupported file format")

            with open(output_path, 'wb') as f:
                f.write(data)

            messagebox.showinfo("Success", "Data extracted successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _execute_detect(self):
        try:
            file_path = self.detect_file_entry.get()
            
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                result = detect_anomalies(file_path)
            elif file_path.lower().endswith(('.wav', '.mp3')):
                result = detect_anomalies_lsb(file_path)
            elif file_path.lower().endswith(('.mp4', '.avi')):
                result = detect_anomalies_video(file_path)
            else:
                raise ValueError("Unsupported file format")

            self.detect_result_label.config(
                text=f"Steganography detected: {result}",
                foreground="red" if result else "green"
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = SteganoGUI()
    app.mainloop()
