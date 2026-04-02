import pygame
import math
from collections import namedtuple

pygame.init()
screen = pygame.display.set_mode((1280,720), vsync = 1)
pygame.display.set_caption("2D POV")
running = False
Menu = True
clock = pygame.time.Clock()

# Menu Loop
while Menu:
    MenuScreen = pygame.Surface((1280, 720))
    MenuScreen.fill((255, 255, 255))
    screen.blit(MenuScreen, (0, 0))

    key = pygame.key.get_pressed()

    # Menu Text
    FontMenu = pygame.font.Font(None, 100)
    MenuText = FontMenu.render("1st Person 2D Platformer", True, (0, 0, 0))
    screen.blit(MenuText, (MenuScreen.get_width() / 2 - MenuText.get_width() / 2, MenuScreen.get_height() / 3 - MenuText.get_height() / 2))
    # Start Insttuction Text
    FontInstruction = pygame.font.Font(None, 50)
    InstructionText = FontInstruction.render("Press Enter to Start", True, (0, 0, 0))
    screen.blit(InstructionText, (MenuScreen.get_width() / 2 - InstructionText.get_width() / 2, MenuScreen.get_height() * 0.5 - MenuText.get_height() / 2))

    # Controls InstructionText
    FontControlls = pygame.font.Font(None, 30)
    InstructionLine1 = FontControlls.render("W to walk forward", True, (0, 0, 0))
    InstructionLine2 = FontControlls.render("S to walk backward", True, (0, 0, 0))
    InstructionLine3 = FontControlls.render("Space to jump", True, (0, 0, 0))
    InstructionLine4 = FontControlls.render("E to look forward", True, (0, 0, 0))
    InstructionLine5 = FontControlls.render("Q to look backward", True, (0, 0, 0))
    InstructionLine6 = FontControlls.render("Arrow Up to look up", True, (0, 0, 0))
    InstructionLine7 = FontControlls.render("Arrow Down to look down", True, (0, 0, 0))
    InstructionLine8 = FontControlls.render("M to toggle map", True, (0, 0, 0))
    InstructionLine9 = FontControlls.render("R to toggle rays", True, (0, 0, 0))
    InstructionLine10 = FontControlls.render("Esc to close", True, (0, 0, 0))

    Instructions = [InstructionLine1, InstructionLine2, InstructionLine3, InstructionLine4, InstructionLine5, InstructionLine6, InstructionLine7, InstructionLine8, InstructionLine9, InstructionLine10]

    for i, instruction in enumerate(Instructions):
        screen.blit(instruction, (10, 30 * i + 420))

    WarningFont = pygame.font.Font(None, 30)
    WarningText = WarningFont.render("Opening the map will show you the layout and remove the first person aspect of the game, try beating the game witouth it first!", True, (255, 0, 0))
    screen.blit(WarningText, (MenuScreen.get_width() / 2 - WarningText.get_width() / 2, 30))

    if key[pygame.K_RETURN]:
        Menu = False
        running = True
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Menu = False

    pygame.display.flip()


#Map deffenitions
Mapwidth = 160
Mapheight = 90
Largemap = False
RayShow = False
#Movement deffinitions
PlayerSpawnX = -40
PlayerSpawnY = 20
player = pygame.Rect(PlayerSpawnX, PlayerSpawnY, 5, 10)
playerX = float(PlayerSpawnX)
playerY = float(PlayerSpawnY)
VelocityX = 0
VelocityY = 0
Gravity = 0.07
MovementAcceleration = 0.2
SlowdownX = 0.05


pov = pygame.Surface((1280, 720))
map = pygame.Surface((Mapwidth, Mapheight))
map_for_screen = pygame.transform.scale(map, (Mapwidth, Mapheight))

#Camera deffinitions
#Map
CamSize = 1
Cam = pygame.Rect(0, 0, int(160 * CamSize), int(90 * CamSize))
CamBufferX = 10
CamBufferYHigh = 10
CamBufferYLow = 4
#POV
PovAngle = 0

# Terain deffinitions
Platforms = [pygame.Rect(-200, 80, 530, 200), #Floor
             pygame.Rect(-200, -50, 600, 60), #Ceiling
             pygame.Rect(-200, -50, 100, 130), #Backwall
             pygame.Rect(80, 60, 50, 20),
             pygame.Rect(80, 0, 50, 30),
             pygame.Rect(200, 70, 20, 10,), #Stairs
             pygame.Rect(210, 60, 20, 10),
             pygame.Rect(220, 50, 20, 10),
             pygame.Rect(230, 40, 20, 10),
             pygame.Rect(240, 30, 10, 10),
             pygame.Rect(310, 10, 10, 60),
             pygame.Rect(300, 20, 10, 50),
             pygame.Rect(290, 30, 10, 40),
             pygame.Rect(280, 40, 10, 30),
             pygame.Rect(270, 50, 10, 20),
             pygame.Rect(260, 60, 10, 10),
             pygame.Rect(400, -50, 50, 230), #End wall
             pygame.Rect(300, 200, 200, 100),
             pygame.Rect(400, 0, 500, 120), #Low Ceiling
             pygame.Rect(500, 220, 220, 100), #Pitbottomm
             pygame.Rect(510, 190, 20, 5), #Platforms above pit
             pygame.Rect(560, 190, 20, 5),
             pygame.Rect(610, 190, 20, 5),
             pygame.Rect(660, 190, 20, 5),
             pygame.Rect(710, 190, 300, 130), #Pit End
             pygame.Rect(900, 0, 500, 300)]# Ending Wall

#Game Loop
while running:

    #Last frame data
    OldX = playerX
    OldY = playerY
    OnGround = False

    pov.fill((255, 255, 255))
    map.fill((150, 150, 150))

    #On Ground Check
    for Platform in Platforms:
        if pygame.Rect(int(playerX), int(playerY)+player.height, player.width, 1).colliderect(Platform):
            OnGround = True
            break
        else:
            OnGround = False

    key = pygame.key.get_pressed()

    #jump    
    if key[pygame.K_SPACE]and OnGround:
        VelocityY = -1.5
    # Resolve Movement Y
    VelocityY += Gravity
    playerY += VelocityY

    #Colision Y
    for Platform in Platforms:
        if pygame.Rect(int(playerX), int(playerY), player.width, player.height).colliderect(Platform):
            if OldY < playerY: #Colision from above
                playerY = Platform.y - player.height
                VelocityY = 0
                break
            if OldY > playerY: #Colision from below
                playerY = Platform.y + Platform.height
                VelocityY = 0


    # Key Toggles
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            # Map Toggle
            if event.key == pygame.K_m:
                if Largemap == True:
                    Largemap = False
                else:
                    Largemap = True
            # Show Rays
            if event.key == pygame.K_r:
                if RayShow == True:
                    RayShow = False
                else:
                    RayShow = True

        if event.type == pygame.QUIT:
            running = False

    # Key Hold
    # Movement X
    if key[pygame.K_ESCAPE]:
        running = False
    if key[pygame.K_w]:
        if OnGround:
            VelocityX = 1
        else:
            if VelocityX > 1:
                VelocityX = 1
            VelocityX += MovementAcceleration

    if key[pygame.K_s]:
        if OnGround:
            VelocityX = -1
        else:
            if VelocityX < -1:
                VelocityX = -1
            VelocityX -= MovementAcceleration
    if key[pygame.K_s] == False and key[pygame.K_w] == False:
        if OnGround:
            VelocityX = 0
    if OnGround == False:
        if VelocityX > 0:
            VelocityX -= SlowdownX
        if VelocityX < 0:
            VelocityX += SlowdownX
    if VelocityX < 0.05 and VelocityX > -0.05:
        VelocityX = 0

    # Resolve Movement X
    if VelocityX > 1:
        VelocityX = 1
    if VelocityX < -1:
        VelocityX = -1
    playerX += VelocityX

    #Colision X
    for Platform in Platforms:
        if pygame.Rect(int(playerX), int(playerY), player.width, player.height).colliderect(Platform):
            if OldX < playerX: #Colision from the right
                 playerX = Platform.x - player.width
                 VelocityX = 0
                 break
            if OldX > playerX: #Colision from the left
                 playerX = Platform.x + Platform.width
                 VelocityX = 0

    # Camera movement POV
    if key[pygame.K_UP]:
        PovAngle += 1
    if key[pygame.K_DOWN]:
        PovAngle -= 1
    if key[pygame.K_e]:
        PovAngle = 0
    if key[pygame.K_q]:
        PovAngle = 200


    # Camera movement Map
    # X Directions
    if playerX > Cam.x + Cam.width/2 + CamBufferX:
        Cam.x = playerX - Cam.width/2 - CamBufferX
    if playerX < Cam.x + Cam.width/2 - CamBufferX:
        Cam.x = playerX - Cam.width/2 + CamBufferX
    # Y Directions
    if playerY > Cam.y + Cam.height/2 + CamBufferYLow:
        Cam.y = playerY - Cam.height/2 - CamBufferYLow
    if playerY < Cam.y + Cam.height/2 - CamBufferYHigh:
        Cam.y = playerY - Cam.height/2 + CamBufferYHigh

    # Render Platforms
    for Platform in Platforms:
        pygame.draw.rect(
        map,
        (0, 0, 0),
        pygame.Rect(
        int((Platform.x - Cam.x) * map.get_width() / Cam.width),
        int((Platform.y - Cam.y) * map.get_height() / Cam.height),
        int(Platform.width * map.get_width() / Cam.width),
        int(Platform.height * map.get_height() / Cam.height),),)
    
    # Render Player
    pygame.draw.rect(
    map,
    (200, 0, 0),
    pygame.Rect(
    int((playerX - Cam.x) * map.get_width() / Cam.width),
    int((playerY - Cam.y) * map.get_height() / Cam.height),
    int(player.width * map.get_width() / Cam.width),
    int(player.height * map.get_height() / Cam.height),),)

    # Render map
    if Largemap:
        map_for_screen = pygame.transform.scale(map, (1280, 720))
    else:
         map_for_screen = map


    playerx = int(playerX)
    playerY = int(playerY)
    #  Ray casting
    for RayIndex in range(122):
        RayHit = False
        angle = math.radians(RayIndex / 3 - PovAngle - 20)
        dx = math.cos(angle)
        dy = math.sin(angle)
        for dist in range (1, 128, 2):
            rx = int(playerX+ dx * dist)
            ry = int(playerY + dy * dist)
            for plat in Platforms:
                if plat.collidepoint(rx, ry):
                    RayHit = True
                    colour = int(dist*2)
                    break
            if RayHit == True:
                break
            
        if RayHit == True:
            pygame.draw.line(pov, (colour, colour, colour), (0, RayIndex*6), (1280, RayIndex*6), 6)
        #Show Rays
        if RayShow == True:
            pygame.draw.line(map_for_screen, (255, 0, 0), (int(playerX - Cam.x) * map_for_screen.get_width() / Cam.width, int(playerY - Cam.y) * map_for_screen.get_height() / Cam.height), (int(rx- Cam.x) * map_for_screen.get_width() / Cam.width, int(ry - Cam.y) * map_for_screen.get_height() / Cam.height), 1)


    ViewAngle = math.radians(-PovAngle)
    ViewSize = 75
    # Points for Head
    Point = namedtuple('Point', ['x', 'y'])
    center = Point(100, 620)
    SquareHeight = 80
    SquareWidth = 40
    CornersSquare = [
        (SquareWidth/2, -SquareHeight/2),
        (SquareWidth/2, SquareHeight/2),
        (-SquareWidth/2, SquareHeight/2),
        (-SquareWidth/2, -SquareHeight/2),
    ]

    # Point for triangle
    forward_x = math.cos(ViewAngle)
    forward_y = math.sin(ViewAngle)
    side_x = -forward_y
    side_y = forward_x
    tip_offset = SquareWidth / 2
    base_offset = SquareWidth / 2 + 80
    wing_half = 20
    height_shift = -SquareHeight / 6
    Triangle = [
        (center.x + forward_x * tip_offset + side_x * height_shift, center.y + forward_y * tip_offset + side_y * height_shift),
        (center.x + forward_x * base_offset + side_x * (wing_half + height_shift), center.y + forward_y * base_offset + side_y * (wing_half + height_shift)),
        (center.x + forward_x * base_offset + side_x * (-wing_half + height_shift), center.y + forward_y * base_offset + side_y * (-wing_half + height_shift)),
    ]

    pygame.draw.polygon(pov, (140, 240, 240), Triangle)
    Counter = 0
    for dx, dy in CornersSquare:
        rx = int(dx * math.cos(ViewAngle) - dy * math.sin(ViewAngle))
        ry = int(dx * math.sin(ViewAngle) + dy * math.cos(ViewAngle))
        CornersSquare[Counter] = center.x + rx, center.y + ry
        Counter += 1
    Counter = 0

    pygame.draw.polygon(pov, (255, 255, 0), CornersSquare)

    # Render screens
    screen.blit(pov,(0, 0))

    # Comment to show map
    if Largemap:
        screen.blit(map_for_screen, (0, 0))

    if playerX > 800:
        FontWin = pygame.font.Font(None, int(100))
        WinText = FontWin.render("Your reached the end, Yaay", True, (0, 255, 0))
        screen.blit(WinText, (pov.get_width() / 2 - WinText.get_width() / 2, pov.get_height() / 2 - WinText.get_height()))


    # End loop with clock
    clock.tick(60)
    pygame.display.flip()
pygame.quit()