HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

print(f"{WARNING}test color WARNING{ENDC}\n"
      f"{HEADER}test color HEADER{ENDC}\n"
      f"{OKBLUE}test color OKBLUE{ENDC}\n"
      f"{OKCYAN}test color OKCYAN{ENDC}\n"
      f"{OKGREEN}test color OKGREEN{ENDC}\n"
      f"{FAIL}test color FAIL{ENDC}\n"
      f"{BOLD}test color BOLD{ENDC}\n"
      f"{UNDERLINE}test color UNDERLINE{ENDC}\n")
