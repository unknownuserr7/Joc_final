import pygame
import random
import math
import asyncio
import os
import platform

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Joc Militar: Invasió Alienígena")
clock = pygame.time.Clock()
FPS = 60

NEGRE = (30, 30, 50)
BLANC = (255, 255, 255)
VERMELL = (255, 0, 0)
VERD = (0, 255, 0)
BLAU = (0, 0, 255)
GROC = (255, 255, 0)
TARONJA = (255, 165, 0)
GRIS = (100, 100, 100)
MORAT = (128, 0, 128)
VERMELL_FOSC = (139, 0, 0)

try:
    font = pygame.font.SysFont('PressStart2P', 40)
    font_small = pygame.font.SysFont('PressStart2P', 20)
    font_narrativa = pygame.font.SysFont('PressStart2P', 24)
except pygame.error:
    font = pygame.font.SysFont('arial', 40)
    font_small = pygame.font.SysFont('arial', 20)
    font_narrativa = pygame.font.SysFont('arial', 24)

try:
    jugador_imgs = {
        'Pistola': pygame.transform.scale(pygame.image.load(os.path.join('assets', 'jugador_pistola.png')), (60,60)),
        'Fusell': pygame.transform.scale(pygame.image.load(os.path.join('assets', 'jugador_fusell.png')), (60,60)),
        'Minigun': pygame.transform.scale(pygame.image.load(os.path.join('assets', 'jugador_minigun.png')), (60,60))
    }
    enemic_img = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'enemic.png')), (40, 30))
    enemic_boss_imgs = {
        0: pygame.transform.scale(pygame.image.load(os.path.join('assets', 'enemic_boss_nivell_0.png')), (60, 40)),
        1: pygame.transform.scale(pygame.image.load(os.path.join('assets', 'enemic_boss_nivell_1.png')), (60, 40)),
        2: pygame.transform.scale(pygame.image.load(os.path.join('assets', 'enemic_boss_nivell_2.png')), (60, 40))
    }
    enemic_boss_final_img = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'enemic_boss_final.png')), (100, 80))
    fons_nivells = {
        (0, 0): pygame.transform.scale(pygame.image.load(os.path.join('assets', 'fons_nivell_0_0.png')), (WIDTH, HEIGHT)),
        (0, 1): pygame.transform.scale(pygame.image.load(os.path.join('assets', 'fons_nivell_0_1.png')), (WIDTH, HEIGHT)),
        (0, 2): pygame.transform.scale(pygame.image.load(os.path.join('assets', 'fons_nivell_0_2.png')), (WIDTH, HEIGHT)),
        (1, 0): pygame.transform.scale(pygame.image.load(os.path.join('assets', 'fons_nivell_1_0.png')), (WIDTH, HEIGHT)),
        (1, 1): pygame.transform.scale(pygame.image.load(os.path.join('assets', 'fons_nivell_1_1.png')), (WIDTH, HEIGHT)),
        (1, 2): pygame.transform.scale(pygame.image.load(os.path.join('assets', 'fons_nivell_1_2.png')), (WIDTH, HEIGHT)),
        (2, 0): pygame.transform.scale(pygame.image.load(os.path.join('assets', 'fons_nivell_2_0.png')), (WIDTH, HEIGHT)),
        (2, 1): pygame.transform.scale(pygame.image.load(os.path.join('assets', 'fons_nivell_2_1.png')), (WIDTH, HEIGHT)),
        (2, 2): pygame.transform.scale(pygame.image.load(os.path.join('assets', 'fons_nivell_2_2.png')), (WIDTH, HEIGHT))
    }
except pygame.error as e:
    print(f"Error al cargar imágenes: {e}")
    jugador_imgs = {key: None for key in ['Pistola', 'Fusell', 'Minigun']}
    enemic_img = None
    enemic_boss_imgs = {key: None for key in [0, 1, 2]}
    enemic_boss_final_img = None
    fons_nivells = {(i, j): None for i in range(3) for j in range(3)}

class Particula:
    def __init__(self, x, y, vx, vy, color, duracio=20, size=5):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.duracio = duracio
        self.temps = 0
        self.size = size

    def actualitzar(self):
        self.x += self.vx
        self.y += self.vy
        self.temps += 1
        self.size = max(1, int(self.size - 0.2))
        return self.temps >= self.duracio

    def dibuixar(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))

class Efecte:
    def __init__(self, x, y, tipus, duracio=30):
        self.x = x
        self.y = y
        self.tipus = tipus
        self.duracio = duracio
        self.temps = 0
        self.size = 10 if tipus == 'dispar' else 20 if tipus == 'explosio' else 15
        self.particules = []
        self.inicialitzar_particules()

    def inicialitzar_particules(self):
        if self.tipus == 'dispar':
            for _ in range(5):
                angle = random.uniform(0, 2 * math.pi)
                velocitat = random.uniform(2, 5)
                vx = math.cos(angle) * velocitat
                vy = math.sin(angle) * velocitat
                self.particules.append(Particula(self.x, self.y, vx, vy, GROC, duracio=15, size=3))
        elif self.tipus == 'explosio':
            for _ in range(20):
                angle = random.uniform(0, 2 * math.pi)
                velocitat = random.uniform(3, 8)
                vx = math.cos(angle) * velocitat
                vy = math.sin(angle) * velocitat
                color = random.choice([TARONJA, VERMELL, GROC])
                self.particules.append(Particula(self.x, self.y, vx, vy, color, duracio=30, size=5))
        elif self.tipus == 'dany':
            for _ in range(10):
                angle = random.uniform(0, 2 * math.pi)
                velocitat = random.uniform(2, 6)
                vx = math.cos(angle) * velocitat
                vy = math.sin(angle) * velocitat
                self.particules.append(Particula(self.x, self.y, vx, vy, VERMELL, duracio=20, size=4))
        elif self.tipus == 'item':
            for _ in range(8):
                angle = random.uniform(0, 2 * math.pi)
                velocitat = random.uniform(1, 4)
                vx = math.cos(angle) * velocitat
                vy = math.sin(angle) * velocitat
                self.particules.append(Particula(self.x, self.y, vx, vy, VERD, duracio=25, size=3))
        elif self.tipus == 'escut':
            for _ in range(15):
                angle = random.uniform(0, 2 * math.pi)
                velocitat = random.uniform(2, 5)
                vx = math.cos(angle) * velocitat
                vy = math.sin(angle) * velocitat
                self.particules.append(Particula(self.x, self.y, vx, vy, BLAU, duracio=20, size=4))
        elif self.tipus == 'radial':
            for _ in range(20):
                angle = random.uniform(0, 2 * math.pi)
                velocitat = random.uniform(3, 7)
                vx = math.cos(angle) * velocitat
                vy = math.sin(angle) * velocitat
                self.particules.append(Particula(self.x, self.y, vx, vy, TARONJA, duracio=25, size=5))
        elif self.tipus == 'regen':
            for _ in range(10):
                angle = random.uniform(0, 2 * math.pi)
                velocitat = random.uniform(1, 4)
                vx = math.cos(angle) * velocitat
                vy = math.sin(angle) * velocitat
                self.particules.append(Particula(self.x, self.y, vx, vy, VERD, duracio=30, size=3))
        elif self.tipus == 'narrativa':
            for _ in range(20):
                angle = random.uniform(0, 2 * math.pi)
                velocitat = random.uniform(1, 3)
                vx = math.cos(angle) * velocitat
                vy = math.sin(angle) * velocitat
                self.particules.append(Particula(self.x, self.y, vx, vy, BLANC, duracio=50, size=2))
        elif self.tipus == 'derrota':
            for _ in range(30):
                angle = random.uniform(0, 2 * math.pi)
                velocitat = random.uniform(2, 5)
                vx = math.cos(angle) * velocitat
                vy = math.sin(angle) * velocitat
                self.particules.append(Particula(self.x, self.y, vx, vy, VERMELL, duracio=100, size=5))

    def actualitzar(self):
        self.temps += 1
        if self.tipus in ['explosio']:
            self.size += 3
        for particula in self.particules[:]:
            if particula.actualitzar():
                self.particules.remove(particula)
        return self.temps >= self.duracio

    def dibuixar(self):
        if self.tipus == 'dispar':
            pygame.draw.circle(screen, GROC, (self.x, self.y), self.size, 2)
        elif self.tipus == 'explosio':
            pygame.draw.circle(screen, TARONJA, (self.x, self.y), self.size, 3)
        elif self.tipus == 'dany':
            pygame.draw.circle(screen, VERMELL, (self.x, self.y), self.size, 2)
        elif self.tipus == 'item':
            pygame.draw.circle(screen, VERD, (self.x, self.y), self.size, 2)
        elif self.tipus == 'escut':
            pygame.draw.circle(screen, BLAU, (self.x, self.y), self.size, 2)
        elif self.tipus == 'radial':
            pygame.draw.circle(screen, TARONJA, (self.x, self.y), self.size, 3)
        elif self.tipus == 'regen':
            pygame.draw.circle(screen, VERD, (self.x, self.y), self.size, 2)
        for particula in self.particules:
            particula.dibuixar()

class Jugador:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT - 50 - 60
        self.vx = 0
        self.vy = 0
        self.vida = 100
        self.width = 40
        self.height = 60
        self.gravetat = 0.8
        self.velocitat = 5
        self.forca_salt = -15
        self.terra = True
        self.escut_actiu = False
        self.temps_escut = 0
        self.direccio = 1  # 1 para derecha, -1 para izquierda

    def moure(self, esquerra, dreta, salt):
        self.vx = 0
        if esquerra:
            self.vx = -self.velocitat
            self.direccio = -1  # Gira a la izquierda
        if dreta:
            self.vx = self.velocitat
            self.direccio = 1  # Gira a la derecha
        if salt and self.terra:
            self.vy = self.forca_salt
            self.terra = False
        self.vy += self.gravetat
        self.x += self.vx
        self.y += self.vy
        if self.x < 0:
            self.x = 0
        if self.x > WIDTH - self.width:
            self.x = WIDTH - self.width
        if self.y > HEIGHT - 50 - self.height:
            self.y = HEIGHT - 50 - self.height
            self.vy = 0
            self.terra = True

    def dibuixar(self, arma_actual):
        jugador_img = jugador_imgs.get(arma_actual, None)
        if jugador_img:
            # Gira la imagen según la dirección
            img_a_dibujar = pygame.transform.flip(jugador_img, self.direccio == -1, False) if self.vx != 0 else jugador_img
            screen.blit(img_a_dibujar, (self.x, self.y))
        else:
            pygame.draw.rect(screen, VERD, (self.x, self.y, self.width, self.height))
        if self.escut_actiu:
            pygame.draw.rect(screen, BLAU, (self.x - 5, self.y - 5, self.width + 10, self.height + 10), 3)
        if self.vida > 0:
            cors_ple = self.vida // 20
            for i in range(5):
                x = 10 + i * 30
                y = 10
                if i < cors_ple:
                    pygame.draw.polygon(screen, VERMELL, [
                        (x + 10, y), (x + 20, y + 10), (x + 10, y + 20), (x, y + 10)
                    ])
                else:
                    pygame.draw.polygon(screen, GRIS, [
                        (x + 10, y), (x + 20, y + 10), (x + 10, y + 20), (x, y + 10)
                    ], 2)

class Boto:
    def __init__(self, x, y, w, h, text, accio=None, color=BLAU, color_hover=VERMELL):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.accio = accio
        self.color = color
        self.color_hover = color_hover

    def dibuixar(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and self.accio:
            pygame.draw.rect(screen, self.color_hover, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        text_surf = font_small.render(self.text, True, BLANC)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def clic(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and self.accio:
            self.accio()

class Plataforma:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

    def dibuixar(self):
        pygame.draw.rect(screen, GROC, self.rect)

class Enemic:
    def __init__(self, x, y, vida, es_boss=False, es_boss_final=False, nivell=0):
        self.x = x
        self.y = y
        self.vida = vida
        self.es_boss = es_boss
        self.es_boss_final = es_boss_final
        self.nivell = nivell
        self.width = 100 if es_boss_final else 60 if es_boss else 40
        self.height = 80 if es_boss_final else 40 if es_boss else 30
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.temps_atac = 0
        self.temps_canvi_direccio = 0
        self.dany_bala = 15 if es_boss_final else 10 if es_boss else 5

    def actualitzar(self, jugador, altres_enemics):
        bales = []
        self.temps_atac += 1
        self.temps_canvi_direccio += 1

        dx = jugador.x + jugador.width / 2 - (self.x + self.width / 2)
        dy = jugador.y + jugador.height / 2 - (self.y + self.height / 2)
        dist = math.sqrt(dx ** 2 + dy ** 2)
        if dist > 0:
            vx_bala = (dx / dist) * 8
            vy_bala = (dy / dist) * 8
        else:
            vx_bala, vy_bala = 0, 0

        if self.es_boss_final:
            if self.temps_atac >= 90:
                self.temps_atac = 0
                for angle in range(0, 360, 15):
                    rad = math.radians(angle)
                    vx = math.cos(rad) * 8
                    vy = math.sin(rad) * 8
                    bales.append(Bala(self.x + self.width / 2, self.y + self.height / 2, vx, vy, dany=10))
        else:
            if self.temps_atac > (60 if self.es_boss else 90):
                self.temps_atac = 0
                if self.es_boss:
                    bales.append(Bala(self.x + self.width / 2, self.y + self.height / 2, vx_bala * 1.2, vy_bala * 1.2, dany=self.dany_bala))
                    bales.append(Bala(self.x + self.width / 2, self.y + self.height / 2, vx_bala * 1.2, vy_bala * 1.2 + 2, dany=self.dany_bala))
                    bales.append(Bala(self.x + self.width / 2, self.y + self.height / 2, vx_bala * 1.2, vy_bala * 1.2 - 2, dany=self.dany_bala))
                else:
                    bales.append(Bala(self.x + self.width / 2, self.y + self.height / 2, vx_bala, vy_bala, dany=self.dany_bala))

        if self.temps_canvi_direccio > 60:
            self.vx += random.uniform(-1, 1)
            self.vy += random.uniform(-1, 1)
            speed = math.sqrt(self.vx ** 2 + self.vy ** 2)
            if speed > 4:
                self.vx = (self.vx / speed) * 4
                self.vy = (self.vy / speed) * 4
            self.temps_canvi_direccio = 0

        dist_jugador = math.sqrt((self.x - jugador.x) ** 2 + (self.y - jugador.y) ** 2)
        if dist_jugador < (150 if self.es_boss_final else 100):
            angle = math.atan2(self.y - jugador.y, self.x - jugador.x)
            self.vx += math.cos(angle) * 0.1
            self.vy += math.sin(angle) * 0.1

        for altre in altres_enemics:
            if altre != self:
                dist = math.sqrt((self.x - altre.x) ** 2 + (self.y - altre.y) ** 2)
                if 0 < dist < 80:
                    angle = math.atan2(self.y - altre.y, self.x - altre.x)
                    self.vx += math.cos(angle) * 0.05
                    self.vy += math.sin(angle) * 0.05

        self.x += self.vx
        self.y += self.vy

        margin = 50
        if self.x < -margin:
            self.x = -margin
            self.vx = abs(self.vx)
        if self.x > WIDTH + margin:
            self.x = WIDTH + margin
            self.vx = -abs(self.vx)
        if self.y < -margin:
            self.y = -margin
            self.vy = abs(self.vy)
        if self.y > HEIGHT + margin:
            self.y = HEIGHT + margin
            self.vy = -abs(self.vy)

        return bales

    def dibuixar(self):
        if self.es_boss_final and enemic_boss_final_img:
            screen.blit(enemic_boss_final_img, (self.x, self.y))
        elif self.es_boss and enemic_boss_imgs.get(self.nivell):
            screen.blit(enemic_boss_imgs[self.nivell], (self.x, self.y))
        elif enemic_img:
            screen.blit(enemic_img, (self.x, self.y))
        else:
            color = VERMELL_FOSC if self.es_boss or self.es_boss_final else MORAT
            pygame.draw.ellipse(screen, color, (self.x, self.y, self.width, self.height))
        if self.es_boss or self.es_boss_final:
            pygame.draw.rect(screen, VERMELL, (self.x, self.y - 20, self.width, 10))
            max_vida = 1200 if self.es_boss_final else 400 if self.vida > 200 else 200 if self.vida > 100 else 100
            pygame.draw.rect(screen, VERD, (self.x, self.y - 20, self.width * (self.vida / max_vida), 10))

class Bala:
    def __init__(self, x, y, vx, vy, tipus_arma='pistola', dany=10):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.tipus_arma = tipus_arma
        self.dany = dany
        self.width = 20 if tipus_arma == 'massiu' else 10 if tipus_arma == 'pistola' else 15 if tipus_arma == 'fusell' else 8 if tipus_arma == 'minigun' else 20
        self.height = 10 if tipus_arma == 'massiu' else 7 if tipus_arma == 'fusell' else 5 if tipus_arma == 'minigun' else 10
        self.color = VERMELL if tipus_arma == 'massiu' else BLANC if tipus_arma == 'pistola' else GROC if tipus_arma == 'fusell' else TARONJA if tipus_arma == 'minigun' else TARONJA

    def actualitzar(self):
        self.x += self.vx
        self.y += self.vy

    def dibuixar(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

class Item:
    def __init__(self, x, y, tipus):
        self.x = x
        self.y = y
        self.tipus = tipus
        self.width = 20
        self.height = 20
        self.anim_temps = 0

    def dibuixar(self):
        self.anim_temps = (self.anim_temps + 1) % 60
        offset_y = math.sin(self.anim_temps / 10) * 5
        if self.tipus == 'vida':
            pygame.draw.polygon(screen, VERMELL, [
                (self.x + 10, self.y + offset_y),
                (self.x + 20, self.y + 10 + offset_y),
                (self.x + 10, self.y + 20 + offset_y),
                (self.x, self.y + 10 + offset_y)
            ])
            pygame.draw.circle(screen, BLANC, (self.x + 10, self.y + 10 + offset_y), 5, 1)
        elif self.tipus == 'bales':
            pygame.draw.rect(screen, GROC, (self.x + 5, self.y + offset_y, 10, 15))
            pygame.draw.rect(screen, GRIS, (self.x + 5, self.y + offset_y, 10, 5))
            pygame.draw.circle(screen, BLANC, (self.x + 10, self.y + 7.5 + offset_y), 3, 1)

class Narrativa:
    def __init__(self, game, nivell, escenari, es_victoria=False):
        self.game = game
        self.nivell = nivell
        self.escenari = escenari
        self.es_victoria = es_victoria
        self.text_complet = self.get_text()
        self.text_mostrat = ""
        self.temps_caracter = 5
        self.temps_actual = 0
        self.efectes = []
        for _ in range(10):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            self.efectes.append(Efecte(x, y, 'narrativa', duracio=100))
        self.boto = Boto(WIDTH // 2 - 100, HEIGHT - 100, 200, 50, "Continuar", self.continuar)

    def get_text(self):
        if self.es_victoria:
            return (
                "Has derrotat el Comandant Suprem Xylothian! La Fortalesa Xylothian cau en ruïnes, "
                "tancant l'últim portal alienígena. La Terra està salvada gràcies a tu, Nexus. "
                "La humanitat pot reconstruir-se i viure en pau... almenys per ara."
            )
        if self.nivell == 0:
            if self.escenari == 0:
                return (
                    "Any 2147. Els Xylothians han envaït la Terra, deixant només ruïnes. Ets Nexus, l'últim soldat cibernètic. "
                    "La teva missió: infiltrar-te a les bases alienígenes. Comences a les ruïnes urbanes. Sobreviu."
                )
            elif self.escenari == 1:
                return (
                    "Has destruït una base Xylothian, però n'hi ha més. Els aliens reforcen les seves defenses. "
                    "Avances per les ruïnes, on els drons patrullen. Troba i elimina els seus lloctinents."
                )
            else:
                return (
                    "Un General Xylothian guarda l'última base urbana. La seva derrota obrirà el camí al següent sector. "
                    "Les teves armes són limitades, però la teva determinació és infinita. Endavant, Nexus."
                )
        elif self.nivell == 1:
            if self.escenari == 0:
                return (
                    "Has sortit de les ruïnes i entres a la Selva Tecnològica, un bioma alienígena ple de màquines orgàniques. "
                    "Els Xylothians experimenten aquí. Descobreix els seus secrets i destrueix-los."
                )
            elif self.escenari == 1:
                return (
                    "La selva és viva, amb trampes biològiques i criatures Xylothians. Has trobat un laboratori alienígena. "
                    "Destrueix les seves creacions abans que siguin alliberades contra la humanitat."
                )
            else:
                return (
                    "El Mestre de la Selva, un bio-constructor Xylothian, controla aquest sector. "
                    "Derrota'l per desactivar les defenses de la selva i apropar-te al bastió final."
                )
        else:
            if self.escenari == 0:
                return (
                    "La Fortalesa Xylothian és el bastió final. Muralles d'energia i legions d'elit et barraran el pas. "
                    "Infiltra't i debilita les seves defenses. El temps s'acaba, Nexus."
                )
            elif self.escenari == 1:
                return (
                    "Has trencat les defenses externes, però els Xylothians es reagrupen. Un comandant d'elit lidera la segona línia. "
                    "Elimina'l per accedir al cor de la fortalesa."
                )
            else:
                return (
                    "El Comandant Suprem Xylothian protegeix el cor de la fortalesa. Derrota'l per salvar la Terra. "
                    "Aquest és l'últim enfrontament, Nexus. La humanitat depèn de tu."
                )

    def continuar(self):
        self.game.estat = 'joc'
        self.game.inicialitzar_nivell()

    async def actualitzar(self):
        self.temps_actual += 1
        if self.temps_actual % self.temps_caracter == 0 and len(self.text_mostrat) < len(self.text_complet):
            self.text_mostrat += self.text_complet[len(self.text_mostrat)]
        for efecte_iter in self.efectes[:]:
            if efecte_iter.actualitzar():
                self.efectes.remove(efecte_iter)
                x = random.randint(0, WIDTH)
                y = random.randint(0, HEIGHT)
                self.efectes.append(Efecte(x, y, 'narrativa', duracio=100))

    def dibuixar(self):
        screen.fill(NEGRE)
        for i in range(0, WIDTH, 50):
            pygame.draw.line(screen, BLAU, (i, 0), (i, HEIGHT), 1)
        for i in range(0, HEIGHT, 50):
            pygame.draw.line(screen, BLAU, (0, i), (WIDTH, i), 1)
        for efecte_iter in self.efectes:
            efecte_iter.dibuixar()

        linies = []
        paraula_actual = ""
        for char in self.text_mostrat:
            if char == " ":
                linies.append(paraula_actual)
                paraula_actual = ""
            else:
                paraula_actual += char
        if paraula_actual:
            linies.append(paraula_actual)

        text_actual = ""
        ample_max = WIDTH - 100
        y = 150
        for paraula in linies:
            text_prova = text_actual + (" " if text_actual else "") + paraula
            ample = font_narrativa.size(text_prova)[0]
            if ample > ample_max:
                text_surf = font_narrativa.render(text_actual, True, BLANC)
                screen.blit(text_surf, (WIDTH // 2 - text_surf.get_width() // 2, y))
                y += 40
                text_actual = paraula
            else:
                text_actual = text_prova
        if text_actual:
            text_surf = font_narrativa.render(text_actual, True, BLANC)
            screen.blit(text_surf, (WIDTH // 2 - text_surf.get_width() // 2, y))

        self.boto.dibuixar()

class Derrota:
    def __init__(self, game):
        self.game = game
        self.text = "Has caigut en combat. Els Xylothians avancen. Què faràs, Nexus?"
        self.text_mostrat = ""
        self.temps_caracter = 5
        self.temps_actual = 0
        self.efectes = []
        for _ in range(10):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            self.efectes.append(Efecte(x, y, 'derrota', duracio=100))
        self.boto_menu = Boto(WIDTH // 2 - 200, HEIGHT - 100, 150, 50, "Menú", lambda: setattr(self.game, 'estat', 'menu'))
        self.boto_reintentar = Boto(WIDTH // 2 + 50, HEIGHT - 100, 150, 50, "Reintentar", self.reintentar)

    def reintentar(self):
        self.game.inicialitzar_nivell()
        self.game.estat = 'joc'

    async def actualitzar(self):
        self.temps_actual += 1
        if self.temps_actual % self.temps_caracter == 0 and len(self.text_mostrat) < len(self.text):
            self.text_mostrat += self.text[len(self.text_mostrat)]
        for efecte_iter in self.efectes[:]:
            if efecte_iter.actualitzar():
                self.efectes.remove(efecte_iter)
                x = random.randint(0, WIDTH)
                y = random.randint(0, HEIGHT)
                self.efectes.append(Efecte(x, y, 'derrota', duracio=100))

    def dibuixar(self):
        screen.fill(NEGRE)
        for i in range(0, WIDTH, 50):
            pygame.draw.line(screen, BLAU, (i, 0), (i, HEIGHT), 1)
        for i in range(0, HEIGHT, 50):
            pygame.draw.line(screen, BLAU, (0, i), (WIDTH, i), 1)
        for efecte_iter in self.efectes:
            efecte_iter.dibuixar()

        linies = []
        paraula_actual = ""
        for char in self.text_mostrat:
            if char == " ":
                linies.append(paraula_actual)
                paraula_actual = ""
            else:
                paraula_actual += char
        if paraula_actual:
            linies.append(paraula_actual)

        text_actual = ""
        ample_max = WIDTH - 100
        y = 150
        for paraula in linies:
            text_prova = text_actual + (" " if text_actual else "") + paraula
            ample = font_narrativa.size(text_prova)[0]
            if ample > ample_max:
                text_surf = font_narrativa.render(text_actual, True, BLANC)
                screen.blit(text_surf, (WIDTH // 2 - text_surf.get_width() // 2, y))
                y += 40
                text_actual = paraula
            else:
                text_actual = text_prova
        if text_actual:
            text_surf = font_narrativa.render(text_actual, True, BLANC)
            screen.blit(text_surf, (WIDTH // 2 - text_surf.get_width() // 2, y))

        self.boto_menu.dibuixar()
        self.boto_reintentar.dibuixar()

class Game:
    def __init__(self):
        self.estat = 'menu'
        self.jugador = Jugador()
        self.arma_actual = 0
        self.armes = [
            {'nom': 'Pistola', 'dany': 6, 'bales': 20, 'bales_max': 20, 'desbloquejada': True, 'cost': 0},
            {'nom': 'Fusell', 'dany': 12, 'bales': 15, 'bales_max': 15, 'desbloquejada': False, 'cost': 50},
            {'nom': 'Minigun', 'dany': 15, 'bales': float('inf'), 'bales_max': float('inf'), 'desbloquejada': False, 'cost': 100}
        ]
        self.habilitats = [
            {'nom': 'Escut', 'usos': 0, 'usos_max': 3, 'tecla': pygame.K_1},
            {'nom': 'Explosió Radial', 'usos': 0, 'usos_max': 3, 'tecla': pygame.K_2},
            {'nom': 'Regeneració', 'usos': 0, 'usos_max': 3, 'tecla': pygame.K_3}
        ]
        self.habilitats_desbloquejades = False  # Nueva variable para rastrear desbloqueo
        self.monedes = 0
        self.nivells_desbloquejats = [[True, False, False], [False, False, False], [False, False, False]]
        self.nivell_actual = 0
        self.escenari_actual = 0
        self.enemics = []
        self.bales = []
        self.bales_enemics = []
        self.items = []
        self.plataformes = []
        self.efectes = []
        self.menu_botons = []
        self.botiga_botons = []
        self.selector_botons = []
        self.temps_spawn_items = 0
        self.missatge_botiga = ""
        self.temps_missatge = 0
        self.missatge_selector = ""
        self.narrativa = None
        self.derrota = None
        self.item_count = 0  # Contador para alternar vida y munición
        self.max_items = 3  # Máximo de 3 items en pantalla
        self.inicialitzar_menu()

    def crear_accio_arma(self, index):
        def accio():
            self.seleccionar_arma(index)
        return accio

    def crear_accio_habilitat(self, index):
        def accio():
            self.comprar_habilitat(index)
        return accio

    def crear_accio_nivell(self, nivell, escenari):
        def accio():
            self.mostrar_narrativa(nivell, escenari)
        return accio

    def inicialitzar_menu(self):
        self.menu_botons = [
            Boto(WIDTH // 2 - 100, 200, 200, 50, 'Jugar', lambda: setattr(self, 'estat', 'selector')),
            Boto(WIDTH // 2 - 100, 270, 200, 50, 'Botiga', lambda: setattr(self, 'estat', 'botiga')),
            Boto(WIDTH // 2 - 100, 340, 200, 50, 'Guia', lambda: setattr(self, 'estat', 'guia')),
            Boto(WIDTH // 2 - 100, 410, 200, 50, 'Crèdits', lambda: setattr(self, 'estat', 'credits')),
            Boto(WIDTH // 2 - 100, 480, 200, 50, 'Sortir', lambda: setattr(self, 'estat', 'quit'))
        ]

    def inicialitzar_nivell(self):
        self.jugador = Jugador()
        self.armes[self.arma_actual]['bales'] = self.armes[self.arma_actual]['bales_max']
        self.enemics = []
        self.bales = []
        self.bales_enemics = []
        self.items = []
        self.efectes = []
        self.temps_spawn_items = 0
        self.item_count = 0  # Reiniciar contador de items
        if self.nivell_actual == 0:
            if self.escenari_actual == 0:
                self.plataformes = [
                    Plataforma(0, HEIGHT - 50, WIDTH, 50),
                    Plataforma(100, HEIGHT - 150, 150, 20),
                    Plataforma(300, HEIGHT - 250, 150, 20),
                    Plataforma(500, HEIGHT - 350, 150, 20)
                ]
                self.enemics.append(Enemic(WIDTH, random.randint(50, HEIGHT - 50), 30, nivell=self.nivell_actual))
                self.enemics.append(Enemic(0, random.randint(50, HEIGHT - 50), 30, nivell=self.nivell_actual))
                self.spawn_item_aleatori()  # Iniciar con un item de vida
            elif self.escenari_actual == 1:
                self.plataformes = [
                    Plataforma(0, HEIGHT - 50, WIDTH, 50),
                    Plataforma(150, HEIGHT - 150, 150, 20),
                    Plataforma(350, HEIGHT - 250, 150, 20),
                    Plataforma(550, HEIGHT - 200, 150, 20)
                ]
                self.enemics.append(Enemic(WIDTH, random.randint(50, HEIGHT - 50), 30, nivell=self.nivell_actual))
                self.enemics.append(Enemic(0, random.randint(50, HEIGHT - 50), 30, nivell=self.nivell_actual))
                self.enemics.append(Enemic(WIDTH, random.randint(50, HEIGHT - 50), 30, nivell=self.nivell_actual))
            else:
                self.plataformes = [
                    Plataforma(0, HEIGHT - 50, WIDTH, 50),
                    Plataforma(100, HEIGHT - 150, 150, 20),
                    Plataforma(300, HEIGHT - 250, 150, 20),
                    Plataforma(500, HEIGHT - 350, 150, 20)
                ]
                self.enemics.append(Enemic(WIDTH, random.randint(50, HEIGHT - 50), 100, es_boss=True, nivell=self.nivell_actual))
        elif self.nivell_actual == 1:
            if self.escenari_actual == 0:
                self.plataformes = [
                    Plataforma(0, HEIGHT - 50, WIDTH, 50),
                    Plataforma(150, HEIGHT - 150, 150, 20),
                    Plataforma(350, HEIGHT - 250, 200, 20),
                    Plataforma(550, HEIGHT - 350, 150, 20)
                ]
                self.enemics.append(Enemic(WIDTH, random.randint(50, HEIGHT - 50), 50, nivell=self.nivell_actual))
                self.enemics.append(Enemic(0, random.randint(50, HEIGHT - 50), 50, nivell=self.nivell_actual))
            elif self.escenari_actual == 1:
                self.plataformes = [
                    Plataforma(0, HEIGHT - 50, WIDTH, 50),
                    Plataforma(100, HEIGHT - 150, 150, 20),
                    Plataforma(300, HEIGHT - 250, 150, 20),
                    Plataforma(500, HEIGHT - 350, 150, 20)
                ]
                self.enemics.append(Enemic(WIDTH, random.randint(50, HEIGHT - 50), 50, nivell=self.nivell_actual))
                self.enemics.append(Enemic(0, random.randint(50, HEIGHT - 50), 50, nivell=self.nivell_actual))
                self.enemics.append(Enemic(WIDTH, random.randint(50, HEIGHT - 50), 50, nivell=self.nivell_actual))
            else:
                self.plataformes = [
                    Plataforma(0, HEIGHT - 50, WIDTH, 50),
                    Plataforma(150, HEIGHT - 150, 150, 20),
                    Plataforma(350, HEIGHT - 250, 150, 20),
                    Plataforma(550, HEIGHT - 350, 150, 20)
                ]
                self.enemics.append(Enemic(WIDTH, random.randint(50, HEIGHT - 50), 200, es_boss=True, nivell=self.nivell_actual))
                # Desbloqueo de habilidades al completar 1-3
                self.habilitats_desbloquejades = True
                for habilitat in self.habilitats:
                    habilitat['usos'] = habilitat['usos_max']
        else:
            if self.escenari_actual == 0:
                self.plataformes = [
                    Plataforma(0, HEIGHT - 50, WIDTH, 50),
                    Plataforma(100, HEIGHT - 150, 150, 20),
                    Plataforma(300, HEIGHT - 250, 150, 20),
                    Plataforma(500, HEIGHT - 350, 150, 20)
                ]
                self.enemics.append(Enemic(WIDTH, random.randint(50, HEIGHT - 50), 80, nivell=self.nivell_actual))
                self.enemics.append(Enemic(0, random.randint(50, HEIGHT - 50), 80, nivell=self.nivell_actual))
            elif self.escenari_actual == 1:
                self.plataformes = [
                    Plataforma(0, HEIGHT - 50, WIDTH, 50),
                    Plataforma(150, HEIGHT - 150, 150, 20),
                    Plataforma(350, HEIGHT - 250, 150, 20),
                    Plataforma(550, HEIGHT - 350, 150, 20)
                ]
                self.enemics.append(Enemic(WIDTH, random.randint(50, HEIGHT - 50), 80, nivell=self.nivell_actual))
                self.enemics.append(Enemic(0, random.randint(50, HEIGHT - 50), 80, nivell=self.nivell_actual))
                self.enemics.append(Enemic(WIDTH, random.randint(50, HEIGHT - 50), 80, nivell=self.nivell_actual))
            else:
                self.plataformes = [
                    Plataforma(0, HEIGHT - 50, WIDTH, 50),
                    Plataforma(100, HEIGHT - 150, 150, 20),
                    Plataforma(300, HEIGHT - 250, 150, 20),
                    Plataforma(500, HEIGHT - 350, 150, 20)
                ]
                self.enemics.append(Enemic(WIDTH, random.randint(50, HEIGHT - 50), 1200, es_boss_final=True, nivell=self.nivell_actual))

    def spawn_item_aleatori(self):
        if len(self.items) >= self.max_items:
            return
        plataformes_disponibles = [p for p in self.plataformes if p.rect.width > 50]
        if not plataformes_disponibles:
            return
        plataforma = random.choice(plataformes_disponibles)
        x = random.randint(plataforma.rect.x + 10, plataforma.rect.x + plataforma.rect.width - 30)
        y = plataforma.rect.y - 20
        tipus = 'vida' if self.item_count % 2 == 0 else 'bales'  # Alternar vida y munición
        self.items.append(Item(x, y, tipus))
        self.item_count += 1

    def dibuixar_menu(self):
        screen.fill(NEGRE)
        titol = font.render('Invasió Alienígena', True, BLANC)
        screen.blit(titol, (WIDTH // 2 - titol.get_width() // 2, 100))
        for boto in self.menu_botons:
            boto.dibuixar()
        text = font_small.render('Prem G per al menú', True, BLANC)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 50))

    def dibuixar_botiga(self):
        screen.fill(NEGRE)
        titol = font.render('Botiga', True, BLANC)
        screen.blit(titol, (WIDTH // 2 - titol.get_width() // 2, 50))
        monedes_text = font_small.render(f'Monedes: {self.monedes}', True, BLANC)
        screen.blit(monedes_text, (WIDTH // 2 - monedes_text.get_width() // 2, 100))

        armes_titol = font_small.render('Armes', True, BLANC)
        screen.blit(armes_titol, (WIDTH // 4 - armes_titol.get_width() // 2, 150))
        habilitats_titol = font_small.render('Habilitats', True, BLANC)
        screen.blit(habilitats_titol, (3 * WIDTH // 4 - habilitats_titol.get_width() // 2, 150))

        self.botiga_botons = []
        for i, arma in enumerate(self.armes):
            color = BLAU if arma['desbloquejada'] else VERMELL
            color_hover = VERMELL if arma['desbloquejada'] else TARONJA
            nom_boto = arma['nom']
            accio = self.crear_accio_arma(i)
            self.botiga_botons.append(Boto(WIDTH // 4 - 100, 180 + i * 60, 200, 50, nom_boto, accio, color, color_hover))

        for i, habilitat in enumerate(self.habilitats):
            if self.habilitats_desbloquejades:
                color = BLAU
                color_hover = VERMELL
                nom_boto = f"{habilitat['nom']} ({habilitat['usos']}/{habilitat['usos_max']})"
                accio = None  # No se necesita acción, ya que los usos se manejan en el juego
            else:
                color = GRIS
                color_hover = TARONJA
                nom_boto = 'Desbloquejat al Nivell 1-3'
                accio = lambda: self.mostrar_missatge_botiga("Habilitats desbloquejades al completar el Nivell 1-3")
            self.botiga_botons.append(Boto(3 * WIDTH // 4 - 100, 180 + i * 60, 200, 50, nom_boto, accio, color, color_hover))

        for i, boto in enumerate(self.botiga_botons):
            boto.dibuixar()
            if i < len(self.armes):
                if not self.armes[i]['desbloquejada']:
                    cost_text = font_small.render(f'Cost: {self.armes[i]["cost"]}', True, VERMELL)
                    screen.blit(cost_text, (WIDTH // 4 + 110, 190 + i * 60))
                if self.armes[i]['desbloquejada']:
                    status_text = font_small.render('Desbloquejat', True, VERD)
                    screen.blit(status_text, (WIDTH // 4 + 110, 210 + i * 60))

        if self.missatge_botiga:
            missatge_text = font_small.render(self.missatge_botiga, True, VERMELL)
            screen.blit(missatge_text, (WIDTH // 2 - missatge_text.get_width() // 2, HEIGHT - 80))
            self.temps_missatge -= 1
            if self.temps_missatge <= 0:
                self.missatge_botiga = ""

        text = font_small.render('Prem ESC per tornar', True, BLANC)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 50))

    def mostrar_missatge_botiga(self, missatge):
        self.missatge_botiga = missatge
        self.temps_missatge = 120

    def mostrar_missatge_selector(self, missatge):
        self.missatge_selector = missatge
        self.temps_missatge = 120

    def seleccionar_arma(self, index):
        if index >= len(self.armes):
            return
        arma = self.armes[index]
        if not arma['desbloquejada']:
            if self.monedes >= arma['cost']:
                self.monedes -= arma['cost']
                arma['desbloquejada'] = True
                self.mostrar_missatge_botiga(f"{arma['nom']} desbloquejat!")
            else:
                self.mostrar_missatge_botiga("No tens prou monedes!")
                return
        self.arma_actual = index

    def comprar_habilitat(self, index):
        if not self.habilitats_desbloquejades:
            self.mostrar_missatge_botiga("Habilitats desbloquejades al completar el Nivell 1-3")
            return
        # Las habilidades ya están desbloqueadas y con usos máximos, no se necesita comprar

    @staticmethod
    def dibuixar_guia():
        screen.fill(NEGRE)
        titol = font.render('Guia de Controls', True, BLANC)
        screen.blit(titol, (WIDTH // 2 - titol.get_width() // 2, 100))
        controls = [
            'A, D: Moure esquerra/dreta',
            'ESPAC: Saltar',
            'Clic esquerre: Disparar',
            '1: Activar Escut',
            '2: Activar Explosió Radial',
            '3: Activar Regeneració',
            'G: Tornar al menú'
        ]
        for i, control in enumerate(controls):
            text = font_small.render(control, True, BLANC)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 200 + i * 40))
        text = font_small.render('Prem ESC per tornar', True, BLANC)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 50))

    @staticmethod
    def dibuixar_credits():
        screen.fill(NEGRE)
        titol = font.render('Crèdits', True, BLANC)
        screen.blit(titol, (WIDTH // 2 - titol.get_width() // 2, 100))
        credits_list = [
            'Joc creat per Nacho i Abel',
            'Programació: Nacho i Abel',
            'Disseny de joc: Nacho i Abel',
            'Gràfics: Nacho i Abel',
            'Música i efectes: Nacho i Abel',
            'Producció: Nacho i Abel',
            'Gràcies per jugar!'
        ]
        for i, credit in enumerate(credits_list):
            text = font_small.render(credit, True, BLANC)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 200 + i * 40))
        text = font_small.render('Prem ESC per tornar', True, BLANC)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 50))

    def dibuixar_selector(self):
        screen.fill(NEGRE)
        titol = font.render('Selecciona Nivell', True, BLANC)
        screen.blit(titol, (WIDTH // 2 - titol.get_width() // 2, 50))

        self.selector_botons = []
        for nivell in range(3):
            for escenari in range(3):
                x = WIDTH // 4 + (escenari * 200)
                y = 150 + (nivell * 100)
                text = f'{nivell + 1}-{escenari + 1}' if self.nivells_desbloquejats[nivell][escenari] else '?'
                accio = self.crear_accio_nivell(nivell, escenari) if self.nivells_desbloquejats[nivell][escenari] else None
                color = GRIS if not self.nivells_desbloquejats[nivell][escenari] else BLAU
                self.selector_botons.append(Boto(x - 50, y, 100, 50, text, accio, color))

        for boto in self.selector_botons:
            boto.dibuixar()

        if hasattr(self, 'missatge_selector') and self.missatge_selector:
            missatge_text = font_small.render(self.missatge_selector, True, VERMELL)
            screen.blit(missatge_text, (WIDTH // 2 - missatge_text.get_width() // 2, HEIGHT - 80))
            self.temps_missatge -= 1
            if self.temps_missatge <= 0:
                self.missatge_selector = ""

        text = font_small.render('Prem ESC per tornar', True, BLANC)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 50))

    def mostrar_narrativa(self, nivell, escenari):
        self.nivell_actual = nivell
        self.escenari_actual = escenari
        self.nivells_desbloquejats[nivell][escenari] = True  # Asegura que el nivel actual quede desbloqueado
        self.narrativa = Narrativa(self, nivell, escenari)
        self.estat = 'narrativa'

    def mostrar_narrativa_victoria(self):
        self.narrativa = Narrativa(self, self.nivell_actual, self.escenari_actual, es_victoria=True)
        self.estat = 'victoria'

    def mostrar_derrota(self):
        self.derrota = Derrota(self)
        self.estat = 'derrota'

    def desbloquejar_seguent_nivell(self):
        # Desbloquea el escenario actual permanentemente
        self.nivells_desbloquejats[self.nivell_actual][self.escenari_actual] = True
        # Desbloquea el siguiente escenario o nivel
        if self.escenari_actual < 2:
            self.nivells_desbloquejats[self.nivell_actual][self.escenari_actual + 1] = True
        elif self.nivell_actual < 2:
            self.nivells_desbloquejats[self.nivell_actual + 1][0] = True

    def actualitzar_joc(self):
        if self.jugador.vida <= 0:
            self.mostrar_derrota()
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.estat = 'quit'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    self.estat = 'menu'
                elif event.key == pygame.K_1 and self.habilitats[0]['usos'] > 0 and not self.jugador.escut_actiu:
                    self.habilitats[0]['usos'] -= 1
                    self.jugador.escut_actiu = True
                    self.jugador.temps_escut = 300
                    self.efectes.append(Efecte(self.jugador.x + self.jugador.width / 2, self.jugador.y + self.jugador.height / 2, 'escut'))
                elif event.key == pygame.K_2 and self.habilitats[1]['usos'] > 0:
                    self.habilitats[1]['usos'] -= 1
                    for angle in range(0, 360, 30):
                        rad = math.radians(angle)
                        vx = math.cos(rad) * 10
                        vy = math.sin(rad) * 10
                        self.bales.append(Bala(self.jugador.x + self.jugador.width / 2, self.jugador.y + self.jugador.height / 2, vx, vy, dany=20))
                    self.efectes.append(Efecte(self.jugador.x + self.jugador.width / 2, self.jugador.y + self.jugador.height / 2, 'radial'))
                elif event.key == pygame.K_3 and self.habilitats[2]['usos'] > 0:
                    self.habilitats[2]['usos'] -= 1
                    self.jugador.vida = min(self.jugador.vida + 20, 100)
                    self.efectes.append(Efecte(self.jugador.x + self.jugador.width / 2, self.jugador.y + self.jugador.height / 2, 'regen'))
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.armes[self.arma_actual]['bales'] > 0 or self.armes[self.arma_actual]['nom'] == 'Minigun':
                    mouse_pos = pygame.mouse.get_pos()
                    dx = mouse_pos[0] - (self.jugador.x + self.jugador.width / 2)
                    dy = mouse_pos[1] - (self.jugador.y + self.jugador.height / 2)
                    dist = max(math.sqrt(dx ** 2 + dy ** 2), 1)
                    vx = (dx / dist) * 10
                    vy = (dy / dist) * 10
                    tipus_arma = self.armes[self.arma_actual]['nom'].lower()
                    if tipus_arma == 'minigun':
                        tipus_arma = 'minigun'
                    self.bales.append(Bala(self.jugador.x + self.jugador.width / 2, self.jugador.y + self.jugador.height / 2, vx, vy, tipus_arma, self.armes[self.arma_actual]['dany']))
                    if self.armes[self.arma_actual]['nom'] != 'Minigun':
                        self.armes[self.arma_actual]['bales'] -= 1
                    self.efectes.append(Efecte(self.jugador.x + self.jugador.width / 2, self.jugador.y + self.jugador.height / 2, 'dispar'))

        keys = pygame.key.get_pressed()
        self.jugador.moure(keys[pygame.K_a], keys[pygame.K_d], keys[pygame.K_SPACE])

        if self.jugador.escut_actiu:
            self.jugador.temps_escut -= 1
            if self.jugador.temps_escut <= 0:
                self.jugador.escut_actiu = False

        for enemic in self.enemics[:]:
            bales_enemic = enemic.actualitzar(self.jugador, self.enemics)
            self.bales_enemics.extend(bales_enemic)
            if enemic.vida <= 0:
                self.enemics.remove(enemic)
                self.efectes.append(Efecte(enemic.x + enemic.width / 2, enemic.y + enemic.height / 2, 'explosio'))
                self.monedes += (10 * 5) if not enemic.es_boss and not enemic.es_boss_final else (50 * 5) if enemic.es_boss else (100 * 5)

        for bala in self.bales[:]:
            bala.actualitzar()
            if bala.x < 0 or bala.x > WIDTH or bala.y < 0 or bala.y > HEIGHT:
                self.bales.remove(bala)
                continue
            for enemic in self.enemics[:]:
                if pygame.Rect(enemic.x, enemic.y, enemic.width, enemic.height).colliderect(pygame.Rect(bala.x, bala.y, bala.width, bala.height)):
                    enemic.vida -= bala.dany
                    self.bales.remove(bala)
                    self.efectes.append(Efecte(enemic.x + enemic.width / 2, enemic.y + enemic.height / 2, 'dany'))
                    break

        for bala in self.bales_enemics[:]:
            bala.actualitzar()
            if bala.x < 0 or bala.x > WIDTH or bala.y < 0 or bala.y > HEIGHT:
                self.bales_enemics.remove(bala)
                continue
            if pygame.Rect(self.jugador.x, self.jugador.y, self.jugador.width, self.jugador.height).colliderect(pygame.Rect(bala.x, bala.y, bala.width, bala.height)):
                if not self.jugador.escut_actiu:
                    self.jugador.vida -= bala.dany
                    self.efectes.append(Efecte(self.jugador.x + self.jugador.width / 2, self.jugador.y + self.jugador.height / 2, 'dany'))
                self.bales_enemics.remove(bala)

        for item_iter in self.items[:]:
            if pygame.Rect(self.jugador.x, self.jugador.y, self.jugador.width, self.jugador.height).colliderect(pygame.Rect(item_iter.x, item_iter.y, item_iter.width, item_iter.height)):
                if item_iter.tipus == 'vida' and self.jugador.vida < 100:
                    self.jugador.vida = min(self.jugador.vida + 20, 100)
                    self.efectes.append(Efecte(item_iter.x + item_iter.width / 2, item_iter.y + item_iter.height / 2, 'item'))
                    self.items.remove(item_iter)
                    self.spawn_item_aleatori()  # Reaparece otro item
                elif item_iter.tipus == 'bales' and self.armes[self.arma_actual]['bales'] < self.armes[self.arma_actual]['bales_max']:
                    self.armes[self.arma_actual]['bales'] = self.armes[self.arma_actual]['bales_max']
                    self.efectes.append(Efecte(item_iter.x + item_iter.width / 2, item_iter.y + item_iter.height / 2, 'item'))
                    self.items.remove(item_iter)
                    self.spawn_item_aleatori()  # Reaparece otro item

        self.temps_spawn_items += 1
        if self.temps_spawn_items >= 300 and len(self.items) < self.max_items:
            self.temps_spawn_items = 0
            self.spawn_item_aleatori()

        for plataforma_iter in self.plataformes:
            if (plataforma_iter.rect.x < self.jugador.x + self.jugador.width and
                self.jugador.x < plataforma_iter.rect.x + plataforma_iter.rect.width and
                plataforma_iter.rect.y < self.jugador.y + self.jugador.height and
                self.jugador.y + self.jugador.height < plataforma_iter.rect.y + plataforma_iter.rect.height + self.jugador.vy):
                self.jugador.y = plataforma_iter.rect.y - self.jugador.height
                self.jugador.vy = 0
                self.jugador.terra = True

        for efecte_iter in self.efectes[:]:
            if efecte_iter.actualitzar():
                self.efectes.remove(efecte_iter)

        if not self.enemics:
            self.desbloquejar_seguent_nivell()
            if self.nivell_actual == 2 and self.escenari_actual == 2:
                self.mostrar_narrativa_victoria()
            elif self.escenari_actual == 2:
                self.dibuixar_selector()
            else:
                self.escenari_actual += 1
                self.inicialitzar_nivell()

    def dibuixar_joc(self):
        key = (self.nivell_actual, self.escenari_actual)
        fons = fons_nivells.get(key, None)
        if fons:
            screen.blit(fons, (0, 0))
        else:
            screen.fill(NEGRE)

        for plataforma_iter in self.plataformes:
            plataforma_iter.dibuixar()
        for item_iter in self.items:
            item_iter.dibuixar()
        for enemic_iter in self.enemics:
            enemic_iter.dibuixar()
        for bala_iter in self.bales:
            bala_iter.dibuixar()
        for bala_enemic_iter in self.bales_enemics:
            bala_enemic_iter.dibuixar()
        self.jugador.dibuixar(self.armes[self.arma_actual]['nom'])
        for efecte_iter in self.efectes:
            efecte_iter.dibuixar()

        # Mostrar habilidades arriba en el centro
        y_offset = 10
        for i, habilitat in enumerate(self.habilitats):
            text = font_small.render(f"{habilitat['nom']}: {habilitat['usos']}/{habilitat['usos_max']}", True, BLANC)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y_offset))
            y_offset += 30

        arma_text = font_small.render(f'arma: {self.armes[self.arma_actual]["nom"]}', True, BLANC)
        bales_text = font_small.render(f'Bales: {self.armes[self.arma_actual]["bales"]}', True, BLANC)
        screen.blit(arma_text, (10, 50))
        screen.blit(bales_text, (10, 80))

    async def dibuixar_derrota(self):
        await self.derrota.actualitzar()
        self.derrota.dibuixar()

    async def main(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.estat = 'quit'
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.estat == 'menu':
                        for boto in self.menu_botons:
                            boto.clic()
                    elif self.estat == 'botiga':
                        for boto in self.botiga_botons:
                            boto.clic()
                    elif self.estat == 'selector':
                        for boto in self.selector_botons:
                            boto.clic()
                    elif self.estat == 'narrativa' or self.estat == 'victoria':
                        self.narrativa.boto.clic()
                    elif self.estat == 'derrota':
                        self.derrota.boto_menu.clic()
                        self.derrota.boto_reintentar.clic()
                    elif self.estat == 'joc':
                        if self.armes[self.arma_actual]['bales'] > 0 or self.armes[self.arma_actual]['nom'] == 'Minigun':
                            mouse_pos = pygame.mouse.get_pos()
                            dx = mouse_pos[0] - (self.jugador.x + self.jugador.width / 2)
                            dy = mouse_pos[1] - (self.jugador.y + self.jugador.height / 2)
                            dist = max(math.sqrt(dx ** 2 + dy ** 2), 1)
                            vx = (dx / dist) * 10
                            vy = (dy / dist) * 10
                            tipus_arma = self.armes[self.arma_actual]['nom'].lower()
                            if tipus_arma == 'minigun':
                                tipus_arma = 'minigun'
                            self.bales.append(Bala(self.jugador.x + self.jugador.width / 2, self.jugador.y + self.jugador.height / 2, vx, vy, tipus_arma, self.armes[self.arma_actual]['dany']))
                            if self.armes[self.arma_actual]['nom'] != 'Minigun':
                                self.armes[self.arma_actual]['bales'] -= 1
                            self.efectes.append(Efecte(self.jugador.x + self.jugador.width / 2, self.jugador.y + self.jugador.height / 2, 'dispar'))
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_g:
                        self.estat = 'menu'
                    elif event.key == pygame.K_ESCAPE:
                        if self.estat in ['botiga', 'guia', 'credits', 'selector']:
                            self.estat = 'menu'

            if self.estat == 'menu':
                self.dibuixar_menu()
            elif self.estat == 'botiga':
                self.dibuixar_botiga()
            elif self.estat == 'guia':
                self.dibuixar_guia()
            elif self.estat == 'credits':
                self.dibuixar_credits()
            elif self.estat == 'selector':
                self.dibuixar_selector()
            elif self.estat == 'narrativa':
                await self.narrativa.actualitzar()
                self.narrativa.dibuixar()
            elif self.estat == 'joc':
                self.actualitzar_joc()
                self.dibuixar_joc()
            elif self.estat == 'derrota':
                await self.dibuixar_derrota()
            elif self.estat == 'victoria':
                await self.narrativa.actualitzar()
                self.narrativa.dibuixar()
                if self.narrativa.temps_actual > 600:
                    self.inicialitzar_menu()
                    self.estat = 'menu'
            elif self.estat == 'quit':
                break

            pygame.display.flip()
            clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    asyncio.run(game.main())
