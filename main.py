import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *
from navire import *
from random import *
from pygame import mixer


#choisi au hasard les navires ennemis
lst_navire=[(Destroyer("ijn","Ayanami",1000,20000,[3,16,14],38,[127,150,6],[610,4,9])),(Cuirasse("uss","Iowa",9000,20000,[307,500,10],33,[406,9,35],[127,20,25],[False])),(Cuirasse("uss","New Jersey",9000,20000,[307,500,10],33,[406,9,35],[127,20,25],[False])),(Croiseur('uss',"Saint Louis",5000,15000,[127,152,5],32.5,[152,15,17],[127,8,13],[False])),(Croiseur("uss","Atlanta",4500,7500,[95,32,64],32.5,[127,16,17],[28,12,10],[True,533,4,8])),(Destroyer("uss","William D. Porter",2500,5000,[10,10,10],35,[127,5,17],[533,4,10])),(Croiseur("hms","Hood",6000,17500,[305,381,25],32,[381,8,27],[140,12,17],[False]))]
i1=randint(0,len(lst_navire)-1)
i2=randint(0,len(lst_navire)-1)
if i1==i2:
    while i1==i2:
        i2=randint(0,len(lst_navire)-1)
i3=randint(0,len(lst_navire)-1)
if i1==i3 or i2==i3:
    while i1==i3 or i3==i2:
        i3=randint(0,len(lst_navire)-1)
i4=randint(0,len(lst_navire)-1)
if i1==i4 or i2==i4 or i3==i4:
    while i1==i4 or i2==i4 or i3==i4:
        i4=randint(0,len(lst_navire)-1)
#initialise les navires
navire_joueur=(Cuirasse("ijn","Mikasa",5000,40000,[280,280,20],28,[305,6,30],[76,20,15],[True,457,3,5]))
navire_ennemi_1=lst_navire[i1]
navire_ennemi_2=lst_navire[i2]
navire_ennemi_3=lst_navire[i3]
navire_ennemi_4=lst_navire[i4]

#listes contenants les articles du magasin
blindage=[[409,650,20,20000,10000],[320,360,30,10000,7500],[305,279,15,10000,80000],[457,800,80,30000,12500]]
lst_bp=[[460,9,40,30000],[356,12,25,15000],[410,10,28,25000],[410,8,31,20000],[510,9,45,50000]]
lst_bs=[[155,12,27,7500],[140,20,25,8000],[152,16,26,10000],[75,30,15,5000]]
lst_torp=[[True,457,3,5,10000],[True,533,3,6,15000],[True,500,3,6,15000],[False]]

#règle la musique
pg.mixer.init()
music=pg.mixer.music.load("A_Change_in_Course.mp3")
pg.mixer.music.play(-1)

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        self.affiche_texte=0
        self.mode_achat=0
        self.mode_achat_bp=0
        self.mode_achat_bs=0
        self.mode_achat_torp=0
        self.mode_achat_blindage=0


    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        self.map = Map(path.join(game_folder, 'map3.txt'))
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.player_img=pg.transform.scale(self.player_img,(TILESIZE,TILESIZE))
        self.wall_img = pg.image.load(path.join(img_folder, wall_img)).convert_alpha()
        self.wall_img=pg.transform.scale(self.wall_img,(TILESIZE,TILESIZE))
        self.dock_img = pg.image.load(path.join(img_folder, dock_img)).convert_alpha()
        self.dock_img=pg.transform.scale(self.dock_img,(TILESIZE,TILESIZE))
        self.ennemi_img= pg.image.load(path.join(img_folder, ennemi_img)).convert_alpha()
        self.ennemi_img=pg.transform.scale(self.ennemi_img,(TILESIZE,TILESIZE))


    def new(self):
        # initialise les variables
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.ennemi=pg.sprite.Group()
        self.ennemi_1=pg.sprite.Group()
        self.ennemi_2=pg.sprite.Group()
        self.ennemi_3=pg.sprite.Group()
        self.ennemi_4=pg.sprite.Group()
        self.port=pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile=='2':
                    Limite(self,col,row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile=='E':
                    self.ennemi_1=Ennemi(self,col,row)
                if tile=='D':
                    self.port=Port(self,col,row)
                if tile=='M':
                    self.ennemi_2=(Ennemi(self,col,row))
                if tile=='O':
                    self.ennemi_3=(Ennemi(self,col,row))
                if tile=='F':
                    self.ennemi_4=(Ennemi(self,col,row))

        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        # la boucle principale du jeu
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update les sprites et la caméra
        self.all_sprites.update()
        self.camera.update(self.player)
    """
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))"""

    def draw(self):
        self.screen.fill(BGCOLOR)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()


    def events(self):
        #tous les evenements
        if navire_joueur.navire_coule==True:
            self.playing=False
        elif navire_ennemi_1.navire_coule==True and navire_ennemi_2.navire_coule==True and navire_ennemi_3.navire_coule==True and navire_ennemi_4.navire_coule==True:
            self.playing=False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_LEFT:
                    self.player.move(dx=-1)
                if event.key == pg.K_RIGHT:
                    self.player.move(dx=1)
                if event.key == pg.K_UP:
                    self.player.move(dy=-1)
                if event.key == pg.K_DOWN:
                    self.player.move(dy=1)
                if self.player.x==self.ennemi_1.ex:
                    if self.player.y==self.ennemi_1.ey:
                        distance=10000
                        joueur=navire_joueur
                        ennemi=navire_ennemi_1
                        etat_joueur=joueur.a_coule()
                        etat_ennemi=ennemi.a_coule()
                        while etat_joueur==False and etat_ennemi==False:
                            if distance>2000:
                                distance=distance-(joueur.vitesse*10+ennemi.vitesse*10)
                            print("la distance qui sépare le",str(joueur.prefixe),str(joueur.nom),"du",str(ennemi.prefixe),str(ennemi.nom),"est",distance)
                            joueur.combat(ennemi,distance)
                            ennemi.combat(joueur,distance)
                            etat_joueur=joueur.a_coule()
                            etat_ennemi=ennemi.a_coule()
                            if etat_ennemi==True:
                                navire_joueur.budget+=navire_ennemi_1.budget
                                print("vous avez gagnez",navire_ennemi_1.budget,"€ en battant vorte adversaire votre budget est maintenant de",navire_joueur.budget,"€")
                            print("il reste",ennemi.ps,"ps a votre ennemi")
                            print("il vous reste",joueur.ps,"ps")

                if self.player.x==self.ennemi_2.ex:
                    if self.player.y==self.ennemi_2.ey:
                        distance=10000
                        joueur=navire_joueur
                        ennemi=navire_ennemi_2
                        etat_joueur=joueur.a_coule()
                        etat_ennemi=ennemi.a_coule()
                        while etat_joueur==False and etat_ennemi==False:
                            if distance>2000:
                                distance=distance-(joueur.vitesse*10+ennemi.vitesse*10)
                            print("la distance qui sépare le",str(joueur.prefixe),str(joueur.nom),"du",str(ennemi.prefixe),str(ennemi.nom),"est",distance)
                            joueur.combat(ennemi,distance)
                            ennemi.combat(joueur,distance)
                            etat_joueur=joueur.a_coule()
                            etat_ennemi=ennemi.a_coule()
                            if etat_ennemi==True:
                                navire_joueur.budget+=navire_ennemi_2.budget
                                print("vous avez gagnez",navire_ennemi_2.budget,"€ en battant vorte adversaire votre budget est maintenant de",navire_joueur.budget,"€")
                            print("il reste",ennemi.ps,"ps a votre ennemi")
                            print("il vous reste",joueur.ps,"ps")
                if self.player.x==self.ennemi_3.ex:
                    if self.player.y==self.ennemi_3.ey:
                        distance=10000
                        joueur=navire_joueur
                        ennemi=navire_ennemi_3
                        etat_joueur=joueur.a_coule()
                        etat_ennemi=ennemi.a_coule()
                        while etat_joueur==False and etat_ennemi==False:
                            if distance>2000:
                                distance=distance-(joueur.vitesse*10+ennemi.vitesse*10)
                            print("la distance qui sépare le",str(joueur.prefixe),str(joueur.nom),"du",str(ennemi.prefixe),str(ennemi.nom),"est",distance)
                            joueur.combat(ennemi,distance)
                            ennemi.combat(joueur,distance)
                            etat_joueur=joueur.a_coule()
                            etat_ennemi=ennemi.a_coule()
                            if etat_ennemi==True:
                                navire_joueur.budget+=navire_ennemi_3.budget
                                print("vous avez gagnez",navire_ennemi_3.budget,"€ en battant vorte adversaire votre budget est maintenant de",navire_joueur.budget,"€")
                            print("il reste",ennemi.ps,"ps a votre ennemi")
                            print("il vous reste",joueur.ps,"ps")
                if self.player.x==self.ennemi_4.ex:
                    if self.player.y==self.ennemi_4.ey:
                        distance=10000
                        joueur=navire_joueur
                        ennemi=navire_ennemi_4
                        etat_joueur=joueur.a_coule()
                        etat_ennemi=ennemi.a_coule()
                        while etat_joueur==False and etat_ennemi==False:
                            if distance>2000:
                                distance=distance-(joueur.vitesse*10+ennemi.vitesse*10)
                            print("la distance qui sépare le",str(joueur.prefixe),str(joueur.nom),"du",str(ennemi.prefixe),str(ennemi.nom),"est",distance)
                            joueur.combat(ennemi,distance)
                            ennemi.combat(joueur,distance)
                            etat_joueur=joueur.a_coule()
                            etat_ennemi=ennemi.a_coule()
                            if etat_ennemi==True:
                                navire_joueur.budget+=navire_ennemi_4.budget
                                print("vous avez gagnez",navire_ennemi_4.budget,"€ en battant vorte adversaire votre budget est maintenant de",navire_joueur.budget,"€")
                            print("il reste",ennemi.ps,"ps a votre ennemi")
                            print("il vous reste",joueur.ps,"ps")

                if self.player.x==self.port.px:
                    if self.player.y==self.port.py:
                        if self.affiche_texte==0:
                            print("vous êtes au port que souhaites vous faire :")
                            print("appuyez sur 'a' pour réparer votre navire (si votre budget le permet)")
                            print("appuyez sur 'q' pour voir la liste des améliorations que vous pouvez faire a votre navire")
                            print("il vous reste",navire_joueur.budget,"€")
                            self.affiche_texte+=1
                            if navire_joueur.ps<0:
                                print("réparation impossible")
                            else:
                                print("les réparations vous couterons",str((navire_joueur.ps_max-navire_joueur.ps)*5))
                                print(navire_joueur.ps_max)
                        if event.key==pg.K_q:
                            if navire_joueur.ps!=navire_joueur.ps_max:
                                if (navire_joueur.ps_max-navire_joueur.ps)*5<=navire_joueur.budget:
                                    navire_joueur.ps=navire_joueur.ps_max
                                    navire_joueur.budget=navire_joueur.budget-((navire_joueur.ps_max-navire_joueur.ps)*5)
                                    print("votre navire a été réparer vos ps sont maintenant à",navire_joueur.ps)
                                    print("il vous reste maintenant",str(navire_joueur.budget),"€")
                            else:
                                    print("votre navire n'a pas besoin de réparation")
                            self.affiche_texte=0
                        if event.key==pg.K_a:
                            self.mode_achat=1
                            print("appuyez sur 's' pour changer de batterie principale")
                            print("appuyez sur 'd' pour changer de batterie secondaire")
                            print("appuyez sur 'f' pour modifié les torpilles")
                            print("appuyez sur 'g' pour changer la configuration du blindage")
                        if event.key==pg.K_s:
                            if self.mode_achat==1:
                                self.mode_achat_bp=1
                                print("entrez 'w' pour acheter des batteries principales de",lst_bp[0][1],"canons et d'un calibre de",lst_bp[0][0],"mm et d'un portée de",lst_bp[0][2]*100,"m cette équipement coutera",lst_bp[0][3],"€")
                                print("entrez 'x' pour acheter des batteries principales de",lst_bp[1][1],"canons et d'un calibre de",lst_bp[1][0],"mm et d'un portée de",lst_bp[1][2]*100,"m cette équipement coutera",lst_bp[1][3],"€")
                                print("entrez 'c' pour acheter des batteries principales de",lst_bp[2][1],"canons et d'un calibre de",lst_bp[2][0],"mm et d'un portée de",lst_bp[2][2]*100,"m cette équipement coutera",lst_bp[2][3],"€")
                                print("entrez 'v' pour acheter des batteries principales de",lst_bp[3][1],"canons et d'un calibre de",lst_bp[3][0],"mm et d'un portée de",lst_bp[3][2]*100,"m cette équipement coutera",lst_bp[3][3],"€")
                                print("entrez 'b' pour acheter des batteries principales de",lst_bp[4][1],"canons et d'un calibre de",lst_bp[4][0],"mm et d'un portée de",lst_bp[4][2]*100,"m cette équipement coutera",lst_bp[4][3],"€")
                                self.mode_achat_bs=0
                                self.mode_achat_torp=0
                                self.mode_achat_blindage=0
                        if event.key==pg.K_d:
                            if self.mode_achat==1:
                                self.mode_achat_bs=1
                                print("entrez 'w' pour acheter des batteries secondaires de",lst_bs[0][1],"canons et d'un calibre de",lst_bs[0][0],"mm et d'un portée de",lst_bs[0][2]*100,"m cette équipement coutera",lst_bs[0][3],"€")
                                print("entrez 'x' pour acheter des batteries secondaires de",lst_bs[1][1],"canons et d'un calibre de",lst_bs[1][0],"mm et d'un portée de",lst_bs[1][2]*100,"m cette équipement coutera",lst_bs[1][3],"€")
                                print("entrez 'c' pour acheter des batteries secondaires de",lst_bs[2][1],"canons et d'un calibre de",lst_bs[2][0],"mm et d'un portée de",lst_bs[2][2]*100,"m cette équipement coutera",lst_bs[2][3],"€")
                                print("entrez 'v' pour acheter des batteries secondaires de",lst_bs[3][1],"canons et d'un calibre de",lst_bs[3][0],"mm et d'un portée de",lst_bs[3][2]*100,"m cette équipement coutera",lst_bs[3][3],"€")
                                self.mode_achat_bp=0
                                self.mode_achat_torp=0
                                self.mode_achat_blindage=0
                        if event.key==pg.K_f:
                            if self.mode_achat==1:
                                self.mode_achat_torp=1
                                print("entrez 'w' pour acheter ",lst_torp[0][3],"tubes lances torpilles d'un calibre de",lst_torp[0][1],"mm et d'un portée de",lst_bs[0][2]*100,"m cette équipement coutera",lst_torp[0][4],"€")
                                print("entrez 'x' pour acheter ",lst_torp[1][3],"tubes lances torpilles d'un calibre de",lst_torp[1][1],"mm et d'un portée de",lst_bs[1][2]*100,"m cette équipement coutera",lst_torp[1][4],"€")
                                print("entrez 'c' pour acheter ",lst_torp[2][3],"tubes lances torpilles d'un calibre de",lst_torp[2][1],"mm et d'un portée de",lst_bs[2][2]*100,"m cette équipement coutera",lst_torp[2][4],"€")
                                print("entrez 'v' pour retirer les torpilles déjà installé (cette option n'est pas obligatoire pour changer de torpille)")
                                self.mode_achat_bp=0
                                self.mode_achat_bs=0
                                self.mode_achat_blindage=0
                        if event.key==pg.K_g:
                            if self.mode_achat==1:
                                self.mode_achat_blindage=1
                                print("entrez 'w' pour acheter un blindage de ceinture de",blindage[0][0],"un blindage aux tourelles de",blindage[0][1],"et un blindage a la super structure de",blindage[0][2],"ce blinadage vous coutera",blindage[0][3],"€")
                                print("entrez 'x' pour acheter un blindage de ceinture de",blindage[1][0],"un blindage aux tourelles de",blindage[1][1],"et un blindage a la super structure de",blindage[1][2],"ce blinadage vous coutera",blindage[1][3],"€")
                                print("entrez 'c' pour acheter un blindage de ceinture de",blindage[2][0],"un blindage aux tourelles de",blindage[2][1],"et un blindage a la super structure de",blindage[2][2],"ce blinadage vous coutera",blindage[2][3],"€")
                                print("entrez 'v' pour acheter un blindage de ceinture de",blindage[3][0],"un blindage aux tourelles de",blindage[3][1],"et un blindage a la super structure de",blindage[3][2],"ce blinadage vous coutera",blindage[3][3],"€")
                                self.mode_achat_bp=0
                                self.mode_achat_bs=0
                                self.mode_achat_torp=0

                        if event.key==pg.K_z:
                            if self.mode_achat==1:
                                if self.mode_achat_bp==1:
                                    if navire_joueur.budget>=lst_bp[0][3]:
                                        navire_joueur.change_bp(lst_bp[0])
                                        print("votre batterie principale a été modifié")
                                        navire_joueur.budget-=lst_bp[0][3]
                                    else:
                                        print("vous n'avez pas assez d'argent")
                                if self.mode_achat_bs==1:
                                    if navire_joueur.budget>=lst_bs[0][3]:
                                        navire_joueur.change_bs(lst_bs[0])
                                        print("vos batteries secondaires a été modifié")
                                        navire_joueur.budget-=lst_bs[0][3]
                                    else:
                                        print("vous n'avez pas assez d'argent")
                                if self.mode_achat_torp==1:
                                    if navire_joueur.budget>=lst_torp[0][4]:
                                        navire_joueur.change_torp(lst_torp[0])
                                        print("vos torpilles ont été modifié")
                                        navire_joueur.budget-=lst_torp[0][4]
                                if self.mode_achat_blindage==1:
                                    if navire_joueur.budget>=blindage[0][3]:
                                        navire_joueur.change_blindage(blindage[0])
                                        print("votre blindage a été changé")
                                        navire_joueur.budget-=blindage[0][3]
                                    else:
                                        print("vous n'avez pas assez d'argent")
                            self.affiche_texte=0
                            self.mode_achat=0
                            self.mode_achat_bp=0
                            self.mode_achat_bs=0
                            self.mode_achat_torp=0
                            self.mode_achat_blindage=0
                        if event.key==pg.K_x:
                            if self.mode_achat==1:
                                if self.mode_achat_bp==1:
                                    if navire_joueur.budget>=lst_bp[1][3]:
                                        navire_joueur.change_bp(lst_bp[1])
                                        print("votre batterie principale a été modifié")
                                        navire_joueur.budget-=lst_bp[1][3]
                                    else:
                                        print("vous n'avez pas assez d'argent")
                                if self.mode_achat_bs==1:
                                    if navire_joueur.budget>=lst_bs[1][3]:
                                        navire_joueur.change_bs(lst_bs[1])
                                        print("vos batteries secondaires a été modifié")
                                        navire_joueur.budget-=lst_bs[1][3]
                                    else:
                                        print("vous n'avez pas assez d'argent")
                                if self.mode_achat_torp==1:
                                    if navire_joueur.budget>=lst_torp[1][4]:
                                        navire_joueur.change_torp(lst_torp[1])
                                        print("vos torpilles ont été modifié")
                                        navire_joueur.budget-=lst_torp[1][4]
                                    else:
                                        print("vous n'avez pas assez d'argent")
                                if self.mode_achat_blindage==1:
                                    if navire_joueur.budget>=blindage[1][3]:
                                        navire_joueur.change_blindage(blindage[1])
                                        print("votre blindage a été changé")
                                        navire_joueur.budget-=blindage[1][3]
                                    else:
                                        print("vous n'avez pas assez d'argent")
                            self.affiche_texte=0
                            self.mode_achat=0
                            self.mode_achat_bp=0
                            self.mode_achat_bs=0
                            self.mode_achat_torp=0
                            self.mode_achat_blindage=0
                        if event.key==pg.K_c:
                            if self.mode_achat==1:
                                if self.mode_achat_bp==1:
                                    if navire_joueur.budget>=lst_bp[2][3]:
                                        navire_joueur.change_bp(lst_bp[2])
                                        print("vos batteries principales a été modifié")
                                        navire_joueur.budget-=lst_bp[2][3]
                                    else:
                                        print("vous n'avez pas assez d'argent")
                                if self.mode_achat_bs==1:
                                    if navire_joueur.budget>=lst_bs[2][3]:
                                        navire_joueur.change_bs(lst_bs[2])
                                        print("vos batteries secondaires a été modifié")
                                        navire_joueur.budget-=lst_bs[2][3]
                                    else:
                                        print("vous n'avez pas assez d'argent")
                                if self.mode_achat_torp==1:
                                    if navire_joueur.budget>=lst_torp[2][4]:
                                        navire_joueur.change_torp(lst_torp[2])
                                        print("vos torpilles ont été modifié")
                                        navire_joueur.budget-=torp[2][4]
                                    else:
                                        print("vous n'avez pas assez d'argent")
                                if self.mode_achat_blindage==1:
                                    if navire_joueur.budget>=blindage[2][3]:
                                        navire_joueur.change_blindage(blindage[2])
                                        print("votre blindage a été changé")
                                        navire_joueur.budget-=blindage[2][3]
                                    else:
                                        print("vous n'avez pas assez d'argent")
                                self.affiche_texte=0
                                self.mode_achat=0
                                self.mode_achat_bp=0
                                self.mode_achat_bs=0
                                self.mode_achat_torp=0
                                self.mode_achat_blindage=0
                        if event.key==pg.K_v:
                            if self.mode_achat==1:
                                if self.mode_achat_bp==1:
                                    if navire_joueur.budget>=lst_bp[3][3]:
                                        navire_joueur.change_bp(lst_bp[3])
                                        print("votre batterie principale a été modifié")
                                        navire_joueur.budget-=lst_bp[3][3]
                                    else:
                                        print("vous n'avez pas assez d'argent")
                                if self.mode_achat_bs==1:
                                    if navire_joueur.budget>=lst_bs[3][3]:
                                        navire_joueur.change_bs(lst_bs[3])
                                        print("votre batterie secondaire a été modifié")
                                        navire_joueur.budget-=lst_bs[3][3]
                                    else:
                                        print("vous n'avez pas assez d'argent")
                                if self.mode_achat_torp==1:
                                    navire_joueur.change_torp(lst_torp[3])
                                    print("vos torpille ont été rétiré")
                                if self.mode_achat_blindage==1:
                                    if navire_joueur.budget>=blindage[3][3]:
                                        navire_joueur.change_blindage(blindage[3])
                                        print("votre blindage a été changé")
                                        navire_joueur.budget-=blindage[3][3]
                                    else:
                                        print("vous n'avez pas assez d'argent")
                                self.affiche_texte=0
                                self.mode_achat=0
                                self.mode_achat_bp=0
                                self.mode_achat_bs=0
                                self.mode_achat_torp=0
                                self.mode_achat_blindage=0
                        if event.key==pg.K_b:
                            if self.mode_achat==1:
                                if self.mode_achat_bp==1:
                                    if navire_joueur.budget>=lst_bp[4][3]:
                                        navire_joueur.change_bp(lst_bp[4])
                                        print("votre batterie principale a été modifié")
                                self.affiche_texte=0
                                self.mode_achat=0
                                self.mode_achat_bp=0
                                self.mode_achat_bs=0
                                self.mode_achat_torp=0
                                self.mode_achat_blindage=0

            if self.player.x!=self.port.px or self.player.y!=self.port.py:
                    self.affiche_texte=0
                    self.mode_achat=0
                    self.mode_achat_bp=0
                    self.mode_achat_bs=0
                    self.mode_achat_torp=0
                    self.mode_achat_blindage=0


    def show_go_screen(self):
        if navire_joueur.navire_coule==True:
            print("vous avez coulé")
        else:
            print(" vous avez gagné")
        pg.quit()
        sys.exit()




g = Game()

while True:
    g.new()
    g.run()
    g.show_go_screen()