import pygame , sys , random ,os
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
pygame.display.set_caption( "Máy bay chiến đấu")
icon = pygame.image.load( r"C:\workspace\Python\plane-game\Images\Objects\ship2.png" )
pygame.display.set_icon( icon )
#cac ham
def draw_bg():
    Screen.blit( bg , ( 0 , bg_pos ))
    Screen.blit( bg , ( 0 , bg_pos - 1668 ) )
def create_rocket():
    rocket_wight = random.choice( rocket_pos )
    rocket_rect = rocket_surface.get_rect( center = ( rocket_wight , 0 ) )
    return rocket_rect
def draw_rocket( rocket_list ):
    for rocket in rocket_list:
        Screen.blit( rocket_surface , rocket )
def move_rocket( rocket_list ):
    for rocket_rect in rocket_list:
        if rocket_rect.centery <= height + 48 :
            rocket_rect.centery += 3
        else:
            rocket_list.remove( rocket_rect)
def creat_bullet():
    bullet_rect = bullet_surface.get_rect( center = ( plane_rect.centerx , plane_rect.centery - 48 ) )
    return bullet_rect
def move_bullet( bullet_list ):
    for bullet_rect in bullet_list :
        if bullet_rect.centery >= -20 :
            bullet_rect.centery -= 5 
        else :
            bullet_list.remove( bullet_rect )
def draw_bullet( bullet_list ):
    for bullet_rect in bullet_list:
        Screen.blit( bullet_surface , bullet_rect )
def check_die( bullet_list ):
    for bullet_rect in bullet_list :
        if plane_rect.colliderect( bullet_rect ):
            die_sound.play()
            return False
    return True
def headshoot( bullet_list , rocket_list ):
    global score
    for bullet in bullet_list :
        for rocket in rocket_list :
            if bullet.colliderect( rocket ):
                score += 1
                headshoot_sound.play()
                bullet_list.remove( bullet )
                rocket_list.remove( rocket )
def creat_star():
    star_wight = random.choice( range( 10 , 930 ) )
    star_rect = star_surface.get_rect( center = ( star_wight , 0 ) )
    return star_rect
def move_star(star_list):
    for star_rect in star_list :
        if star_rect.centery < height - 20 :
            star_rect.centery += 2 
        else:
            star_rect.centery = height - 20
def draw_star( star_list ):
    for star_rect in star_list :
        Screen.blit( star_surface , star_rect )
def get_star(bullet_speed , star_list):
    for star_rect in star_list:
        if plane_rect.colliderect( star_rect):
            get_star_sound.play()
            star_list.remove( star_rect )
            if bullet_speed >= 90 :
                bullet_speed -= 30
    return bullet_speed
def drow_score1( ):
    score_surface = game_font.render( str( score ) , True , ( 255 , 255 , 255 ) )
    Screen.blit( score_surface , ( wight/2 , 20 ) )
def drow_score2( ):
    score_surface = game_font.render( "current score: " + str( score ) , True , (255,0,0) )
    score_rect = score_surface.get_rect( center = ( wight/2 , height/ 2 + 100 ) )
    max_score_surface = game_font.render( "High score: " + str( max_score ) , True , (255,0,0) )
    max_score_rect = max_score_surface.get_rect( center = ( wight/2 , height/ 2 + 150 ) )
    Screen.blit( score_surface , score_rect )
    Screen.blit( max_score_surface , max_score_rect )
# add sound 
pygame.mixer.music.load( r"C:\workspace\Python\plane-game\.Sounds\Epic Hip Hop.mp3")
pygame.mixer.music.play(-1 , 0 , 0 )
shoot_sound = pygame.mixer.Sound( r"C:\workspace\Python\plane-game\.Sounds\gunshot.wav")
headshoot_sound = pygame.mixer.Sound( r"C:\workspace\Python\plane-game\.Sounds\explosion.wav" )
die_sound = pygame.mixer.Sound(r"C:\workspace\Python\plane-game\.Sounds\bomb.wav")
get_star_sound = pygame.mixer.Sound( r"C:\workspace\Python\plane-game\.Sounds\sound-effect-twinklesparkle-115095.mp3")
#set up
height = 790
wight = 938
Screen = pygame.display.set_mode ( (wight ,height) )
clock = pygame.time.Clock()
# tao nen 
bg = pygame.image.load(r"C:\workspace\Python\plane-game\Images\Textures\stars_galaxy.jpg")
bg_pos = 0 
# tao plane
plane_surface = pygame.image.load( r"C:\workspace\Python\plane-game\Images\Objects\ship2.png")
plane_rect = plane_surface.get_rect( midbottom = ( wight // 2 , height - 20  ) )
plane_movementx = 0 
plane_movementy = 0 
#tao rocket
rocket_surface = pygame.image.load( r"C:\workspace\Python\plane-game\Images\Objects\ship_gray.png")
rocket_speed_event = pygame.USEREVENT + 1
pygame.time.set_timer( rocket_speed_event , 5000 ) # cu moi 5s thi tang so luong rocket
rocket_event = pygame.USEREVENT + 2
rocket_speed = 1000
pygame.time.set_timer( rocket_event , rocket_speed )
rocket_list = []
rocket_pos = range( 10 , 930 )
# tao bullet cho plane
bullet_surface = pygame.image.load( r"C:\workspace\Python\plane-game\Images\Objects\bullet4.png")
bullet_speed = 300
bullet_speed_max = 60
bullet_event = pygame.USEREVENT + 3
pygame.time.set_timer( bullet_event , bullet_speed )
bullet_list = [ ]
# tao star
star_surface = pygame.image.load ( r"C:\workspace\Python\plane-game\Images\Objects\star (1).png")
star_list = []
star_event = pygame.USEREVENT + 4 
pygame.time.set_timer( star_event , 20000 )
# check collision giua rocket va plane
Active = True 
# tao score
game_font = pygame.font.Font(r"C:\workspace\Python\plane-game\04B_19.TTF", 40)
score = 0 
max_score = 0 
# game over
geme_over_surface = pygame.image.load ( r"C:\workspace\Python\plane-game\Images\Textures\game_over_PNG41 (1).png")
game_over_rect = geme_over_surface.get_rect( center = ( wight/2 , height/2 - 50 ) )
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and Active :
            if event.key == pygame.K_LEFT or event.key == pygame.K_a :
                plane_movementx = -7
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                plane_movementx = 7 
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                plane_movementy = 7
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                plane_movementy = -7
        if event.type == pygame.KEYDOWN and ( not Active ) :
            if event.key == pygame.K_SPACE:
                Active = True
                #xoa het rocket va bullet 
                rocket_list.clear()
                bullet_list.clear()
                bullet_speed = 300
                pygame.time.set_timer( bullet_event , bullet_speed )
                # reset lai so luong ten lua va toc do ten lua
                rocket_speed = 1000
                pygame.time.set_timer( rocket_event , rocket_speed )
                # xoa het star
                star_list.clear()
                # reset lai vi tri cua may bay
                plane_rect = plane_surface.get_rect( midbottom = ( 450 , 750 ) )
                #reset score
                score = 0 ; 
        if event.type == pygame.KEYUP:
            plane_movementx = 0 
            plane_movementy = 0 
        if event.type == rocket_event:
            rocket_list.append( create_rocket() )
        if event.type == bullet_event and Active :
            shoot_sound.play()
            bullet_list.append( creat_bullet() )
        # sau mot khoang thoi gian se tang them so luong rocket
        if event.type == rocket_speed_event and rocket_speed >= 250 :
            rocket_speed -= 50
            pygame.time.set_timer( rocket_event , rocket_speed )
        # khi nao toc do chua = toc do max thi tiep tuc cho ngoi sao
        if event.type == star_event and len( star_list ) < 1 and bullet_speed > bullet_speed_max : 
            star_list.append( creat_star() )
    draw_bg()
    bg_pos += 1 
    if bg_pos > 1668 :
        bg_pos = 0
    if Active:
        #plane
        move_bullet( bullet_list )
        draw_bullet( bullet_list )
        Screen.blit( plane_surface , plane_rect )
        plane_rect.centerx += plane_movementx
        plane_rect.centery += plane_movementy
        if plane_rect.centerx < 0 + 48:
            plane_rect.centerx = 0 + 48
        if plane_rect.centerx > wight - 48:
            plane_rect.centerx = wight - 48
        if plane_rect.centery < 0 + 48:
            plane_rect.centery = 0 + 48
        if plane_rect.centery > height - 48:
            plane_rect.centery = height - 48 
        #rocket
        move_rocket( rocket_list )
        draw_rocket(rocket_list )
        headshoot(bullet_list , rocket_list)
        # star
        move_star(star_list)
        draw_star(star_list)
        bullet_speed_sample = get_star( bullet_speed ,star_list)
        if bullet_speed != bullet_speed_sample:
            bullet_speed = bullet_speed_sample
            pygame.time.set_timer( bullet_event , bullet_speed )
        Active = check_die( rocket_list )
        # score
        max_score = max( max_score , score )
        drow_score1()
    else :
        Screen.blit( geme_over_surface , game_over_rect )
        drow_score2()
    pygame.display.update()
    clock.tick( 120 )