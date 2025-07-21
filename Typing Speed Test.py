import tkinter as tk
import time
import random

long_paragraphs = [
    "Typing is a vital skill that can be improved with practice. "
    "The goal of this test is to type as quickly and accurately as possible. "
    "Make sure to match all words, punctuation, and spacing exactly. "
    "Speed matters, but accuracy is more important in the long run. "
    "Take your time, focus on each word, and do your best to complete the paragraph without any mistakes.",

    "Many professionals type for hours every day. Developing fast and accurate typing can make a big difference. "
    "Whether you're writing reports, code, or messages, the ability to type well saves time. "
    "This test helps you measure both speed and focus. Good luck and concentrate on typing with precision."
]

class TypingTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("900x600")
        self.root.configure(bg="#f0f4f8")

        self.start_time = None
        self.running = False
        self.time_limit = 60

        self.mode = tk.StringVar(value="Paragraph")
        self.prompt_text = tk.StringVar()

        self.create_widgets()
        self.reset_game()

    def create_widgets(self):
        header = tk.Label(self.root, text="Typing Speed Test",
                          font=("Segoe UI", 24, "bold"),
                          bg="#f0f4f8", fg="#1e293b")
        header.pack(pady=(20,10))

        mode_frame = tk.Frame(self.root, bg="#f0f4f8")
        mode_frame.pack(pady=(0,15))

        tk.Label(mode_frame, text="Choose Mode:", font=("Segoe UI", 12, "bold"),
                 bg="#f0f4f8", fg="#334155").pack(side=tk.LEFT, padx=5)

        for val in ["Paragraph", "Free"]:
            tk.Radiobutton(mode_frame, text=val, variable=self.mode, value=val,
                           bg="#f0f4f8", fg="#334155", font=("Segoe UI", 11),
                           activebackground="#e0e7ff", activeforeground="#1e40af",
                           selectcolor="#e0e7ff", command=self.reset_game).pack(side=tk.LEFT, padx=8)

        # Card frame for paragraph and input
        card_frame = tk.Frame(self.root, bg="white", bd=2, relief="groove")
        card_frame.pack(padx=20, pady=(0,20), fill="both", expand=True)

        self.paragraph_display = tk.Label(card_frame, textvariable=self.prompt_text,
                                          wraplength=840, font=("Segoe UI", 14),
                                          bg="white", fg="#334155", justify="left",
                                          padx=15, pady=15)
        self.paragraph_display.pack(pady=(20,10))

        self.text_input = tk.Text(card_frame, height=8, font=("Consolas", 16), wrap="word",
                                  bd=2, relief="solid", padx=10, pady=10)
        self.text_input.pack(padx=20, pady=(0,20), fill="x")
        self.text_input.bind("<KeyRelease>", self.on_typing)

        self.error_label = tk.Label(self.root, text="", font=("Segoe UI", 11), fg="#dc2626", bg="#f0f4f8")
        self.error_label.pack()

        self.info_label = tk.Label(self.root, text="", font=("Segoe UI", 14, "bold"), fg="#2563eb", bg="#f0f4f8")
        self.info_label.pack(pady=(10,20))

        self.restart_button = tk.Button(self.root, text="Restart", font=("Segoe UI", 13, "bold"),
                                        bg="#2563eb", fg="white", activebackground="#1d4ed8",
                                        activeforeground="white", bd=0, padx=25, pady=10,
                                        cursor="hand2", command=self.reset_game)
        self.restart_button.pack()

    def on_typing(self, event):
        if not self.running:
            self.running = True
            self.start_time = time.time()
            self.update_timer()

        input_text = self.text_input.get("1.0", "end-1c")
        expected = self.prompt_text.get()

        if self.mode.get() == "Paragraph":
            if input_text != expected[:len(input_text)]:
                self.text_input.config(fg="#b91c1c")  # Red for error
                self.error_label.config(text="Typing error! Please match the paragraph exactly.")
            else:
                self.text_input.config(fg="#1e293b")  # Dark slate for normal
                self.error_label.config(text="")

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

        if self.mode.get() == "Free":
            characters = len(input_text)
        else:
            expected = self.prompt_text.get()
            characters = self.count_correct_chars(input_text, expected)

        wpm = (characters / 5) / minutes if minutes > 0 else 0

        self.info_label.config(text=f"WPM: {wpm:.2f}   Time Left: {time_left}s")

        if elapsed >= self.time_limit:
            self.finish_test(elapsed, input_text)
        else:
            self.root.after(500, self.update_timer)

    def finish_test(self, elapsed, input_text):
        self.running = False
        self.text_input.config(state=tk.DISABLED)
        minutes = elapsed / 60
        if self.mode.get() == "Free":
            characters = len(input_text)
        else:
            expected = self.prompt_text.get()
            characters = self.count_correct_chars(input_text, expected)
        wpm = (characters / 5) / minutes if minutes > 0 else 0
        self.info_label.config(text=f"Test Complete! WPM: {wpm:.2f}   Time: {elapsed:.2f} seconds")

    def reset_game(self):
        self.running = False
        self.start_time = None
        self.text_input.config(state=tk.NORMAL)
        self.text_input.delete("1.0", tk.END)
        self.text_input.config(fg="#1e293b")
        self.error_label.config(text="")
        self.info_label.config(text="")

        if self.mode.get() == "Paragraph":
            self.prompt_text.set(random.choice(long_paragraphs))
        else:
            self.prompt_text.set("Type freely for 60 seconds. Your WPM will be calculated automatically.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingTestApp(root)
    root.mainloop()
