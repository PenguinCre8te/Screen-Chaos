import tkinter as tk
import random
import os
import sys



class WindowClosingGame:
    @staticmethod
    def resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
    def __init__(self, master):
        self.master = master
        self.master.title("Window chaos")
        self.master.geometry("400x250")
        self.master.attributes("-topmost", True)
        temp = WindowClosingGame.resource_path("icon.ico")
        root.iconbitmap(temp)
        

        self.level = 1
        self.num_windows = 2
        self.high_score = 1
        self.windows = []
        self.moving_windows = 0  # Number of windows that will move

        # UI Elements
        self.label = tk.Label(self.master, text="Level 1 - Survive the Windows!", font=("Arial", 14))
        self.label.pack(pady=10)
        
        self.high_score_label = tk.Label(self.master, text="High Score: 1", font=("Arial", 12), fg="blue")
        self.high_score_label.pack()

        self.restart_button = tk.Button(self.master, text="Restart", font=("Arial", 12), command=self.restart_game)
        self.restart_button.pack(pady=10)
        self.restart_button.pack_forget()  # Hide the button initially

        self.create_windows()

    def update_message(self, text):
        """Updates the main window's message."""
        self.label.config(text=text)

    def update_high_score(self):
        """Updates the high score display."""
        self.high_score_label.config(text=f"High Score: {self.high_score}")

    def create_windows(self):
        """Creates windows with countdown timers and windows, ensuring they appear on top."""
        self.moving_windows = min(self.level, self.num_windows // 2)  # More moving windows as levels increase
        

        for i in range(self.num_windows):
            new_win = tk.Toplevel(self.master)
            new_win.geometry(f"200x100+{random.randint(100, 800)}+{random.randint(100, 600)}")
            new_win.attributes("-topmost", True)  # Ensure windows stay on top
            new_win.attributes("-topmost", True)
            temp = WindowClosingGame.resource_path("icon.ico")
            new_win.iconbitmap(temp)

            is_window = random.choice([True])  # 100% chance for a window
            if self.level < 21:
                time_limit = random.randint(9000, 70000 - (self.level * 3000))  # Timer between 3-20 seconds
                
            else:
                time_limit = random.randint(3000, 9000)

            label = tk.Label(new_win, text="Closing in...", font=("Arial", 12))
            label.pack()
            
            countdown_label = tk.Label(new_win, text=f"{time_limit // 1000} sec", font=("Arial", 14), fg="red")
            countdown_label.pack()

            if is_window:
                new_win.title("💣 window! Survive the countdown!")

            new_win.protocol("WM_DELETE_WINDOW", lambda w=new_win: self.close_window(w))
            self.windows.append((new_win, is_window, countdown_label, time_limit))

            self.update_timer(new_win, time_limit, countdown_label, is_window)

            # Make some windows move
            print('New Window, time_limit', time_limit, 'level', self.level)
            if i < self.moving_windows:
                self.move_window(new_win)
                print('↑ is moving')
            
            
    def move_window(self, window):
        """Makes a window teleport in steps toward a random new position."""
        if window.winfo_exists():
            target_x = random.randint(100, 800)
            target_y = random.randint(100, 600)
            current_x, current_y = window.winfo_x(), window.winfo_y()

            step_x = (target_x - current_x) // 10
            step_y = (target_y - current_y) // 10

            self.smooth_move(window, current_x, current_y, step_x, step_y, target_x, target_y)

    def smooth_move(self, window, x, y, step_x, step_y, target_x, target_y):
        """Gradually moves the window in small steps while keeping it inside the screen."""
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        
        # Get actual window dimensions
        window.update_idletasks()  # Ensure geometry is up-to-date
        window_width = window.winfo_width()
        window_height = window.winfo_height()
        
        # Ensure target stays within screen bounds
        target_x = max(0, min(screen_width - window_width, target_x))
        target_y = max(0, min(screen_height - window_height, target_y))
        
        # Calculate direction and distance
        dx = target_x - x
        dy = target_y - y
        
        # If close enough to target, pick a new target
        if abs(dx) <= abs(step_x) and abs(dy) <= abs(step_y):
            self.master.after(1000, lambda: self.move_window(window))
        else:
            # Adjust step to avoid overshooting
            new_x = x + step_x if abs(dx) > abs(step_x) else target_x
            new_y = y + step_y if abs(dy) > abs(step_y) else target_y
            
            # Ensure new position is within bounds
            new_x = max(0, min(screen_width - window_width, new_x))
            new_y = max(0, min(screen_height - window_height, new_y))
            
            window.geometry(f"{window_width}x{window_height}+{int(new_x)}+{int(new_y)}")
            self.master.after(50, lambda: self.smooth_move(window, new_x, new_y, step_x, step_y, target_x, target_y))
    def update_timer(self, window, time_left, label, is_window):
        """Updates the countdown timer on the window safely."""
        if time_left <= 0:
            if is_window:
                self.game_over()
            window.destroy()
            self.windows = [w for w in self.windows if w[0] != window]
            return

        if window.winfo_exists():
            # Update the countdown label
            label.config(text=f"{time_left // 1000}.{(time_left % 1000) // 100} sec")
            
            # Flash the window faster when the timer is under 8 seconds
            if time_left <= 8000:
                current_bg = window.cget("background")
                new_bg = "red" if current_bg != "red" else "white"
                window.configure(background=new_bg)
            
            # Update every 100 milliseconds
            self.master.after(100, lambda: self.update_timer(window, time_left - 100, label, is_window))
        else:
            return  # Window was closed, stop updating

    def close_window(self, window):
        """Closes a window safely."""
        window.destroy()
        self.windows = [w for w in self.windows if w[0] != window]

        if not self.windows:
            self.next_level()

    def next_level(self):
        """Progresses to the next level, increasing difficulty."""
        self.level += 1
        self.num_windows += 3  # Increase number of windows each level
        self.update_message(f"🚀 Level {self.level}! Faster windows incoming...")
        self.create_windows()

    def game_over(self):
        """Ends the game if a window explodes and closes all remaining windows except the main one."""
        self.update_message("💥 A window exploded! Game Over.")

        # Close all windows except the main one
        for w, _, _, _ in self.windows:
            if w.winfo_exists() and w != self.master:
                w.destroy()

        self.windows.clear()  # Ensure the list is emptied

        self.restart_button.pack()  # Show restart button
        self.high_score = max(self.high_score, self.level)
        self.update_high_score()

    def restart_game(self):
        """Resets the game to level 1 and hides the restart button."""
        self.level = 1
        self.num_windows = 5
        self.update_message("Level 1 - Survive the windows!")
        self.restart_button.pack_forget()  # Hide restart button
        self.create_windows()

if __name__ == "__main__":
    root = tk.Tk()
    game = WindowClosingGame(root)
    root.mainloop()

