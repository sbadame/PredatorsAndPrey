import menu
import predpreyalgorithm
from Tkinter import *
from tkFileDialog import *
import webbrowser


#Grock Mutate Parameters, i.e. Number of Generations, Predators and Prey
def receive_mutate_parameters():
	#Use gen_num.get(), pred_num.get(), prey_num.get()
	pass

#Will call predpreyalgo to grock state of map through score function
def updatePlayingField(world):
	pass

#Will display successive turns on map
def animate():
	#predpreyalgorithm.score((predpreyalgorithm.best_pred, predpreyalgorithm.best_prey, updatePlayingField))
	playing_field.delete(ALL)
	draw_map()
	draw_root()

def README_display():
	webbrowser.open("help.html")

def About_display():
	webbrowser.open("about.html")

#Open pre-saved set of Predators
def open_pred():
	open_pred_file = askopenfilename(initialdir="critters/")	
	return open_pred_file

#Save a set of Predators
def save_pred():
	save_pred_file = asksaveasfilename(defaultextension=".pred",initialdir="critters/")
	return save_pred_file

#Open a re-saved set of prey
def open_prey():
	open_prey_file = askopenfilename(initialdir="critters/")
	return open_prey_file

#Save a set of Prey
def save_prey():
	save_prey_file = asksaveasfilename(defaultextension=".prey",initialdir="critters/")
	return save_prey_file

#Reset all values to default and clear the Playing Field
def reset():
	playing_field.delete(ALL)
	gen_num.set("10")
	speed_slider.set(0)
	pred_num.set("1")
	prey_num.set("20")
	draw_map()
	draw_root()

#Draw(place) all the widgets on the root
def draw_root():
	gen_num_label.grid(row=0, column=0, sticky=S)
	gen_num_input.grid(row=1, column=0, sticky=N)
	pred_num_label.grid(row=2, column=0, sticky=S)
	pred_num_input.grid(row=3, column=0, sticky=N)
	prey_num_label.grid(row=4, column=0, sticky=S)
	prey_num_input.grid(row=5, column=0, sticky=N)
	mutate_button.grid(row=6, column=0, sticky=N)
	key_title_label.grid(row=8, column=0)
	key_pred_label.grid(row=9, column=0, sticky=S)
	key_prey_label.grid(row=10, column=0)
	key_veg_label.grid(row=11, column=0, sticky=N)
	speed_slider_label.grid(row=13, column=0, sticky=S)
	speed_slider.grid(row=14, column=0, sticky=N)
	map_size_label.grid(row=15, column=0, sticky=S)
	map_size_input.grid(row=16, column=0, sticky=N)
	animate_button.grid(row=17, column=0, sticky=N)
	playing_field.grid(row=0, column=1, rowspan=17, padx=5)

#Draw the map of hexagons
def draw_map():
	size = map_size.get()
	size = int(size)
	y = 0
	for i in range(size):
    		if (i % 2 == 1):
        		x = 13
        		for j in range(size):       
            			playing_field.create_polygon(x,y+12, x+12,y, x+24,y+12, x+24,y+29, x+12,y+41, x,y+29, fill='', outline="black")
            			x = x + 24
    		else:
        		x = 1
        		for j in range(size):       
            			playing_field.create_polygon(x,y+12, x+12,y, x+24,y+12, x+24,y+29, x+12,y+41, x,y+29, fill='', outline="black")
            			x = x + 24
    		y = y + 29

	

if __name__ == "__main__":
	root = Tk()
	root.wm_title("Pred/Prey Animator")
	yscrollbar = Scrollbar(root, orient=VERTICAL)
	yscrollbar.grid(row=0, column=2, sticky=N+S+W+E, rowspan=17)
	xscrollbar = Scrollbar(root, orient=HORIZONTAL)
	xscrollbar.grid(row=18, column=0, sticky=N+S+W+E, columnspan=3)
	playing_field = Canvas(root, width=600, height=600, yscrollcommand=yscrollbar.set, xscrollcommand=xscrollbar.set, scrollregion=(0, 0, 3000, 3000))
	yscrollbar.config(command=playing_field.yview)
	xscrollbar.config(command=playing_field.xview)

	menu = Menu(root)
	root.config(menu=menu)
	file_menu = Menu(menu)
	menu.add_cascade(label="File", menu=file_menu)
	file_menu.add_command(label="Reset", command=reset)
	file_menu.add_separator()
	file_menu.add_command(label="Open Predators", command=open_pred)
	file_menu.add_command(label="Open Prey", command=open_prey)
	file_menu.add_separator()
	file_menu.add_command(label="Save Predators", command=save_pred)
	file_menu.add_command(label="Save Prey", command=save_prey)
	file_menu.add_separator()
	file_menu.add_command(label="Close", command=playing_field.quit)
	help_menu = Menu(menu)
	menu.add_cascade(label="Help", menu=help_menu)
	help_menu.add_command(label="README", command=README_display)
	help_menu.add_command(label="About...", command=About_display)



	speed_slider = Scale(root, from_=0, to=100, orient=HORIZONTAL)
	speed_slider_label = Label(root, text="Speed of Animation")



	gen_num = StringVar()
	pred_num = StringVar()
	prey_num = StringVar()
	map_size = StringVar()
	gen_num_label = Label(root, text="Number of Generations")
	gen_num_input = Entry(root, textvariable=gen_num)
	gen_num.set("10")
	pred_num_label = Label(root, text="Number of Predators")
	pred_num_input = Entry(root, textvariable=pred_num)
	pred_num.set("1")
	prey_num_label = Label(root, text="Number of Prey")
	prey_num_input = Entry(root, textvariable=prey_num)
	prey_num.set("20")
	mutate_button = Button(root, text="Mutate", command=receive_mutate_parameters)
	
	map_size_label = Label(root, text="Size of Map")
	map_size_input = Entry(root, textvariable=map_size)
	map_size.set("23")
	key_title_label = Label(root, text="Map Icon Key")
	key_pred_label = Label(root, text="Predator = D")
	key_prey_label = Label(root, text="Prey = Y")
	key_veg_label = Label(root, text="Vegetation = V")
	animate_button = Button(root, text="Animate", command=animate)


	draw_map()
	draw_root()
	root.mainloop()
