import tkinter as tk
import time
import random

# Sample paragraphs
long_paragraphs = [
    "Typing is a vital skill that can be improved with practice. The goal of this test is to type as quickly and accurately as possible.",
    "Many professionals type for hours every day. Developing fast and accurate typing can make a big difference."
]

level_sentences = [
    "Typing challenges help us become more accurate and efficient in using a keyboard every day, especially when writing for work or study.",
    "The art of speed typing comes from both muscle memory and mental focus, combining rapid movement with minimal errors.",
    "Accuracy should always be prioritized before speed, since repeated mistakes reduce overall effectiveness and communication clarity.",
    "Mastering long and difficult sentences enhances not only your typing ability but also your cognitive stamina under pressure.",
    "Typing games are far more than just a source of entertainment; they serve as powerful tools that train your fingers to move with precision and speed, while sharpening your mental focus and coordination. Through timed challenges and engaging practice, they help you build the muscle memory and discipline needed to become a confident and efficient typist in everyday life."
]

class TypingRaceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Race Challenge!")
        self.root.geometry("900x600")
        self.root.configure(bg="#aee1f9")

        self.time_limit = 60
        self.start_time = None
        self.running = False

        self.level_index = 0
        self.in_level_mode = False
        self.total_correct_chars = 0
        self.level_start_time = 0

        self.mode = tk.StringVar(value="Paragraph")
        self.prompt_text = tk.StringVar()

        self.menu_frame = None
        self.settings_frame = None
        self.instructions_frame = None
        self.game_frame = None

        self.create_main_menu()

    def create_main_menu(self):
        self.clear_frames()
        self.menu_frame = tk.Frame(self.root, bg="#aee1f9", bd=4, relief="ridge")
        self.menu_frame.pack(fill="both", expand=True, padx=40, pady=40)

        tk.Label(self.menu_frame, text="Typing Race Challenge!", font=("Comic Sans MS", 32, "bold"),
                 bg="#aee1f9", fg="white", relief="raised", bd=4, padx=10, pady=5).pack(pady=40)

        tk.Button(self.menu_frame, text="🚗 START RACE", font=("Comic Sans MS", 18, "bold"),
                  bg="#ff4d4d", fg="black", width=20, activebackground="#ff1a1a",
                  relief="raised", bd=4, command=self.start_game).pack(pady=10)

        tk.Button(self.menu_frame, text="🧠 LEVEL MODE", font=("Comic Sans MS", 16, "bold"),
                  bg="#ff4d4d", fg="black", width=20, activebackground="#ff1a1a",
                  relief="raised", bd=4, command=self.start_level_mode).pack(pady=10)

        tk.Button(self.menu_frame, text="⚙️ SETTINGS", font=("Comic Sans MS", 16, "bold"),
                  bg="#ff4d4d", fg="black", width=20, activebackground="#ff1a1a",
                  relief="raised", bd=4, command=self.show_settings).pack(pady=10)

        tk.Button(self.menu_frame, text="📖 INSTRUCTIONS", font=("Comic Sans MS", 16, "bold"),
                  bg="#ff4d4d", fg="black", width=20, activebackground="#ff1a1a",
                  relief="raised", bd=4, command=self.show_instructions).pack(pady=10)

        tk.Button(self.menu_frame, text="❌ QUIT", font=("Comic Sans MS", 16, "bold"),
                  bg="#ff4d4d", fg="black", width=20, activebackground="#ff1a1a",
                  relief="raised", bd=4, command=self.root.quit).pack(pady=10)

    def show_settings(self):
        self.clear_frames()
        self.settings_frame = tk.Frame(self.root, bg="#e0f7fa")
        self.settings_frame.pack(fill="both", expand=True)

        tk.Label(self.settings_frame, text="Choose Time Limit", font=("Comic Sans MS", 22, "bold"), bg="#e0f7fa", fg="#00796b").pack(pady=20)
        for seconds in [30, 60, 120, 180, 240, 300]:
            label = f"{seconds//60 if seconds >= 60 else seconds}{' min' if seconds >= 60 else ' sec'}"
            tk.Button(self.settings_frame, text=label, font=("Comic Sans MS", 16), width=15,
                      bg="#b2dfdb", fg="black", command=lambda s=seconds: self.set_time_limit(s)).pack(pady=5)

        tk.Button(self.settings_frame, text="⬅️ Back", font=("Comic Sans MS", 14),
                  bg="#80cbc4", fg="black", command=self.create_main_menu).pack(pady=20)

    def show_instructions(self):
        self.clear_frames()
        self.instructions_frame = tk.Frame(self.root, bg="#fffde7")
        self.instructions_frame.pack(fill="both", expand=True)

        tk.Label(self.instructions_frame, text="Instructions", font=("Comic Sans MS", 24, "bold"), bg="#fffde7", fg="#f57f17").pack(pady=20)
        msg = (
            "🏁 Typing Race Mode:\n\n"
            "• Type the given paragraph as accurately and fast as you can.\n"
            "• Timer starts when you type.\n"
            "• Only correctly typed characters count towards WPM.\n\n"
            "🧠 Level Mode:\n\n"
            "• Each level shows a longer and more difficult sentence.\n"
            "• Only type the sentence (not the level title).\n"
            "• Your stats are shown after completing all levels."
        )
        tk.Label(self.instructions_frame, text=msg, font=("Comic Sans MS", 14), bg="#fffde7", justify="left", wraplength=800).pack(pady=10, padx=30)

        tk.Button(self.instructions_frame, text="⬅️ Back", font=("Comic Sans MS", 14),
                  bg="#fdd835", fg="black", command=self.create_main_menu).pack(pady=20)

    def set_time_limit(self, seconds):
        self.time_limit = seconds
        self.create_main_menu()

    def clear_frames(self):
        for frame in [self.menu_frame, self.settings_frame, self.instructions_frame, self.game_frame]:
            if frame is not None:
                frame.pack_forget()

    def start_game(self):
        self.in_level_mode = False
        self.clear_frames()
        self.create_game_ui()
        self.reset_game()

    def start_level_mode(self):
        self.in_level_mode = True
        self.level_index = 0
        self.total_correct_chars = 0
        self.level_start_time = time.time()
        self.clear_frames()
        self.create_game_ui()
        self.reset_game()

    def create_game_ui(self):
        self.game_frame = tk.Frame(self.root, bg="#fff8e1")
        self.game_frame.pack(fill="both", expand=True)

        self.level_title = tk.Label(self.game_frame, text="", font=("Comic Sans MS", 22, "bold"), bg="#fff8e1", fg="#ff5722")
        self.level_title.pack(pady=(20, 10))

        self.paragraph_display = tk.Label(self.game_frame, textvariable=self.prompt_text,
                                          wraplength=800, font=("Comic Sans MS", 16),
                                          bg="#fff8e1", fg="#333333", justify="left")
        self.paragraph_display.pack(pady=20)

        self.text_input = tk.Text(self.game_frame, height=6, font=("Comic Sans MS", 16), wrap="word",
                                  bd=2, relief="solid", bg="#f0f0f0", fg="black")
        self.text_input.pack(padx=20, pady=(0, 20), fill="x")
        self.text_input.bind("<KeyRelease>", self.on_typing)

        self.info_label = tk.Label(self.game_frame, text="", font=("Comic Sans MS", 14, "bold"), fg="#3f51b5", bg="#fff8e1")
        self.info_label.pack()

        self.next_button = tk.Button(self.game_frame, text="➡️ Next Level", font=("Comic Sans MS", 14, "bold"),
                                     bg="#81c784", fg="black", command=self.next_level)
        self.restart_button = tk.Button(self.game_frame, text="🔁 Restart", font=("Comic Sans MS", 14, "bold"),
                                        bg="#ffc107", fg="black", command=self.reset_game)
        self.menu_button = tk.Button(self.game_frame, text="🏠 Main Menu", font=("Comic Sans MS", 12, "bold"),
                                     bg="#e0e0e0", fg="black", command=self.create_main_menu)
        self.restart_button.pack(pady=10)
        self.menu_button.pack()

    def on_typing(self, event):
        if not self.running:
            self.running = True
            self.start_time = time.time()
            self.update_timer()

        input_text = self.text_input.get("1.0", "end-1c")
        expected = self.prompt_text.get()

        if input_text != expected[:len(input_text)]:
            self.text_input.config(fg="#b91c1c")
        else:
            self.text_input.config(fg="black")

        if input_text == expected:
            elapsed = time.time() - self.start_time
            self.finish_test(elapsed, input_text)

    def count_correct_chars(self, typed, expected):
        count = 0
        for i, ch in enumerate(typed):
            if i >= len(expected) or ch != expected[i]:
                break
            count += 1
        return count

    def update_timer(self):
        if not self.running:
            return

        elapsed = time.time() - self.start_time
        time_left = max(0, self.time_limit - int(elapsed))
        minutes = elapsed / 60
        input_text = self.text_input.get("1.0", "end-1c")
        expected = self.prompt_text.get()

        correct_chars = self.count_correct_chars(input_text, expected)
        wpm = (correct_chars / 5) / minutes if minutes > 0 else 0

        self.info_label.config(text=f"WPM: {wpm:.2f}   Time Left: {time_left}s")

        if elapsed >= self.time_limit:
            self.finish_test(elapsed, input_text)
        else:
            self.root.after(500, self.update_timer)

    def finish_test(self, elapsed, input_text):
        self.running = False
        self.text_input.config(state=tk.DISABLED)
        expected = self.prompt_text.get()
        correct_chars = self.count_correct_chars(input_text, expected)
        minutes = elapsed / 60
        wpm = (correct_chars / 5) / minutes if minutes > 0 else 0
        self.info_label.config(text=f"🏁 Finished! WPM: {wpm:.2f}   Time: {elapsed:.2f}s")

        if self.in_level_mode:
            self.total_correct_chars += correct_chars
            if self.level_index < len(level_sentences) - 1:
                self.next_button.pack(pady=10)
            else:
                total_time = time.time() - self.level_start_time
                total_minutes = total_time / 60
                total_wpm = (self.total_correct_chars / 5) / total_minutes if total_minutes > 0 else 0
                self.info_label.config(text=f"🎉 All Levels Complete! Total WPM: {total_wpm:.2f}   Time: {total_time:.2f}s")

    def reset_game(self):
        self.running = False
        self.start_time = None
        self.text_input.config(state=tk.NORMAL)
        self.text_input.delete("1.0", tk.END)
        self.text_input.config(fg="black")
        self.info_label.config(text="")
        self.next_button.pack_forget()
        if self.in_level_mode:
            sentence = level_sentences[self.level_index]
            self.prompt_text.set(sentence)
            self.level_title.config(text=f"Level {self.level_index + 1}")
        else:
            self.prompt_text.set(random.choice(long_paragraphs))
            self.level_title.config(text="Race Mode")

    def next_level(self):
        self.level_index += 1
        self.reset_game()

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingRaceApp(root)
    root.mainloop()
