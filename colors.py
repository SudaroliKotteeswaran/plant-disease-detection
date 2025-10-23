import sys, time, math, random

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ORANGE = '\033[38;5;208m'
    WHITE = '\033[97m'
    GREY = '\033[90m'

def colorize(text, color):
    return f"{color}{text}{bcolors.ENDC}"

def typing_effect(text, color=bcolors.WHITE, delay=0.02):
    for char in text:
        sys.stdout.write(color + char + bcolors.ENDC)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def spinner(text, duration=2):
    spinner_icons = ['|', '/', '-', '\\']
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r{text} {spinner_icons[i % len(spinner_icons)]}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write("\r" + " " * (len(text) + 5) + "\r")

def progress_bar(total=20, text="Processing"):
    for i in range(total + 1):
        bar = "█" * i + "-" * (total - i)
        sys.stdout.write(f"\r{text}: [{bar}] {int((i/total)*100)}%")
        sys.stdout.flush()
        time.sleep(0.05)
    print()

def wave_title(text, cycles=2, delay=0.05, beep=True):
    for cycle in range(cycles * len(text)):
        sys.stdout.write("\r")
        for i, char in enumerate(text):
            offset = int(2 * math.sin((i + cycle) * 0.5))
            spaces = " " * (offset + 2)
            color = bcolors.OKGREEN if i % 2 == 0 else bcolors.OKCYAN
            sys.stdout.write(color + spaces + char + bcolors.ENDC)
            if beep and offset > 1:
                sys.stdout.write("\a")  # terminal beep
        sys.stdout.flush()
        time.sleep(delay)
    print("\n")

def sparkle_effect(text, duration=1.5):
    """Add sparkle ✨ effect around text"""
    sparkle_chars = ['✨', '★', '✦', '✧']
    end_time = time.time() + duration
    while time.time() < end_time:
        decorated = "".join(random.choice(sparkle_chars) + c for c in text)
        sys.stdout.write("\r" + colorize(decorated, bcolors.WARNING))
        sys.stdout.flush()
        time.sleep(0.2)
    print("\n")
