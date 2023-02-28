import random

def endroit_toucher():
    endroit_toucher=random.randint(0,100)
    if endroit_toucher<=10:        #correspond a un obus sous la ligne de flotaison
        zone=3
    elif 10<endroit_toucher<=80:   #correspond a un obus dans la ceinture
        zone=0
    elif 80<endroit_toucher<=90:   #correspond a un obus dans une tourrelle
        zone=1
    else:                          #correspond a un obus dans la super structure
        zone=2
    return zone



class Navire:
    def __init__(self,prefixe,nom,ps,budget,blindage,vitesse):
        self.prefixe=prefixe
        self.nom=nom
        self.ps=ps
        self.ps_max=ps
        self.budget=budget
        self.innondation=0
        self.navire_coule=False
        self.vitesse=vitesse
        self.blindage=blindage

    def reparation(self,nb_ps_a_reparer):
        ps_manquants=self.ps_max-self.ps
        if self.navire_coule==True:
            print("réparation impossible")
        else:
            if nb_ps_a_reparer>ps_manquants:
                prix_reparation=ps_manquants*5
                if prix_reparation<self.budget:
                    self.ps=self.ps_max
                    self.budget-=prix_reparation
                    print("votre navire a été entièrement réparer")
                    print("les réparations vous on couté",str(prix_reparation),"il vous reste donc",str(self.budget,"€"))
            else:
                prix_reparation=nb_ps_a_reparer*5
                if prix_reparation<self.budget:
                    self.ps+=nb_ps_a_reparer
                    self.budget-=prix_reparation
                    print(str(nb_ps_a_reparer),"ps on été réstaurer")
                    print("les réparations vous on couté",str(prix_reparation),"il vous reste donc",str(self.budget,"€"))

    def a_coule(self):
        if self.innondation>=100 or self.ps<=0:
            self.navire_coule=True
            print("le "+str(self.prefixe)+" "+str(self.nom)+" a coulé")
            return True
        else:
            return False

class Cuirasse(Navire):
    def __init__(self,prefixe,nom,ps,budget,blindage,vitesse,batterie_principale,batterie_secondaire,torpille):
        super().__init__(prefixe,nom,ps,budget,blindage,vitesse)
        self.nb_bp=batterie_principale[1]
        self.calibre_bp=batterie_principale[0]
        self.portee_bp=batterie_principale[2]
        self.nb_bs=batterie_secondaire[1]
        self.calibre_bs=batterie_secondaire[0]
        self.portee_bs=batterie_secondaire[2]
        if torpille[0]==False:
            self.torp=False
        elif torpille[0]==True:
            self.torp=True
            self.portee_torp=torpille[2]
            self.calibre_torp=torpille[1]
            self.nb_torp=torpille[3]
    def combat(self,ennemi,distance):
        if distance<self.portee_bp*100:                                         #calcul les dégats qu'inflige les batteries principales
            nb_touche=0
            nb_ceinture=0
            nb_super_structure=0
            nb_ligne_flottaison=0
            nb_tourelle=0
            for i in range(0,self.nb_bp):
                a_toucher=random.randint(1,100)
                if a_toucher<=0+distance/100:
                    nb_touche+=0
                else:
                    nb_touche+=1
                    zone_toucher=endroit_toucher()
                    if zone_toucher!=3:
                        if self.blindage[zone_toucher]>self.calibre_bp:              #regarde si le calibre de l'obus est supérieur au blindage si il l'est un bonus de déga sera appliqué si il est inférieur un malus sera appliqué
                            multiplicateur=1.2
                        else:
                            multiplicateur=0.7
                        if zone_toucher==0:
                            multiplicateur*=1
                            #print("les obus ont touchés la ceinture")
                            nb_ceinture+=1
                        elif zone_toucher==1:
                            multiplicateur-=0.2
                            #print("les obus ont touchés une tourelle")
                            nb_tourelle+=1
                        elif zone_toucher==2:
                            multiplicateur+=0.2
                            #print("les obus ont touchés la super structure")
                            nb_super_structure+=1
                    elif zone_toucher==3:
                        multiplicateur=1
                        ennemi.innondation+=self.calibre_bp/100                                     #la zone 3 correspond à sous la ligne de flottaison cette zone est peu blindé donc aucun malus n'est affligé si un obus la touche ais il inflige une addition
                        nb_ligne_flottaison+=1
                    ennemi.ps=ennemi.ps-(self.calibre_bp*multiplicateur*0.5)
            print("sur les",self.nb_bp,"tiré par les batteries principales du",self.nom,",",nb_touche,"obus ont touchés")
            print(nb_ceinture,"ont touchés la ceinture",nb_ligne_flottaison,"ont touchés sous la ligne de flottaison",nb_tourelle,"ont touché les tourelles",nb_super_structure,"ont touchés la super structure")
        else:
            print("le",ennemi.prefixe,ennemi.nom,"est hors de portée des batteries principales du",self.prefixe,self.nom)
        if distance<self.portee_bs*100:                                                   #calcul les dégats qu'inflige les batteries secondaires
                nb_touche=0
                nb_ceinture=0
                nb_super_structure=0
                nb_ligne_flottaison=0
                nb_tourelle=0
                for i in range(0,self.nb_bs):
                    a_toucher=random.randint(1,100)
                    if a_toucher<=0+distance/100:
                        nb_touche+=0
                    else:
                        nb_touche+=1
                        zone_toucher=endroit_toucher()
                        if zone_toucher!=3:
                            if self.blindage[zone_toucher]>self.calibre_bs:                         #regarde si le calibre de l'obus est supérieur au blindage si il l'est un bonus de déga sera appliqué si il est inférieur un malus sera appliqué
                                multiplicateur=1
                            else:
                                multiplicateur=0.5
                            if zone_toucher==0:
                                multiplicateur*=1
                                #print("les obus ont touchés la ceinture")
                                nb_ceinture+=1
                            elif zone_toucher==1:
                                multiplicateur-=0.2
                                #print("les obus ont touchés une tourelle")
                                nb_tourelle+=1
                            elif zone_toucher==2:
                                multiplicateur+=0.2
                                #print("les obus ont touchés la super structure")
                                nb_super_structure+=1
                        elif zone_toucher==3:
                            multiplicateur=1
                            ennemi.innondation+=self.calibre_bs/100               #la zone 3 correspond à sous la ligne de flottaison cette zone est peu blindé donc aucun malus n'est affligé si un obus la touche ais il inflige une addition
                            #print("l'ennemi a été touché sous la ligne de flottaison")
                            nb_ligne_flottaison+=1
                        ennemi.ps=ennemi.ps-(self.calibre_bs*multiplicateur*0.4)
                print("sur les",self.nb_bs,"obus tiré par les batteries secondaires du",self.nom,",",nb_touche,"obus ont touchés")
                print(nb_ceinture,"ont touchés la ceinture",nb_ligne_flottaison,"ont touchés sous la ligne de flottaison",nb_tourelle,"ont touché les tourelles",nb_super_structure,"ont touchés la super structure")
        else:
            print("le",ennemi.prefixe,ennemi.nom,"est hors de portée des batteries secondaire du",self.prefixe,self.nom)

        if self.torp==True:
            if distance<self.portee_torp*1000:                                                   #calcul les dégats qu'inflige les batteries secondaires
                nb_touche=0
                for i in range(0,self.nb_torp):
                    a_toucher=random.randint(1,100)
                    if a_toucher<=0+distance/25:
                        nb_touche+=0
                    else:
                        nb_touche+=1
                        ennemi.ps=ennemi.ps-self.calibre_torp*7
                        ennemi.innondation+=(self.calibre_torp/100)
                print("sur",self.nb_torp,"torpille tiré par le",self.nom,nb_touche,"ont touché(s)")
            else:
                print("le",ennemi.prefixe,ennemi.nom,"est hors de portée des torpilles du",self.prefixe,self.nom)
    def change_bp(self,nouvelle_bp):
        self.nb_bp=nouvelle_bp[1]
        self.calibre_bp=nouvelle_bp[0]
        self.portee_bp=nouvelle_bp[2]
    def change_bs(self,nouvelle_bs):
        self.nb_bs=nouvelle_bs[1]
        self.calibre_bs=nouvelle_bs[0]
        self.portee_bs=nouvelle_bs[2]
    def change_torp(self,novelle_torp):
        if novelle_torp[0]==True:
            self.portee_torp=novelle_torp[2]
            self.calibre_torp=novelle_torp[1]
            self.nb_torp=novelle_torp[3]
        else:
            self.torp=False
    def change_blindage(self,nouveau_blindage):
        self.blindage=nouveau_blindage
        self.ps_max=nouveau_blindage[4]
        self.ps=self.ps_max

class Destroyer(Navire):
    def __init__(self,prefixe,nom,ps,budget,blindage,vitesse,batterie_principale,torpille):
        super().__init__(prefixe,nom,ps,budget,blindage,vitesse)
        self.nb_bp=batterie_principale[1]
        self.calibre_bp=batterie_principale[0]
        self.portee_bp=batterie_principale[2]
        self.portee_torp=torpille[1]
        self.calibre_torp=torpille[0]
        self.nb_torp=torpille[2]

    def combat(self,ennemi,distance):
        if distance<self.portee_bp*100:                                         #calcul les dégats qu'inflige les batteries principales
            nb_touche=0
            nb_ceinture=0
            nb_super_structure=0
            nb_ligne_flottaison=0
            nb_tourelle=0
            for i in range(0,self.nb_bp):
                a_toucher=random.randint(1,100)
                if a_toucher<=0+distance/25:
                    nb_touche+=0
                else:
                    nb_touche+=1
                    zone_toucher=endroit_toucher()
                    if zone_toucher!=3:
                        if self.blindage[zone_toucher]>self.calibre_bp:              #regarde si le calibre de l'obus est supérieur au blindage si il l'est un bonus de déga sera appliqué si il est inférieur un malus sera appliqué
                            multiplicateur=1.2
                        else:
                            multiplicateur=0.7
                        if zone_toucher==0:
                            multiplicateur*=1
                            #print("les obus ont touchés la ceinture")
                            nb_ceinture+=1
                        elif zone_toucher==1:
                            multiplicateur-=0.2
                            #print("les obus ont touchés une tourelle")
                            nb_tourelle+=1
                        elif zone_toucher==2:
                            multiplicateur+=0.2
                            #print("les obus ont touchés la super structure")
                            nb_super_structure+=1
                    elif zone_toucher==3:
                        multiplicateur=1
                        ennemi.innondation+=self.calibre_bp/100                                     #la zone 3 correspond à sous la ligne de flottaison cette zone est peu blindé donc aucun malus n'est affligé si un obus la touche ais il inflige une addition
                        nb_ligne_flottaison+=1
                    ennemi.ps=ennemi.ps-(self.calibre_bp*multiplicateur*0.5)
            print("sur les",self.nb_bp,"tiré par les batteries principales du",self.nom,",",nb_touche,"obus ont touchés")
            print(nb_ceinture,"ont touchés la ceinture",nb_ligne_flottaison,"ont touchés sous la ligne de flottaison",nb_tourelle,"ont touché les tourelles",nb_super_structure,"ont touchés la super structure")
        if distance<self.portee_torp*1000:                                                   #calcul les dégats qu'inflige les batteries secondaires
                nb_touche=0
                for i in range(0,self.nb_torp):
                    a_toucher=random.randint(1,100)
                    if a_toucher<=0+distance/25:
                        nb_touche+=0
                    else:
                        nb_touche+=1
                        ennemi.ps=ennemi.ps-self.calibre_torp*7
                        ennemi.innondation+=(self.calibre_torp/100)
                print("sur",self.nb_torp,"torpille tiré par le",self.nom,nb_touche,"ont touché(s)")



class Croiseur(Navire):
    def __init__(self,prefixe,nom,ps,budget,blindage,vitesse,batterie_principale,batterie_secondaire,torpille):
        super().__init__(prefixe,nom,ps,budget,blindage,vitesse)
        self.nb_bp=batterie_principale[1]
        self.calibre_bp=batterie_principale[0]
        self.portee_bp=batterie_principale[2]
        self.nb_bs=batterie_secondaire[1]
        self.calibre_bs=batterie_secondaire[0]
        self.portee_bs=batterie_secondaire[2]
        if torpille[0]==False:
            self.torp=False
        elif torpille[0]==True:
            self.torp=True
            self.portee_torp=torpille[1]
            self.calibre_torp=torpille[2]
            self.nb_torp=torpille[3]
    def combat(self,ennemi,distance):
        if distance<self.portee_bp*100:                                         #calcul les dégats qu'inflige les batteries principales
            nb_touche=0
            nb_ceinture=0
            nb_super_structure=0
            nb_ligne_flottaison=0
            nb_tourelle=0
            for i in range(0,self.nb_bp):
                a_toucher=random.randint(1,100)
                if a_toucher<=0+distance/100:
                    nb_touche+=0
                else:
                    nb_touche+=1
                    zone_toucher=endroit_toucher()
                    if zone_toucher!=3:
                        if self.blindage[zone_toucher]>self.calibre_bp:              #regarde si le calibre de l'obus est supérieur au blindage si il l'est un bonus de déga sera appliqué si il est inférieur un malus sera appliqué
                            multiplicateur=1.2
                        else:
                            multiplicateur=0.7
                        if zone_toucher==0:
                            multiplicateur*=1
                            #print("les obus ont touchés la ceinture")
                            nb_ceinture+=1
                        elif zone_toucher==1:
                            multiplicateur-=0.2
                            #print("les obus ont touchés une tourelle")
                            nb_tourelle+=1
                        elif zone_toucher==2:
                            multiplicateur+=0.2
                            #print("les obus ont touchés la super structure")
                            nb_super_structure+=1
                    elif zone_toucher==3:
                        multiplicateur=1
                        ennemi.innondation+=self.calibre_bp/100                                     #la zone 3 correspond à sous la ligne de flottaison cette zone est peu blindé donc aucun malus n'est affligé si un obus la touche ais il inflige une addition
                        nb_ligne_flottaison+=1
                    ennemi.ps=ennemi.ps-(self.calibre_bp*multiplicateur*0.5)
            print("sur les",self.nb_bp,"tiré par les batteries principales du",self.nom,",",nb_touche,"obus ont touchés")
            print(nb_ceinture,"ont touchés la ceinture",nb_ligne_flottaison,"ont touchés sous la ligne de flottaison",nb_tourelle,"ont touché les tourelles",nb_super_structure,"ont touchés la super structure")
        else:
            print("le",ennemi.prefixe,ennemi.nom,"est hors de portée des batteries pricipales du",self.prefixe,self.nom)
        if distance<self.portee_bs*100:                                                   #calcul les dégats qu'inflige les batteries secondaires
                nb_touche=0
                nb_ceinture=0
                nb_super_structure=0
                nb_ligne_flottaison=0
                nb_tourelle=0
                for i in range(0,self.nb_bs):
                    a_toucher=random.randint(1,100)
                    if a_toucher<=0+distance/100:
                        nb_touche+=0
                    else:
                        nb_touche+=1
                        zone_toucher=endroit_toucher()
                        if zone_toucher!=3:
                            if self.blindage[zone_toucher]>self.calibre_bs:                         #regarde si le calibre de l'obus est supérieur au blindage si il l'est un bonus de déga sera appliqué si il est inférieur un malus sera appliqué
                                multiplicateur=1
                            else:
                                multiplicateur=0.5
                            if zone_toucher==0:
                                multiplicateur*=1
                                #print("les obus ont touchés la ceinture")
                                nb_ceinture+=1
                            elif zone_toucher==1:
                                multiplicateur-=0.2
                                #print("les obus ont touchés une tourelle")
                                nb_tourelle+=1
                            elif zone_toucher==2:
                                multiplicateur+=0.2
                                #print("les obus ont touchés la super structure")
                                nb_super_structure+=1
                        elif zone_toucher==3:
                            multiplicateur=1
                            ennemi.innondation+=self.calibre_bs/100               #la zone 3 correspond à sous la ligne de flottaison cette zone est peu blindé donc aucun malus n'est affligé si un obus la touche ais il inflige une addition
                            #print("l'ennemi a été touché sous la ligne de flottaison")
                            nb_ligne_flottaison+=1
                        ennemi.ps=ennemi.ps-(self.calibre_bs*multiplicateur*0.4)
                print("sur les",self.nb_bs,"obus tiré par les batteries secondaires du",self.nom,",",nb_touche,"obus ont touchés")
                print(nb_ceinture,"ont touchés la ceinture",nb_ligne_flottaison,"ont touchés sous la ligne de flottaison",nb_tourelle,"ont touché les tourelles",nb_super_structure,"ont touchés la super structure")
        else:
            print("le",ennemi.prefixe,ennemi.nom,"est hors de portée des batteries pricipales du",self.prefixe,self.nom)
        if self.torp==True:
            if distance<self.portee_torp*1000:                                                   #calcul les dégats qu'inflige les batteries secondaires
                nb_touche=0
                for i in range(0,self.nb_torp):
                    a_toucher=random.randint(1,100)
                    if a_toucher<=distance/25:
                        nb_touche+=0
                    else:
                        nb_touche+=1
                        ennemi.ps=ennemi.ps-self.calibre_torp*7
                        ennemi.innondation+=(self.calibre_torp/100)
                print("sur",self.nb_torp,"torpille tiré par le",self.nom,nb_touche,"ont touché(s)")
'''
distance=10000
joueur=Cuirasse("kms","Bismarck",10000,20000,[320,350,120],30,[380,8,30],[150,12,20],[False])
ennemi=Croiseur("hms","Hood",6000,17500,[305,381,25],32,[381,8,27],[140,12,17],[False])
etat_joueur=joueur.a_coule()
etat_ennemi=ennemi.a_coule()
while etat_joueur==False and etat_ennemi==False:
    if distance>2000:
        distance=distance-(joueur.vitesse*10+ennemi.vitesse*10)
    print("la distance qui sépare le",str(joueur.prefixe),str(joueur.nom),"du",str(ennemi.prefixe),str(ennemi.nom),"est",distance)
    joueur.combat(ennemi,distance)
    ennemi.combat(joueur,distance)
    print("il vous reste",joueur.ps,"ps")
    print("il reste",ennemi.ps,"ps au",ennemi.prefixe,ennemi.nom)
    etat_joueur=joueur.a_coule()
    etat_ennemi=ennemi.a_coule()'''