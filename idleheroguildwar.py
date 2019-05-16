import os
import time
import threading
import pyautogui 
import pyscreeze 
import pytesseract 
import unicodedata 
# from pyautogui import screenshot, locateOnScreen

from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode


# ex rel_path = "screenshot\data.txt"
def get_abs_file_path(rel_path):
	script_dir = os.path.dirname(__file__) #absolute dir the script is in
	return os.path.join(script_dir, rel_path)
	
	
delay = 11
button = Button.left
check_key = KeyCode(char='s')
force_key = KeyCode(char='f')
exit_key = KeyCode(char='e')
Switch = False
	
IdleHeroLocated = (0,0)
guildnameArea = (0,190,280,30)
# guildsearch = get_abs_file_path('screenshot\\unity2.png')
guildnameImg = get_abs_file_path('screenshot\\term.png')

def GetGuildNameArea():
	global IdleHeroLocated
	
	if IdleHeroLocated != (0,0):
		return (IdleHeroLocated[0] + guildnameArea[0],IdleHeroLocated[1] + guildnameArea[1],guildnameArea[2], guildnameArea[3])
	
	try:
		box = pyautogui.locateOnScreen(get_abs_file_path('screenshot\\topright.png'))
		IdleHeroLocated = (box.left , box.top)
		return (IdleHeroLocated[0] + guildnameArea[0],IdleHeroLocated[1] + guildnameArea[1],guildnameArea[2], guildnameArea[3])
	except pyscreeze.ImageNotFoundException:
		raise pyscreeze.ImageNotFoundException


class ClickMouse(threading.Thread):
	def __init__(self, delay, button):
		super(ClickMouse, self).__init__()
		self.delay = delay
		self.button = button
		self.running = False
		self.program_running = True
		self.switch = False
		self.MacroPosition = (0,0)

	def start_clicking(self):
		self.running = True

	def stop_clicking(self):
		self.running = False

	def exit(self):
		self.stop_clicking()
		self.program_running = False
		
	def GetMacroPosition(self):
		if self.MacroPosition != (0,0): return self.MacroPosition
		try:
			box = pyautogui.locateOnScreen(get_abs_file_path('screenshot\\GuildWarOff.png'))
			self.switch = False
			self.MacroPosition = (box.left + 94 , box.top + 9)
			return (box.left + 94 , box.top + 9)
		except pyscreeze.ImageNotFoundException:
			try:
				box = pyautogui.locateOnScreen(get_abs_file_path('screenshot\\GuildWarOn.png'))
				self.switch = True
				self.MacroPosition = (box.left + 94 , box.top + 9)
				return (box.left + 94 , box.top + 9)
			except pyscreeze.ImageNotFoundException:
				raise pyscreeze.ImageNotFoundException	
				
	def GetFightPosition(self):
		if self.MacroPosition != (0,0): return (self.MacroPosition[0], self.MacroPosition[1] + 40)
		try:
			box = pyautogui.locateOnScreen(get_abs_file_path('screenshot\\GuildWarOff.png'))
			self.switch = False
			self.MacroPosition = (box.left + 94 , box.top + 9)
			return (box.left + 94 , box.top + 9 + 40)
		except pyscreeze.ImageNotFoundException:
			try:
				box = pyautogui.locateOnScreen(get_abs_file_path('screenshot\\GuildWarOn.png'))
				self.switch = True
				self.MacroPosition = (box.left + 94 , box.top + 9)
				return (box.left + 94 , box.top + 9 + 40)
			except pyscreeze.ImageNotFoundException:
				raise pyscreeze.ImageNotFoundException
	
	def SwitchMacro(self,value):
		if self.running:
			if self.switch != value:
				old = mouse.position
				pyautogui.mouseUp()
				try:
					if self.MacroPosition == (0,0):
						mouse.position = self.GetMacroPosition()
					if self.switch != value:
						mouse.click(self.button)
						mouse.position = old
						self.switch = value
				except pyscreeze.ImageNotFoundException:
					print("Can't find Macro")
			
	def run(self):
		global IdleHeroLocated
		global Switch
		global guildnameArea
		
		while self.program_running:
			while self.running:
				try:
					GuildnameArea = GetGuildNameArea()
				except pyscreeze.ImageNotFoundException:
					print("Can't find Nox")
					continue 
				
				im = pyautogui.screenshot(region=GuildnameArea)
				im.save(get_abs_file_path("screenshot\\term.png"),'png')
				GuildName = pytesseract.image_to_string(get_abs_file_path("screenshot\\term.png"))
				try:
					GuildName = unicodedata.normalize('NFKC', GuildName)
					print(GuildName)
					im.save(get_abs_file_path(("screenshot\\{0}.png").format(GuildName)),'png')
					if GuildName == 'The Dimmadome':
						old = mouse.position
						pyautogui.mouseUp()
						mouse.position = self.GetFightPosition()
						mouse.click(self.button)
						mouse.position = old
						time.sleep(13)
						continue
					
				except UnicodeEncodeError:
					print(GuildName.encode('utf-8'), '(Error)')
					
				#L: mmmu
				old = mouse.position
				pyautogui.mouseUp()
				mouse.position = self.GetMacroPosition()
				mouse.click(self.button)
				mouse.position = old
				print("not ok")
				time.sleep(self.delay)
			time.sleep(0.1)

# try:
	# box = pyautogui.locateOnScreen(get_abs_file_path('screenshot\\GuildWarOff.png'))
	# self.switch = False
	# return (box.left + 94 , box.top + 9)
# except pyscreeze.ImageNotFoundException:
	# try:
		# box = pyautogui.locateOnScreen(get_abs_file_path('screenshot\\GuildWarOn.png'))
		# self.switch = True
		# return (box.left + 94 , box.top + 9)
	# except pyscreeze.ImageNotFoundException:
		# print("Can't find Macro")
		
mouse = Controller()
click_thread = ClickMouse(delay, button)
click_thread.start()
print("starting....")
click_thread.start_clicking()

def on_press(key):
	# if key == check_key:
		# # click_thread.running = False
		# # print(click_thread.switch)
		# # click_thread.running = True
	# elif key == force_key:
		# # click_thread.running = False
		# # click_thread.running = True
	# elif
	if key == exit_key:
		print("stoping....")
		click_thread.exit()
		listener.stop()

with Listener(on_press=on_press) as listener:
	listener.join()
	
	
