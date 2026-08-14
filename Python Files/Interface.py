import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox
import os

class Interface:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1500x850")
        self.main_window.title("Holiday Design - Pyrotechnic Sequencer")
        self.main_window.configure(bg="#f0f0f0")

        table_frame = tk.Frame(self.main_window, borderwidth=2, relief="solid")
        table_frame.place(x=640, y=90, width=830, height=730)

        scroll_y = ttk.Scrollbar(table_frame, orient="vertical")
        scroll_y.pack(side="right", fill="y")

        columns = ("cue", "time", "channel", "controller", "device")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scroll_y.set,
            height=30
        )
        scroll_y.config(command=self.tree.yview)

        self.tree.heading("cue", text="#")
        self.tree.heading("time", text="Time Code (HH:MM:SS.ms)")
        self.tree.heading("channel", text="Channel")
        self.tree.heading("controller", text="Controller")
        self.tree.heading("device", text="Device")

        self.tree.column("cue", width=50, anchor="center")
        self.tree.column("time", width=180, anchor="center")
        self.tree.column("channel", width=120, anchor="center")
        self.tree.column("controller", width=120, anchor="center")
        self.tree.column("device", width=120, anchor="center")

        self.tree.tag_configure("evenrow", background="#ffffff")
        self.tree.tag_configure("oddrow", background="#e8f0fe")

        self.tree.pack(fill="both", expand=True)

        self.port_frame = tk.Frame(self.main_window, bg="#f0f0f0", height=270, width=600, borderwidth=2, relief="solid")
        self.port_frame.place(x=20, y=90)

        self.channel_frame = tk.Frame(self.main_window, bg="#f0f0f0", height=460, width=600, borderwidth=2,
                                      relief="solid")
        self.channel_frame.place(x=20, y=380)


        self.menubar = tk.Menu(self.main_window)
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="Open file", command=self.open_file)
        self.file_menu.add_command(label = "Save file", command = self.save_file)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.main_window.config(menu=self.menubar)


        self.support_menu = tk.Menu(self.menubar, tearoff = 0)
        self.support_menu.add_command(label = "About",command = self.open_about_window)    # Here are two toplevel windows
        self.support_menu.add_command(label = "Guideline", command = self.open_guideline_window)
        self.menubar.add_cascade(label="Support", menu = self.support_menu)
        self.main_window.config(menu=self.menubar)



    def open_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Text File",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as file:
                lines = file.readlines()

            for row in self.tree.get_children():
                self.tree.delete(row)

            for index, line in enumerate(lines, start=1):
                parts = line.strip().split()
                if len(parts) >= 4:
                    raw_time, controller, channel, device = parts[0], parts[1], parts[2], parts[3]
                    formatted_time = format_timestamp(raw_time)

                    row_tag = "evenrow" if index % 2 == 0 else "oddrow"

                    self.tree.insert(
                        "",
                        "end",
                        values=(index, formatted_time, channel, controller, device),
                        tags=(row_tag,)
                    )

        except Exception as e:
            messagebox.showerror("File Error", f"Could not read file:\n{e}")



    def save_file(self):
        desktop = os.path.join(os.path.expanduser("~"), "All Files")
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialdir=desktop,
            title="Save Text File",
            filetypes=[(".txt", "*.txt")]
        )

        if not file_path:
            return

        with open(file_path, "w") as f:
            f.write("your content here")

##### the function below demonstrates a small pop-window for guidelines where all the steps are shown in order for users)))
    def open_guideline_window(self):
        guideline_window = tk.Toplevel(self.main_window)
        guideline_window.resizable(False, False)
        guideline_window.title("Guideline")
        guideline_window.geometry("600x300")
        guideline_window.configure(bg = "white")
        guideline_text = (
            "Step 1: First of all, please open your text file by choosing an appropriate menu button "
            "(File in this case) and choose the first option from there.\n\n"

            "Step 2: Please choose the right directory—for instance, if your text file is inside Documents, "
            "please choose Documents.\n\n"

            "Step 3: After choosing the right file, you will notice that your text file is displayed "
            "inside the table on the right side."
        )

        step_1 = tk.Label(
            guideline_window,
            bg="white",
            fg="black",
            font=("Arial", 11),
            text=guideline_text,
            justify="left",
            wraplength=550
        )

        step_1.place(x=3, y=20)



 ## this function below tells about this software and where and why this is used....
    def open_about_window(self):
            about_window = tk.Toplevel(self.main_window)
            about_window.resizable(False, False)
            about_window.title("Guideline")
            about_window.geometry("600x300")
            about_window.configure(bg="white")
            about_text = (
                "This software operates as a centralized pyrotechnic show controller designed to manage, sequence, and execute synchronized fireworks displays via an Arduino hardware unit. The user interface is split into two main operational sections: \n\n"
                "Left Panel (Control & Hardware Link): The top Port Frame manages the serial communication bridge (USB/COM ports) between your computer and the Arduino controller. Directly below it, the Channel Frame provides real-time channel status, continuity feedback, and manual testing controls so you can verify each output block before arming the system. \n"
                "Right Panel (Cue Timeline Display): This primary workspace renders your imported .txt show file into an ordered, chronological table. It breaks down each event into distinct columns showing the Cue Number, Time Code, Controller ID, Channel ID, and Device ID, ensuring you can review the exact firing sequence at a glance.\n"
                "Top Navigation Bar: Houses quick-access tools for loading text files (File), executing manual channel tests (Test), and opening operational instructions (Help/Support). \n\n"
                "Overall, the program takes raw timing text files, parses and sequences the events chronologically, gives you full control over your hardware connections and channel states, and sends high-precision firing commands down to the Arduino driver blocks for flawless timing execution."
            )

            step_2 = tk.Label(
                about_window,
                bg="white",
                fg="black",
                font=("Arial", 11),
                text= about_text,
                justify="left",
                wraplength=550
            )
            step_2.place(x = 3, y = 40)






def format_timestamp(raw_time_str):
    try:
        val = float(raw_time_str.lower().replace("s", ""))
        mins, secs = divmod(val, 60)
        hours, mins = divmod(mins, 60)
        return f"{int(hours):02d}:{int(mins):02d}:{secs:05.2f}"
    except ValueError:
        return raw_time_str


if __name__ == "__main__":
    app = Interface()
    app.main_window.mainloop()
