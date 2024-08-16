import pygame , sys , random ,os
import cv2
import mediapipe as mp
import numpy as np
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
pygame.display.set_caption( "Máy bay chiến đấu")
icon = pygame.image.load( r".\Images\Objects\plane.png" )
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
            rocket_rect.centery += 12
        else:
            rocket_list.remove( rocket_rect)
def creat_bullet():
    bullet_rect = bullet_surface.get_rect( center = ( plane_rect.centerx , plane_rect.centery - 48 ) )
    return bullet_rect
def move_bullet( bullet_list ):
    for bullet_rect in bullet_list :
        if bullet_rect.centery >= -20 :
            bullet_rect.centery -= 10 
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
            star_rect.centery += 4 
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

def is_fist(hand_landmarks):
    """ Kiểm tra xem bàn tay có nắm lại không. """
    for i in [8, 12, 16, 20]:
        if hand_landmarks.landmark[i].y < hand_landmarks.landmark[i - 2].y:
            return False
    return True

def is_thumb_touching(hand_landmarks, finger_tip):
    """ Kiểm tra xem ngón cái có chạm ngón chỉ định không. """
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    distance = ((thumb_tip.x - hand_landmarks.landmark[finger_tip].x) ** 2 + 
                (thumb_tip.y - hand_landmarks.landmark[finger_tip].y) ** 2) ** 0.5
    return distance < 0.05

def is_palm_facing(hand_landmarks, direction="left"):
    """ Kiểm tra xem lòng bàn tay hướng về phía nào. """
    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
    thumb_cmc = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC]
    if direction == "left":
        return wrist.x < thumb_cmc.x
    elif direction == "right":
        return wrist.x > thumb_cmc.x
    return False

# add sound 
pygame.mixer.music.load( r".\.Sounds\Epic Hip Hop.mp3")
pygame.mixer.music.play(-1 , 0 , 0 )
shoot_sound = pygame.mixer.Sound( r".\.Sounds\gunshot.wav")
headshoot_sound = pygame.mixer.Sound( r".\.Sounds\explosion.wav" )
die_sound = pygame.mixer.Sound(r".\.Sounds\bomb.wav")
get_star_sound = pygame.mixer.Sound( r".\.Sounds\sound-effect-twinklesparkle-115095.mp3")
#set up
height = 790
wight = 938
Screen = pygame.display.set_mode ( (wight ,height) )
clock = pygame.time.Clock()
# tao nen 
bg = pygame.image.load(r".\Images\Textures\stars_galaxy.jpg")
bg_pos = 0 
# tao plane
plane_surface = pygame.image.load( r".\Images\Objects\plane.png")
plane_rect = plane_surface.get_rect( midbottom = ( wight // 2 , height - 20  ) )
plane_movementx = 0 
plane_movementy = 0 
#tao rocket
rocket_surface = pygame.image.load( r".\Images\Objects\ufo.png")
rocket_speed_event = pygame.USEREVENT + 1
pygame.time.set_timer( rocket_speed_event , 5000 ) # cu moi 5s thi tang so luong rocket
rocket_event = pygame.USEREVENT + 2
rocket_speed = 1000
pygame.time.set_timer( rocket_event , rocket_speed )
rocket_list = []
rocket_pos = range( 10 , 930 )
# tao bullet cho plane
bullet_surface = pygame.image.load( r".\Images\Objects\bullet.png")
bullet_speed = 400
bullet_speed_max = 90
bullet_event = pygame.USEREVENT + 3
pygame.time.set_timer( bullet_event , bullet_speed )
bullet_list = [ ]
# tao star
star_surface = pygame.image.load ( r".\Images\Objects\star (1).png")
star_list = []
star_event = pygame.USEREVENT + 4 
pygame.time.set_timer( star_event , 20000 )
# check collision giua rocket va plane
Active = True 
# tao score
game_font = pygame.font.Font(r".\04B_19.TTF", 40)
score = 0 
max_score = 0 
# game over
geme_over_surface = pygame.image.load ( r".\Images\Textures\game_over_PNG41 (1).png")
game_over_rect = geme_over_surface.get_rect( center = ( wight/2 , height/2 - 50 ) )
# Khởi tạo Mediapipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Thiết lập các tùy chọn cho Mediapipe Hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Bắt đầu sử dụng camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)  # Lật khung hình để thuận tiện hơn
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Xử lý hình ảnh
    result = hands.process(rgb_frame)
    move_direction = "Dung yen"
    plane_movementx = 0
    plane_movementy = 0

    # Nếu phát hiện bàn tay
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmarks = hand_landmarks.landmark

            # Tọa độ của đầu ngón cái và ngón trỏ
            thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_tip = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]  # Đầu ngón giữa

            # Chuyển đổi tọa độ từ tỷ lệ (0-1) sang pixel
            h, w, _ = frame.shape
            thumb_tip_x, thumb_tip_y = int(thumb_tip.x * w), int(thumb_tip.y * h)
            index_tip_x, index_tip_y = int(index_tip.x * w), int(index_tip.y * h)
            middle_tip_x, middle_tip_y = int(middle_tip.x * w), int(middle_tip.y * h)

            # Vẽ điểm ở vị trí của các ngón tay
            cv2.circle(frame, (index_tip_x, index_tip_y), 10, (0, 255, 0), -1)  # Ngón trỏ (màu xanh lá)
            cv2.circle(frame, (thumb_tip_x, thumb_tip_y), 10, (0, 0, 255), -1)  # Ngón cái (màu đỏ)
            cv2.circle(frame, (middle_tip_x, middle_tip_y), 10, (0, 255, 255), -1)  # Ngón giữa (màu vàng)

            if is_fist(hand_landmarks):
                plane_movementx = 0
                plane_movementy = 0
                move_direction = "Dung yen"
            elif is_thumb_touching(hand_landmarks, mp_hands.HandLandmark.INDEX_FINGER_TIP):
                plane_movementy = 14
                move_direction = "Di xuong"
            elif is_thumb_touching(hand_landmarks, mp_hands.HandLandmark.MIDDLE_FINGER_TIP):
                plane_movementy = -14
                move_direction = "Di len"
            elif is_palm_facing(hand_landmarks, "right"):
                plane_movementx = 14
                move_direction = "Sang phai"
            elif is_palm_facing(hand_landmarks, "left"):
                plane_movementx = -14
                move_direction = "Sang trai"

            # Hiển thị cử chỉ trên màn hình
            cv2.putText(frame, move_direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Hiển thị khung hình
    cv2.imshow('Hand Tracking', frame)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and Active :
            if event.key == pygame.K_LEFT or event.key == pygame.K_a :
                plane_movementx = -14
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                plane_movementx = 14 
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                plane_movementy = 14
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                plane_movementy = -14

        if event.type == pygame.KEYDOWN and ( not Active ) :
            if event.key == pygame.K_SPACE:
                Active = True
                #xoa het rocket va bullet 
                rocket_list.clear()
                bullet_list.clear()
                bullet_speed = 400
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
    bg_pos += 3 
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
cap.release()
cv2.destroyAllWindows()