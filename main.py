import sys

import database as db
import docs as doc
import pygame


class App:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        self.width = 400
        self.height = 600
        # it will display on screen
        self.screen = pygame.display.set_mode([self.width, self.height])

        # basic font for user typed
        self.base_font = 'font/joystix.ttf'
        self.font = pygame.font.Font(self.base_font, 18)
        self.user_name = ''
        self.password = ''
        self.age = ''

        self.color_active = pygame.Color('lightskyblue3')

        self.color_passive = pygame.Color('blue')
        self.color = self.color_passive

        self.name_active = False
        self.pwd_active = False

        self.VALID_INPUT_LIST = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
                            'r', 's',
                            't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

        self.login_active = True
        self.reg_active = False
        self.age_active = False

        self.back_btn = self.button("None", self.width, self.height)
        self.bt_login = self.button("None", self.width, self.height)
        self.reg_btn = self.button("None", self.width, self.height)
        self.age_box = self.button("None", self.width, self.height)

        self.error = False
        self.error_txt = ''
        self.logged_in = False
        self.user = ""

    def draw_text(self, text, x, y):
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw_text_with_box(self, text, x, y, color, pwd=False, width=190):
        if pwd:
            nt = ""
            for i in range(len(text)):
                nt = nt + "*"

        text_surface = self.font.render(text if not pwd else nt, True, (255, 255, 255))
        rect = pygame.Rect(x, y, width, 32)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x+5, y+5)
        pygame.draw.rect(self.screen, color, rect)
        self.screen.blit(text_surface, text_rect)
        return rect

    def button(self, text, x, y):
        text_surface = self.font.render(text, True, (255, 0, 255))
        rect = pygame.Rect(x, y, 190, 32)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x+5, y+5)
        pygame.draw.rect(self.screen, (0, 255, 255), rect)
        self.screen.blit(text_surface, text_rect)
        return rect

    def login_screen(self):
        if self.name_active:
            color_name = self.color_active
            color_pwd = self.color_passive
        elif self.pwd_active:
            color_pwd = self.color_active
            color_name = self.color_passive
        else:
            color_name = self.color_passive
            color_pwd = self.color_passive

        self.draw_text("Login", self.width/6, self.height/7)
        self.draw_text("Name", self.width/6, self.height/7 + 30)
        self.draw_text("Password", self.width/6, self.height/7 + 80)
        self.name_box = self.draw_text_with_box(self.user_name, self.width / 6, self.height / 7 + 50, color_name)
        self.pwd_box = self.draw_text_with_box(self.password, self.width / 6, self.height / 7 + 100, color_pwd, True)
        self.bt_login = self.button("Login", self.width / 6, self.height / 7 + 150)
        self.go_to_reg = self.button("Register", self.width / 6, self.height / 7 + 200)

        if self.error:
            self.draw_text_with_box(self.error_txt[0] + " " + self.error_txt[1], self.width/6, self.height/7 - 70, (255, 0, 0), False, 280)
            self.draw_text_with_box(self.error_txt[2] + " " + self.error_txt[3], self.width/6, self.height/7 - 40, (255, 0, 0))

    def register_screen(self):
        if self.name_active:
            color_name = self.color_active
            color_pwd = self.color_passive
            color_age = self.color_passive
        elif self.pwd_active:
            color_pwd = self.color_active
            color_name = self.color_passive
            color_age = self.color_passive
        elif self.age_active:
            color_age = self.color_active
            color_name = self.color_passive
            color_pwd = self.color_passive
        else:
            color_name = self.color_passive
            color_pwd = self.color_passive
            color_age = self.color_passive
        self.draw_text("Register", self.width / 6, self.height / 7)
        self.draw_text("Name", self.width / 6, self.height / 7 + 30)
        self.draw_text("Password", self.width / 6, self.height / 7 + 80)
        self.draw_text("Age", self.width / 6, self.height / 7 + 130)
        self.name_box = self.draw_text_with_box(self.user_name, self.width / 6, self.height / 7 + 50, color_name)
        self.pwd_box = self.draw_text_with_box(self.password, self.width / 6, self.height / 7 + 100, color_pwd, True)
        self.age_box = self.draw_text_with_box(self.age, self.width / 6, self.height / 7 + 150, color_age)
        self.reg_btn = self.button("Register", self.width / 6, self.height / 7 + 200)
        self.back_btn = self.button("Back", self.width / 6, self.height / 7 + 250)

        if self.error:
            self.draw_text_with_box(self.error_txt[0] + " " + self.error_txt[1], self.width/6, self.height/7 - 70, (255, 0, 0))
            self.draw_text_with_box(self.error_txt[2] + " " + self.error_txt[3], self.width/6, self.height/7 - 40, (255, 0, 0), False, 280)


    def trigger(self, button):
        if button == self.bt_login:
            if self.user_name != "" and self.password != "":
                # backend for login
                self.user = doc.get("INDB app FROM users WHERE username?==?" + self.user_name + " AND password?==?" + self.password)
                if len(self.user) >= 1:
                    print("Logged in!")
                    self.logged_in = True
                    self.error = False
                else:
                    self.error = True
                    self.error_txt = 'Incorrect username or password'
                    self.error_txt = self.error_txt.split(' ')
        if button == self.reg_btn:
            if self.user_name != "" and self.password != "" and self.age != "":
                # backend for registration
                check = []
                check = doc.get("INDB app FROM users WHERE username?==?" + self.user_name)
                if check == []:
                    doc.add(self.user_name + "," + self.password + "," + self.age + " INDB app INTO users")
                    print("Register completed!")
                else:
                    self.error = True
                    self.error_txt = "This user already exists!"
                    self.error_txt = self.error_txt.split(' ')
        if button == self.go_to_reg:
            self.error = False
            self.name_box = None
            self.pwd_box = None
            self.bt_login = self.button("None", self.width, self.height)
            self.password = ''
            self.user_name = ''
            self.age = ''
            self.color = self.color_passive
            self.name_active = False
            self.pwd_active = False
            self.login_active = False
            self.reg_active = True
            self.go_to_reg = self.button("None", self.width, self.height)
        if button == self.back_btn:
            self.error = False
            self.back_btn = self.button("None", self.width, self.height)
            self.reg_btn = self.button("NOne", self.width, self.height)
            self.color = self.color_passive
            self.name_active = False
            self.age_active = False
            self.pwd_active = False
            self.password = ''
            self.age = ''
            self.user_name = ''
            self.reg_active = False
            self.age_active = False
            self.login_active = True
            self.age_box = self.button("NOne", self.width, self.height)

    def run(self):
        while True:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.name_box.collidepoint(event.pos):
                        self.name_active = True
                        self.pwd_active = False
                        self.age_active = False
                    elif self.pwd_box.collidepoint(event.pos):
                        self.pwd_active = True
                        self.name_active = False
                        self.age_active = False
                    elif self.age_box.collidepoint(event.pos):
                        self.age_active = True
                        self.pwd_active = False
                        self.name_active = False
                    elif self.bt_login.collidepoint(event.pos):
                        self.trigger(self.bt_login)
                    elif self.reg_btn.collidepoint(event.pos):
                        self.trigger(self.reg_btn)
                    elif self.go_to_reg.collidepoint(event.pos):
                        self.trigger(self.go_to_reg)
                    elif self.back_btn.collidepoint(event.pos):
                        self.trigger(self.back_btn)
                    else:
                        self.name_active = False
                        self.pwd_active = False
                        self.age_active = False

                if event.type == pygame.KEYDOWN:
                    if self.name_active:
                        if event.key == pygame.K_BACKSPACE:
                            self.user_name = self.user_name[:-1]
                        else:
                            if event.unicode in self.VALID_INPUT_LIST and len(self.user_name) < 12:
                                self.user_name += event.unicode
                    if self.pwd_active:
                        if event.key == pygame.K_BACKSPACE:
                            self.password = self.password[:-1]
                        else:
                            if event.unicode in self.VALID_INPUT_LIST and len(self.password) < 12:
                                self.password += event.unicode
                    if self.age_active:
                        if event.key == pygame.K_BACKSPACE:
                            self.age = self.age[:-1]
                        else:
                            if event.unicode in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] and len(self.age) <= 3:
                                self.age += event.unicode

            self.screen.fill((50, 100, 100))

            if self.login_active:
                self.login_screen()
            elif self.reg_active:
                self.register_screen()

            # display.flip() will update only a portion of the
            # screen to updated, not full area
            pygame.display.flip()

            self.clock.tick(60)

            if self.logged_in:
                return self.user


class LoggedIn:
    def __init__(self, user):
        self.user = user
        pygame.init()
        self.clock = pygame.time.Clock()

        self.width = 400
        self.height = 600
        # it will display on screen
        self.screen = pygame.display.set_mode([self.width, self.height])

        # basic font for user typed
        self.base_font = 'font/joystix.ttf'
        self.font = pygame.font.Font(self.base_font, 18)

        self.color_active = pygame.Color('lightskyblue3')
        self.color_passive = pygame.Color('blue')
        self.color = self.color_passive

        self.username = self.user[0][1]

        self.show_pwd = False
        self.password = self.user[0][2]
        self.password_hidden = ""
        for i in range(len(self.password)):
            self.password_hidden += "*"

        self.age = self.user[0][3]
        self.age_txt = ''
        self.age_active = False
        self.logout = False

    def draw_text_with_box(self, text, x, y, color, width=190, height=32):
        text_surface = self.font.render(text, True, (255, 255, 255))
        rect = pygame.Rect(x, y, width, height)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x+5, y+5)
        pygame.draw.rect(self.screen, color, rect)
        self.screen.blit(text_surface, text_rect)
        return rect

    def user_window(self):
        if self.age_active:
            color_age = self.color_active
        else:
            color_age = self.color_passive

        self.draw_text_with_box("username: " + str(self.username), self.width/6, self.height/7, self.color_passive, 280)
        self.draw_text_with_box("password: " + str(self.password_hidden) if not self.show_pwd else "password: " + str(self.password), self.width/6, self.height/7 + 50, self.color_passive, 280)
        self.pass_btn = self.draw_text_with_box("show", self.width/6 + 180, self.height/7 + 100, self.color_passive, 100)

        self.draw_text_with_box("age: " + str(self.age), self.width/6, self.height/7 + 150, self.color_passive, 140)
        self.edit_age = self.draw_text_with_box("new age: " + str(self.age_txt), self.width/6, self.height/7 + 200, color_age, 220)
        self.update_age_btn = self.draw_text_with_box("Update age", self.width/6, self.height/7 + 250, self.color_passive)

        self.delete_acc_btn = self.draw_text_with_box("Delete account", self.width/6, self.height/7 + 400, self.color_passive, 220)
        self.logout_btn = self.draw_text_with_box("logout", self.width/6, self.height/7 + 450, self.color_passive, 110)

    def trigger(self, button):
        if button == self.update_age_btn:
            # backend
            doc.update("INDB app INTO users UPDATE age WHERE username?==?" + str(self.username) + " TO " + self.age_txt)
            self.update_user()
        if button == self.delete_acc_btn:
            # backend
            doc.delete("WHERE name?==?" + self.username + " INDB app FROM users", True)
            self.logout = True
        if button == self.logout_btn:
            self.logout = True

    def update_user(self):
        # backend
        self.user = doc.get(
            "INDB app FROM users WHERE username?==?" + self.username + " AND password?==?" + self.password)
        self.password = self.user[0][2]
        self.age = self.user[0][3]
        self.age_txt = ""
        self.age_active = False

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.pass_btn.collidepoint(event.pos):
                        self.show_pwd = not self.show_pwd
                    elif self.edit_age.collidepoint(event.pos):
                        self.age_active = True
                    elif self.update_age_btn.collidepoint(event.pos):
                        self.trigger(self.update_age_btn)
                    elif self.delete_acc_btn.collidepoint(event.pos):
                        self.trigger(self.delete_acc_btn)
                    elif self.logout_btn.collidepoint(event.pos):
                        self.trigger(self.logout_btn)
                    else:
                        self.age_active = False

                if event.type == pygame.KEYDOWN:
                    if self.age_active:
                        if event.key == pygame.K_BACKSPACE:
                            self.age_txt = self.age_txt[:-1]
                        else:
                            if event.unicode in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] and len(self.age_txt) <= 3:
                                self.age_txt += event.unicode
            self.screen.fill((255, 100, 100))

            self.user_window()

            pygame.display.flip()
            self.clock.tick(60)

            if self.logout:
                return


if __name__ == '__main__':
    # db.create_database("app")
    # doc.create_doc("CRDOC users INDB app", "id: int, username: string, password: string, age: int")
    # doc.add("admin,admin,21 INDB app INTO users")
    while True:
        app = App()
        success = app.run()
        if success:
            app = None
            loggedin = LoggedIn(success)
            loggedin.run()
