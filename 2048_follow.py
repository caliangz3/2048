import turtle
import random


### backgound设定
#########################################################################
grid_bg = "grid_bg.gif"
title_bg = "title2.gif"
current_score_bg = "score.gif"
top_score_bg = "top_score.gif"

#设置窗口大小
screen = turtle.Screen()
screen.title("2048")
screen.bgcolor("gray")
screen.setup(width=600, height=700)
screen.register_shape(grid_bg)
screen.register_shape(title_bg)
screen.register_shape(current_score_bg)
screen.register_shape(top_score_bg)

def draw_boundary(turtle, pos_lst):
    turtle.penup()
    turtle.hideturtle()
    turtle.goto(pos_lst[0])
    turtle.pendown()
    
    turtle.color("white", "white")
    turtle.width(5)
    turtle.speed(5)

    for pos in pos_lst[1:]:
        turtle.goto(pos)

    

def draw_bg_squares(turtle, pos_lst, filename):
    turtle.penup()
    turtle.shape(filename)
    
    for pos in pos_lst:
        turtle.goto(pos)
        turtle.stamp() 
        

### 实际运行 background
#########################################################################
bg_t = turtle.Turtle()

# 2048 title
title_pos = [(-140, 215)]
draw_bg_squares(bg_t, title_pos, title_bg)

# current score
current_score_pos = [(100, 252)]
draw_bg_squares(bg_t, current_score_pos, current_score_bg)

# highest score
highest_score_pos = [(100, 179)]
draw_bg_squares(bg_t, highest_score_pos, top_score_bg)

#drawing boundary around grids
line_pos = [(-210.5,91), (-210.5, -310), (190, -310), (190, 91), (-210.5,91)]
draw_boundary(bg_t, line_pos)

# drawing the 16 squares
grid_pos = [(-160,40), (-160, -60), (-160, -160), (-160, -260),
            (-60,40),  (-60, -60),  (-60, -160), (-60, -260),
            (40,40),   (40, -60),   (40, -160), (40, -260),
            (140, 40), (140, -60),  (140, -160), (140, -260)]
draw_bg_squares(bg_t, grid_pos, grid_bg)

# score
current_score = 0
current_score_turtle = turtle.Turtle()
current_score_turtle.ht()
current_score_turtle.penup()
current_score_turtle.goto(100, 230)
#current_score_turtle.clear()
current_score_turtle.write(current_score, align = "center", font = ("Arial", 20, "bold"))

# highest score
fin = open("highest_score.txt")
highest_score_initial = int(fin.readline())
fin.close()

highest_score = highest_score_initial
highest_score_turtle = turtle.Turtle()
highest_score_turtle.ht()
highest_score_turtle.penup()
highest_score_turtle.goto(100, 155)
#highest_score_turtle.clear()
highest_score_turtle.write(highest_score, align = "center", font = ("Arial", 20, "bold"))


### 内部建搭
#########################################################################
screen.register_shape("2.gif")
screen.register_shape("4.gif")
screen.register_shape("8.gif")
screen.register_shape("16.gif")
screen.register_shape("32.gif")
screen.register_shape("64.gif")
screen.register_shape("128.gif")
screen.register_shape("256.gif")
screen.register_shape("512.gif")
screen.register_shape("1024.gif")
screen.register_shape("2048.gif")
screen.register_shape("4096.gif")
screen.register_shape("8192.gif")
all_pos = grid_pos.copy()                       #在all_pos里代表这个位置现在是空的
block_list = []
move_time = 0
win_2048 = True
win_text = "Congratulations, You WIN!! \n If continue, please hit enter"
lose_text = "Game Over !! \n  If continue, please hit Space"

def random_emerge(turtle):
    num = random.choice([2,2,2,2,4])
    #num = random.choice([2, 16, 8, 128, 512, 2048])
    num_pos = random.choice(all_pos)
    filename = str(num) + ".gif"
    
    turtle.penup()
    #turtle.showturtle()
    turtle.shape(filename)
    turtle.speed(10)
    turtle.goto(num_pos)
    
    all_pos.remove(num_pos)                     #占了的格子remove掉
    block_list.append(turtle)                   #把存在的turtle存起来，后续可以直接用来动


def move(turtle, gox, goy):
    #turtle.penup()
    global move_time, win_2048, current_score, highest_score
    if (gox, goy) in all_pos:                   #这个位置现在是空的
        all_pos.append(turtle.pos())
        turtle.goto(gox, goy)
        turtle.speed(10)
        all_pos.remove((gox, goy))
        move_time += 1
    else:                                      #这个位置被占了
        # 找到现在是哪个tutle在那里
        for exist in block_list:
            if exist.pos() == (gox, goy) and exist.shape() == turtle.shape():
                #current_x = turtle.pos()[0]
                #current_y = turtle.pos()[1]
                all_pos.append(turtle.pos())
                
                turtle.goto(gox, goy)
                turtle.speed(10)
                turtle.ht()
                
                block_list.remove(turtle)
                
                current_num = exist.shape()
                dot_index = current_num.index(".")
                current_num = int(current_num[:dot_index])
                
                new_filename = str(current_num * 2) + ".gif"
                exist.shape(new_filename)
                
                move_time += 1
                
                current_score = current_score + 2 * current_num
                current_score_turtle.clear()
                current_score_turtle.write(current_score, align = "center", font = ("Arial", 20, "bold"))                
                
                
                if current_num == 1024 and win_2048:
                    win_2048 = False
                    win_lose(text_turtle, win_text)
    
    if current_score > highest_score:
        highest_score = current_score
        highest_score_turtle.clear()
        highest_score_turtle.write(highest_score, align = "center", font = ("Arial", 20, "bold"))
        
                    
                
def go(move_one, move_two, move_three, move_x, move_y, move_direction):
    global move_time
    move_time = 0
    if move_direction == "up" or move_direction == "down":
        one = list(filter(lambda turtle: turtle.pos()[1] == move_one, block_list))
        two = list(filter(lambda turtle: turtle.pos()[1] == move_two, block_list))
        three = list(filter(lambda turtle: turtle.pos()[1] == move_three, block_list))
    else:
        one = list(filter(lambda turtle: turtle.pos()[0] == move_one, block_list))
        two = list(filter(lambda turtle: turtle.pos()[0] == move_two, block_list))
        three = list(filter(lambda turtle: turtle.pos()[0] == move_three, block_list))        
    
    for t in one:
        move(t, t.pos()[0] + move_x, t.pos()[1] + move_y)
    for t in two:
        for i in range(2):
            move(t, t.pos()[0] + move_x, t.pos()[1] + move_y)  
    for t in three:
        for i in range(3):
            move(t, t.pos()[0] + move_x, t.pos()[1] + move_y)
    
    if move_time != 0:
        new_turtle = turtle.Turtle()
        random_emerge(new_turtle)  
    
    if game_stop():
        win_lose(text_turtle, lose_text)
        if highest_score > highest_score_initial:
            fout = open("highest_score.txt", "w")
            fout.write(str(highest_score))
            fout.close()
        
        
        
                       
def go_down():
    go(-160, -60, 40, 0, -100, "down")

def go_up():
    go(-60, -160, -260,0, 100, "up")

def go_left():
    go(-60, 40, 140, -100, 0, "left")

def go_right():
    go(40, -60, -160, 100, 0, "right")

def win_lose(turtle, text):
    turtle.penup()
    turtle.color("blue")
    
    
    turtle.write(text, align = "center", font = ("黑体", 30, "bold"))


def check_horizontal_stop():
    '''
    Returns True if cannot move in horizontally
    '''
    y_pos = [40, -60, -160, -260]
    x_pos_combine = [[-160, -60], [-60, 40], [40, 140]]
    for num in y_pos:
        row = list(filter(lambda turtle: turtle.pos()[1] == num, block_list))
        for x_pos in x_pos_combine:
            first = list(filter(lambda turtle: turtle.pos()[0] == x_pos[0], row))
            first = first[0]
            second = list(filter(lambda turtle: turtle.pos()[0] == x_pos[1], row))
            second = second[0]
            if first.shape() == second.shape():
                return False
    return True

def check_vertical_stop():
    '''
    Returns True if cannot move in vertically
    '''
    column_num = [-160, -60, 40, 140]
    y_pos_combine = [[40,-60], [-60, -160], [-160, -260]]
    for col in column_num:
        column = list(filter(lambda turtle: turtle.pos()[0] == col, block_list))
        for y_pos in y_pos_combine:
            first = list(filter(lambda turtle: turtle.pos()[1] == y_pos[0], column))
            first = first[0]
            second = list(filter(lambda turtle: turtle.pos()[1] == y_pos[1], column))
            second = second[0]
            if first.shape() == second.shape():
                return False
    return True
        


def game_stop():
    '''
    Return True if the game should stop
    '''
    if all_pos == [] and check_horizontal_stop() and check_vertical_stop():
        return True
    else:
        return False

def restart():
    global all_pos, block_list, move_time, win_2048, current_score
    all_pos = grid_pos.copy()                      
    
    for tur in block_list:
        tur.clear()
        tur.ht()
    block_list = []
    
    move_time = 0
    win_2048 = True    
    #block_turtle.clear()
    text_turtle.clear()
    
    new_turtle = turtle.Turtle()
    random_emerge(new_turtle)
    
    current_score = 0
    current_score_turtle.clear()
    current_score_turtle.write(current_score, align = "center", font = ("Arial", 20, "bold"))
    
    
    

######################################################################## start
block_turtle = turtle.Turtle()
random_emerge(block_turtle)
#move(block_turtle, block_turtle.pos()[1], -260, all_pos)

screen.listen()
screen.onkey(go_down, 'Down')
screen.onkey(go_left, 'Left')
screen.onkey(go_up, 'Up')
screen.onkey(go_right, 'Right')

######################################################################## Check win
text_turtle = turtle.Turtle()
text_turtle.ht()
screen.onkey(text_turtle.clear, 'Return')

#######################################################################  Restart
screen.onkey(restart, "space")




screen.mainloop()
