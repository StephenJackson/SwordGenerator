import Tkinter as tk
import random

## should only ever be printed.
class MakeSword(object):
    def __init__(self):
        self._error = []
        self._lists = {
            "visual": [],
            "audio": [],
            "shape": [],
            "materials": [],
            "qualities": [],
            "unique": []
            }
        self._populate_lists()
        
    ## for every key in self._lists function will look for a txt file in lists/keyname.txt, open it, and add every line to a list in that key.
    ## if file not found adds error to user output
    ## also informs the user if the file is there but empty
    def _populate_lists(self):   
        for key, keyed_list in self._lists.iteritems():
            current_file = "lists/{file_list_item}.txt".format(file_list_item=key)
            try:
                with open(current_file, "r") as the_file:
                    temp_list = "".join(the_file.readlines())
                    for item in temp_list.rsplit('\n'):
                        if item != '':
                            self._lists[key].append(item)
                    if not keyed_list:
                        self._error.append("{currentfile}: is empty.\n".format(currentfile=current_file))
            except IOError:
                self._error.append("{currentfile}: not found.\n".format(currentfile=current_file))

    #makes swords. takes in a dict of lists containing sword options, picks out items from said lists at random, returns output in __str__     
    def _make_sword(self):

        output = []
        
        def pick_rand(pick):
            return random.choice(self._lists[pick])
                
        ## sword material needed some special love, since it is unique in that it is possible to have more than one material.
        def material_gen():
            mat_output = []
            dice = random.randint(1, 12)
            mat_output.append("made of {mat}".format(mat=pick_rand('materials')))
            if dice >= 6:
                mat_output.append(" and {mat}".format(mat=pick_rand('materials')))
            if dice >= 10:
                mat_output.append(" AND {mat}".format(mat=pick_rand('materials')))
            if dice == 12:
                mat_output.append(" AAAAAND {mat}".format(mat=pick_rand('materials')))
            return "".join(mat_output)

        ## grammar fixer, checks for a or an case.
        def grammar_pick(input_list):
            an_cases = ("a", "e", "i", "o", "u", "hon")
            u_cases = ("un", "on", "us")
            rand_result = pick_rand(input_list)
            rand_result_lower = rand_result.lower() #case matters!
            if rand_result_lower.startswith(an_cases) and not rand_result_lower.startswith(u_cases):
                return "an {result}".format(result=rand_result)
            else:
                return "a {result}".format(result=rand_result)

        output.append("With {grammarAudio}, ".format(grammarAudio=grammar_pick("audio")))
        if random.randint(1,20) == 20:
            output.append("{grammarUnique} ".format(grammarUnique=grammar_pick('unique')))
        else:
            output.append("{grammarShape} {material}, ".format(grammarShape=grammar_pick('shape'), material=material_gen()))
        output.append("{visual}.".format(visual=pick_rand('visual')))
        if random.randint(1,20) == 20:
            output.append(" The weapon also has {quality}.".format(quality=pick_rand('qualities')))
        if random.randint(1,10) == 10:
            output.append(" The weapon menaces with spikes of {material}.".format(material=pick_rand('materials')))

        return "".join(output)

    def _error_return(self):
        return "{errors}Please fix the errors and restart the program.".format(errors="".join(self._error))

    def __str__(self):
        if self._error:
            return self._error_return()
        else:
            return self._make_sword()
        

## stuff to present a GUI to the user. pretty self explanitory, makes a text area and a button that prints a MakeSword object. Also deletes old results to keep it clean.
class SwordApp(tk.Frame):
    def __init__(self, sword, master=None):
        tk.Frame.__init__(self, master)
        self.sword = sword
        self.text = tk.Text(height=7, padx=5, pady=5, wrap=tk.WORD)
        self.button = tk.Button(master, text="MAKE SWORD", command=self._print_sword)
        self.button.pack()
        self.text.pack()
        self._welcome()

    def _print_sword(self):
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.INSERT, self.sword)

    def _welcome(self):
        welcome_text = "Welcome to Sword.py! To generate a 'Sword of Legend!' simply press the button.\n\nTo add more possible outcomes: open a .txt file in the lists folder, add your new options, save the file, and restart the program.\n\nCreated by Stephen Jackson. Powered by Python."
        self.text.insert(tk.INSERT, welcome_text)

## and now to bring it all together
if __name__ == "__main__":
    make_sword = MakeSword()
    app_master = tk.Tk()
    test = SwordApp(make_sword, app_master)
    test.mainloop()
    
    
