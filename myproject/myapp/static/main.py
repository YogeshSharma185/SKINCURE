class NavMenu:
    def __init__(self):
        self.active = False

    def toggle(self):
        self.active = not self.active
        print("Menu is now:", "ACTIVE" if self.active else "INACTIVE")


menu = NavMenu()
menu.toggle()
menu.toggle()
