import pygame , sys , random ,os
pygame.init()
#cac ham 
def create_rocket():
    rocket_wight = random.choice( rocket_pos )
    rocket_rect = rocket_surface.get_rect( center = ( rocket_wight , 0 ) )
    return rocket_rect
def draw_rocket( rocket_list ):
    print( len( rocket_list ) )
    for rocket in rocket_list:
        Screen.blit( rocket_surface , rocket )
def move_rocket( rocket_list ):
    for rocket_rect in rocket_list:
        if rocket_rect.centery <= 800:
            rocket_rect.centery += 3
        else:
            rocket_list.remove( rocket_rect)
    return rocket_list 
def creat_bullet():
    bullet_rect = bullet_surface.get_rect( center = ( 0 , 740) )
    return bullet_rect
def move_bullet( centerx , bullet_list ):
    for bullet_rect in bullet_list :
        if bullet_rect.centery >= -20 :
            bullet_rect.centery -= 5 
            bullet_rect.centerx = centerx
        else :
            bullet_list.remove( bullet_rect )
def draw_bullet( bullet_list ):
    for bullet_rect in bullet_list:
        Screen.blit( bullet_surface , bullet_rect )
def check_die( bullet_list ):
    for bullet_rect in bullet_list :
        if plane_rect.colliderect( bullet_rect ):
            return False
    return True
#set up
Screen = pygame.display.set_mode ( (938 ,780) )
clock = pygame.time.Clock()
# tao nen 
bg = pygame.image.load(r"Images\Textures\stars_galaxy.jpg")
# tao plane
plane_surface = pygame.image.load( r"Images\Objects\ship2.png")
plane_rect = plane_surface.get_rect( midbottom = ( 450 , 750 ) )
plane_movementx = 0 
plane_movementy = 0 
#tao rocket
rocket_surface = pygame.image.load( r"Images\Objects\ship_blue.png")
rocket_event = pygame.USEREVENT + 1
pygame.time.set_timer( rocket_event , 1000 )
rocket_list = []
rocket_pos = [ 10 , 100 , 200 , 300 , 400 , 500 , 600 , 700 , 800 , 900 ]
# tao bullet cho plane
bullet_surface = pygame.image.load( r"Images\Objects\bullet4.png")
bullet_event = pygame.USEREVENT + 2
pygame.time.set_timer( bullet_event , 200 )
bullet_list = [ ]
# check collision giua rocket va plane
Active = True 

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and Active :
            if event.key == pygame.K_LEFT:
                plane_movementx = -7 
            elif event.key == pygame.K_RIGHT:
                plane_movementx = 7 
            elif event.key == pygame.K_DOWN:
                plane_movementy = 7
            elif event.key == pygame.K_UP:
                plane_movementy = -7
        if event.type == pygame.KEYDOWN and ( not Active ) :
            Active = True 
            rocket_list.clear()
            bullet_list.clear()
            plane_rect = plane_surface.get_rect( midbottom = ( 450 , 750 ) )
        if event.type == pygame.KEYUP:
            plane_movementx = 0 
            plane_movementy = 0 
        if event.type == rocket_event:
            rocket_list.append( create_rocket() )
        if event.type == bullet_event:
            bullet_list.append( creat_bullet() )
    Screen.blit( bg , ( 0 , 0 ) )
    if Active:
        #plane
        move_bullet( plane_rect.centerx, bullet_list )
        draw_bullet( bullet_list )
        Screen.blit( plane_surface , plane_rect )
        plane_rect.centerx += plane_movementx
        plane_rect.centery += plane_movementy
        #rocket
        rocket_list = move_rocket( rocket_list )
        draw_rocket(rocket_list)
        Active = check_die( rocket_list )
    
    pygame.display.update()
    clock.tick( 60 )