# Typing-Speed-Test-Game
Typing Speed Test
Overview
This is a simple and user-friendly Typing Speed Test application built with Python and Tkinter. It measures your typing speed in words per minute (WPM) and helps improve your typing accuracy and speed.

Features
Two Modes:

Paragraph Mode: Type a displayed paragraph exactly as shown without errors.

Free Typing Mode: Type anything freely for 60 seconds.

Live WPM and Timer: Shows your current typing speed and remaining time in real-time.

Error Highlighting: Paragraph mode highlights errors if your input doesn't match the prompt.

60-Second Timer: The test runs for one minute or until the paragraph is completed.

Clean and Intuitive Interface: Easy to read fonts and a visually appealing layout.

How to Use
Run the application by executing the Python script.

Choose your mode at the top:

Paragraph: Type the given paragraph exactly.

Free: Type anything for 60 seconds.

Start typing in the input box below the prompt.

Watch your live WPM and remaining time update as you type.

Complete the paragraph or wait until the timer ends.

View your final WPM score displayed below the input area.

Click "Restart" to try again or switch modes.

Requirements
Python 3.x

Tkinter (usually included with Python standard library)

Installation
No special installation needed. Just ensure Python is installed on your system.

Running the App
Run the script using:

bash
Copy
Edit
python typing_speed_test.py
Notes
Accuracy matters in Paragraph mode; any mismatch will highlight errors.

In Free mode, WPM is calculated based on all typed characters.

The WPM is calculated as (correct characters / 5) / (elapsed time in minutes).
