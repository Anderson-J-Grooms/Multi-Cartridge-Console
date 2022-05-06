import os
import keyboard
from evdev import InputDevice, categorize, ecodes
import time
import serial
import os.path
import sys

time.sleep(3)

try:
  os.system("clear")

  gamepad = InputDevice("/dev/input/event1")

  print("Press any button when SD card is ready")
  for event in gamepad.read_loop():
    if event.type == ecodes.EV_KEY:
      break

  print("mounting sd card")
  os.system("sudo mount /dev/mmcblk3p1 /home/pi/rom_dump")
  print("sd card mounted")

  time.sleep(2)
  gamepad = InputDevice("/dev/input/event1")
  #print(gamepad)
  print("")
  print("Please select what system you are playing on:")
  print("N64: left face button")
  print("SNES: bottom face button")
  print("Gameboy: right face button")
  time.sleep(.5)
  select = 0


  gamepad = InputDevice("/dev/input/event1")
  for event in gamepad.read_loop():
    #print(categorize(event))
    if event.type == ecodes.EV_KEY:
      keyevent = categorize(event)
      if keyevent.scancode == 307:
        select = 1
        break
      if keyevent.scancode == 304:
        select = 2
        break
      if keyevent.scancode == 305:
        select = 3
        break

  paths = []
  game_name = []
  if select == 1:
    for path, directories, files in os.walk('/home/pi/rom_dump/N64/'):
      if len(files) != 0:
        if ".n64" in files[0]:
          paths.append(os.path.join(path, files[0]))
          game_name.append(files[0])

  if select == 2:
    for path, directories, files in os.walk('/home/pi/rom_dump/SNES/'):
      if len(files) != 0:
        if ".sfc" in files[0]:
          paths.append(os.path.join(path, files[0]))
          game_name.append(files[0])
        if ".smc" in files[0]:
          paths.append(os.path.join(path, files[0]))
          game_name.append(files[0])

  if select == 3:
    for path, directories, files in os.walk('/home/pi/rom_dump/GBA/'):
      print(path)
      if len(files) != 0:
        if ".gba" in files[0]:
          print("Found Game")
          paths.append(os.path.join(path, files[0]))
          game_name.append(files[0])

  #print(paths)
  print("")
  print("Please choose which game you want to play:")
  print("Match your selection number to the game you want to play by pressing L1 and R1, then press bottom face button")
  time.sleep(1)
  for i in range(len(game_name)):
    print(str(i) + ": " + game_name[i])
  print("")
  gamepad = InputDevice("/dev/input/event1")
  game_select = 0

  print("You are selecting: " + str(int(game_select / 2) % len(game_name)))
  sys.stdout.write("\033[F")
  for event in gamepad.read_loop():
    if event.type == ecodes.EV_KEY:
      keyevent = categorize(event)
      if keyevent.scancode == 311:
         game_select += 1
         time.sleep(.1)
      if keyevent.scancode == 310:
         game_select -= 1
         time.sleep(.1)
      if keyevent.scancode == 304:
         gamepad.close()
         break
      print("You are selecting: " + str(int(game_select / 2) % len(game_name)))
      sys.stdout.write("\033[F")


  game_path = '"' + paths[(int(game_select/2) % len(game_name))] + '"'
  print("You have selected: " + game_name[int(game_select/2) % len(game_name)])
  time.sleep(3)

  print("done")

  if select == 1:
    os.system("/opt/retropie/supplementary/runcommand/runcommand.sh 0 _SYS_ n64 " + game_path)
  if select == 2:
    os.system("/opt/retropie/supplementary/runcommand/runcommand.sh 0 _SYS_ snes " + game_path)
  if select == 3:
    os.system("/opt/retropie/supplementary/runcommand/runcommand.sh 0 _SYS_ gba " + game_path)

except Exception:
  pass
