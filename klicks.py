import tkinter as tk
from pynput import mouse
import threading
import time
from tkinter import filedialog
import pygame # Pygame-Bibliothek importieren

# Globale Variablen
click_count = 0
start_time = 0
timer_running = False
listener = None
ranking_list = []

# Funktion, die bei jedem Mausklick aufgerufen wird
def on_click(x, y, button, pressed):
    global click_count, timer_running, start_time, ranking_list, listener
    if pressed:
        # Startet den Timer beim ersten Klick
        if not timer_running and click_count < 100:
            start_time = time.time()
            timer_running = True
            update_timer()

        # Zählt nur, wenn der Zähler noch nicht 100 erreicht hat
        if click_count < 100:
            click_count += 1
            click_label.config(text=f'Klicks: {click_count}')

        # Stoppt den Timer nach 100 Klicks, speichert die Zeit und aktualisiert die Rangliste
        if click_count == 100 and timer_running:
            timer_running = False
            elapsed_time = time.time() - start_time
            ranking_list.append(elapsed_time)
            ranking_list.sort() # Sortiert die Liste vom schnellsten zum langsamsten
            update_ranking_display()
            result_label.config(text=f"100 Klicks erreicht! Deine Zeit: {elapsed_time:.2f}s")
            listener.stop()  # Stoppt den Maushörer
            pygame.mixer.music.stop() # Stoppt die Musik

# Funktion zum Aktualisieren der Stoppuhr-Anzeige
def update_timer():
    global timer_running, start_time
    if timer_running:
        elapsed_time = time.time() - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        milliseconds = int((elapsed_time - int(elapsed_time)) * 100)
        timer_label.config(text=f'Zeit: {minutes:02}:{seconds:02}:{milliseconds:02}')
        window.after(10, update_timer)

# Funktion zum Aktualisieren der Ranglisten-Anzeige
def update_ranking_display():
    ranking_text = "Rangliste:\n"
    for i, time_taken in enumerate(ranking_list[:5]): # Zeigt nur die Top 5 an
        ranking_text += f"{i+1}. {time_taken:.2f}s\n"
    ranking_label.config(text=ranking_text)

# Funktion zum Zurücksetzen von Zähler und Stoppuhr
def reset_all():
    global click_count, timer_running, start_time, listener
    click_count = 0
    timer_running = False
    start_time = 0
    click_label.config(text=f'Klicks: {click_count}')
    timer_label.config(text='Zeit: 00:00:00')
    result_label.config(text='')

    # Startet den Maushörer neu
    if not listener.running:
        listener = mouse.Listener(on_click=on_click)
        listener_thread = threading.Thread(target=listener.start, daemon=True)
        listener_thread.start()

    # Startet die Musik wieder
    pygame.mixer.music.play(-1)


# Funktion zum Herunterladen der Rangliste als .txt-Datei
def download_ranking():
    # Öffnet einen Dialog, um den Speicherort auszuwählen
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Textdateien", "*.txt")], title="Rangliste speichern")
    if file_path:
        with open(file_path, "w") as f:
            f.write("Mausklick-Rangliste (100 Klicks)\n\n")
            for i, time_taken in enumerate(ranking_list):
                f.write(f"{i+1}. {time_taken:.2f} Sekunden\n")
        result_label.config(text=f"Rangliste gespeichert in: {file_path}", fg="green")


# Erstellt das Hauptfenster
window = tk.Tk()
window.title("Mausklick-Zähler")
window.geometry("400x550")
window.configure(bg='white')

# Erstellt ein Label zur Anzeige des Mausklick-Zählers
click_label = tk.Label(window, text=f'Klicks: {click_count}', font=('Arial', 30), bg='white')
click_label.pack(pady=(20, 10))

# Erstellt ein Label zur Anzeige der Stoppuhr
timer_label = tk.Label(window, text='Zeit: 00:00:00', font=('Arial', 20), bg='white')
timer_label.pack(pady=(10, 20))

# Erstellt ein Label für die Ergebnis- oder Statusmeldung
result_label = tk.Label(window, text='', font=('Arial', 16), bg='white', fg='red')
result_label.pack()

# Erstellt einen Reset-Button
reset_button = tk.Button(window, text="Zurücksetzen", command=reset_all, font=('Arial', 14))
reset_button.pack(pady=10)

# Erstellt einen Button zum Herunterladen der Rangliste
download_button = tk.Button(window, text="Rangliste speichern", command=download_ranking, font=('Arial', 14))
download_button.pack(pady=5)

# Erstellt ein Label für die Rangliste
ranking_label = tk.Label(window, text="Rangliste:", font=('Arial', 16), bg='white', justify='left')
ranking_label.pack(pady=(20, 0))

# Startet den Maushörer neu
listener = mouse.Listener(on_click=on_click)
listener_thread = threading.Thread(target=listener.start, daemon=True)
listener_thread.start()

# --- Pygame für Musik hinzufügen ---
pygame.mixer.init() # Initialisiert den Mixer

# WICHTIG: Ersetze 'deine_musikdatei.mp3' durch den tatsächlichen Pfad zu deiner Musikdatei
pygame.mixer.music.load('SKYLAExceed.mp3')
# Spielt die Musik in einer Schleife ab. Der Parameter -1 bedeutet endlose Wiederholung.
pygame.mixer.music.play(-1)

# Startet die Hauptschleife des Fensters
window.mainloop()