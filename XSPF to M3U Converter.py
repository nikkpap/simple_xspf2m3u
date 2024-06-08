import tkinter as tk
from tkinter import filedialog, messagebox
import xml.etree.ElementTree as ET

def load_xspf():
    file_path = filedialog.askopenfilename(filetypes=[("XSPF files", "*.xspf")])
    if file_path:
        with open(file_path, 'r', encoding='iso-8859-7') as file:
            xspf_content = file.read()
        convert_to_m3u(xspf_content)

def convert_to_m3u(xspf_content):
    try:
        root = ET.fromstring(xspf_content)
        track_list = root.find("{http://xspf.org/ns/0/}trackList")
        m3u_content = "#EXTM3U\n"

        for track in track_list.findall("{http://xspf.org/ns/0/}track"):
            location = track.find("{http://xspf.org/ns/0/}location").text
            creator = track.find("{http://xspf.org/ns/0/}creator").text
            title = track.find("{http://xspf.org/ns/0/}title").text
            m3u_content += f'#EXTINF:-1 tvg-id="" tvg-logo="" group-title="{creator}",{title}\n{location}\n'
        
        save_m3u(m3u_content)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to convert XSPF to M3U: {e}")

def save_m3u(m3u_content):
    file_path = filedialog.asksaveasfilename(defaultextension=".m3u", filetypes=[("M3U files", "*.m3u")])
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(m3u_content)
        messagebox.showinfo("Success", "M3U file has been saved successfully!")

def create_gui():
    root = tk.Tk()
    root.title("XSPF to M3U Converter")

    load_button = tk.Button(root, text="Load XSPF File", command=load_xspf)
    load_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
