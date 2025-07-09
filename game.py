import pygame
pygame.mixer.pre_init(44100, -16, 2, 256)  # 设置音频缓冲区大小
pygame.init()

#游戏开始类
class Game:
    def __init__(self):
        self.screen_w = 1050
        self.screen_h = 800
        self.w_move = False   #初始化 人物是否移动
        self.a_move = False
        self.s_move = False
        self.d_move = False
        self.screen = None
        self.clock = pygame.time.Clock()
        self.jq = []   #初始化一个剑气列表
        #self.ans = 0   #初始化正确操作的次数
        self.is_down = False    #游戏开始后，玩家是否点金键盘
        self.ziti = pygame.font.SysFont('华文行楷', 25)   #给游戏开始时的提示单开一个
        self.zhu = self.ziti.render('提示：作者为颜控，喜欢美女，请正确选择接触（英文模式下wasd） 或 攻击（空格）', True, 'white')
        self.zhu2 = self.ziti.render('注：游戏结算画面有个小按钮，找到了可以点击播放', True, 'white')
        self.zhu3 = self.ziti.render(('再注：播放一段音频时不要碰到其他人物（音频本身人物也不要碰，别问，问就是bug）'), True, 'white')

    def start_game(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_w,self.screen_h))   #Game.screen是类变量，即在这个类里面通用
        pygame.display.set_caption('坦克（燕云版）')
    def end_game(self):
        pygame.quit()
    def main_game(self):
        tp = TP()   #实例化图片类
        jc = JC()   #实例化接触类
        music = Music()   #实例化音乐
        while True:

            if self.w_move == True and tp.y > 0:   #如果这些放在下边的判断event里会导致移动速度不稳定（依赖事件触发频率）
                tp.y -= 5
            if self.a_move == True and tp.x > 0:
                tp.x -= 5
            if self.s_move == True and tp.y < self.screen_h - tp.player_h:
                tp.y += 5
            if self.d_move == True and tp.x < self.screen_w - tp.player_w:
                tp.x += 5                   #人物移动，并且限制在了窗口内
            tp.show(0)     #所有图片渲染到窗口上
            if self.is_down is False:   #玩家点击键盘前，显示作者提示
                game.screen.blit(self.zhu,(50,300))
                game.screen.blit(self.zhu2,(50,350))
                game.screen.blit(self.zhu3,(50,400))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.end_game()    #self代表Game类的实例，end_game代表实例方法
                if event.type == pygame.KEYDOWN:
                    self.is_down = True
                    if event.key == pygame.K_w:    #注意必须是在英文模式下的w
                        self.w_move = True
                        tp.direction = 'w'
                    if event.key == pygame.K_s:
                        self.s_move = True
                        tp.direction = 's'
                    if event.key == pygame.K_a:
                        self.a_move = True
                        tp.direction = 'a'
                    if event.key == pygame.K_d:
                        self.d_move = True
                        tp.direction = 'd'            #以上几行都是人物移动
                    if event.key == pygame.K_SPACE:    #按一次空格，往列表里加一个剑气实例     #其实写的时候就不太懂这个列表，如果按一次加一次且没有重置，而之后每次都要遍历一遍那个列表，不就会每次都出现很多个剑气吗，就算不按空格，那个列表里也已经有之前存下的剑气了啊
                        #start_x = tp.x
                        #start_y = tp.y
                        self.jq.append(JQ(tp.x,tp.y,tp.direction))  # 传入当前位置和方向

                if event.type == pygame.KEYUP:     #如果移动按键弹起，人物停止移动
                    if event.key == pygame.K_w:
                        self.w_move = False
                    if event.key == pygame.K_s:
                        self.s_move = False
                    if event.key == pygame.K_a:
                        self.a_move = False
                    if event.key == pygame.K_d:
                        self.d_move = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 470 < event.pos[0] < 470 + tp.new_bo_w and 375 < event.pos[1] < 375 + tp.new_bo_h:
                        music.play(8)
            for jq in self.jq:
                jq.move()   #剑气的移动
                jq.show()   #剑气在窗口上的渲染

            all_rect = [None,tp.rect1,tp.rect2,tp.rect3,tp.rect4,tp.rect5,tp.rect6,tp.rect7]
            #if len(self.jq) != 0:   #如果剑气列表里有剑气
                #all_rect2 = [None,jq.rect1,jq.rect2,jq.rect3,jq.rect4]
            for n,rect in enumerate(all_rect[2:5],start = 2):   #玩家与正确人物的接触
                if tp.rect1.colliderect(rect):
                    tp.show(n)
                    jc.show(n)
                    #self.ans += 1
                    tp.ans[n] = 1
                    music.play(n)

            for n,rect in enumerate(all_rect[5:],start = 15):   #玩家与错误人物的接触
                if tp.rect1.colliderect(rect):
                    jc.show(n)
            for jq in self.jq:
                for n,rect in enumerate(all_rect[2:5],start = 12):   #玩家错误攻击
                    if jq.rect1.colliderect(rect) or jq.rect2.colliderect(rect) or jq.rect3.colliderect(rect) or jq.rect4.colliderect(rect):
                        jc.show(n)
                for n,rect in enumerate(all_rect[5:],start = 5):   #玩家正确攻击
                    if jq.rect1.colliderect(rect) or jq.rect2.colliderect(rect) or jq.rect3.colliderect(rect) or jq.rect4.colliderect(rect):
                        tp.show(n)
                        jc.show(n)
                        #self.ans += 1
                        tp.ans[n] = 1
                        music.play(n)
            #print(self.ans)
            if 0 not in tp.ans:
                game.screen.blit(tp.new_image,(0,0))     #所有正确操作完成后，结算画面
                tp.show(8)    #容鸢播放图
            pygame.display.update()    #更新窗口
            self.clock.tick(60)
class TP:    #图片类
    def __init__(self):         #初始化游戏中的所有图片
        self.x = 500
        self.y = 400
        self.beijing = pygame.image.load(r'ziyuan\beijing.jpg')
        self.image = pygame.image.load(r'ziyuan\yanyun.jpg')
        self.new_image = pygame.transform.rotozoom(self.image,0,0.711)
        self.image1 = pygame.image.load(r'ziyuan\renwu.png')
        self.new_image1 = pygame.transform.rotozoom(self.image1,0,0.4)
        self.player_w, self.player_h = self.new_image1.get_size()
        self.rect1 = self.new_image1.get_rect()   #会返回一个 pygame.Rect 对象,这个矩形默认与图像尺寸相同（宽度=图像宽度，高度=图像高度）,需要手动设置它的位置
        self.image2 = pygame.image.load(r'ziyuan\hanyi.png')
        self.new_image2 = pygame.transform.rotozoom(self.image2,0,0.13)
        self.hanyi_w, self.hanyi_h = self.new_image2.get_size()
        self.rect2 = self.new_image2.get_rect()        #得到它们的矩形框，方便之后的碰撞检测
        self.image3 = pygame.image.load(r'ziyuan\rongyuan.png')
        self.new_image3 = pygame.transform.rotozoom(self.image3,0,0.13)
        self.rect3 = self.new_image3.get_rect()
        self.image4 = pygame.image.load(r'ziyuan\dongque.png')
        self.new_image4 = pygame.transform.rotozoom(self.image4,0,0.2)
        self.rect4 = self.new_image4.get_rect()
        self.image5 = pygame.image.load(r'ziyuan\heicaishen.png')
        self.new_image5 = pygame.transform.rotozoom(self.image5,0,0.2)
        self.rect5 = self.new_image5.get_rect()
        self.image6 = pygame.image.load(r'ziyuan\guigongzi.png')
        self.new_image6 = pygame.transform.rotozoom(self.image6,0,0.15)
        self.rect6 = self.new_image6.get_rect()
        self.image7 = pygame.image.load(r'ziyuan\zhenge.png')
        self.new_image7 = pygame.transform.rotozoom(self.image7,0,0.15)
        self.rect7 = self.new_image7.get_rect()
        self.direction = 'None'
        self.image12 = pygame.image.load(r'ziyuan\hanyi1.jpg')
        self.new_image12 = pygame.transform.rotozoom(self.image12,0,0.711)
        self.image13 = pygame.image.load(r'ziyuan\rongyuan1.jpg')
        self.new_image13 = pygame.transform.rotozoom(self.image13,0,0.73)
        self.image14 = pygame.image.load(r'ziyuan\dongque1.jpg')
        self.new_image14 = pygame.transform.rotozoom(self.image14,0,0.711)
        self.image15 = pygame.image.load(r'ziyuan\heicaishen1.jpg')
        self.new_image15 = pygame.transform.rotozoom(self.image15,0,0.73)
        self.image16 = pygame.image.load(r'ziyuan\guigongzi1.jpg')
        self.new_image16 = pygame.transform.rotozoom(self.image16,0,0.73)
        self.image17 = pygame.image.load(r'ziyuan\zhenge1.jpg')
        self.new_image17 = pygame.transform.rotozoom(self.image17,0,0.73)
        self.ans = [1,1,0,0,0,0,0,0]
        self.bo = pygame.image.load(r'ziyuan\zanting.png')   #播放容鸢
        self.new_bo = pygame.transform.rotozoom(self.bo,0,0.15)
        self.rect8 = self.new_bo.get_rect()
        self.new_bo_w, self.new_bo_h = self.new_bo.get_size()

    def show(self,who):
        self.rect1.x, self.rect1.y = self.x, self.y   #设置矩形的位置，如果是在上边的初始化中设置这个，那么这仅在 __init__ 中执行一次，后续修改 self.x 和 self.y 时，rect1 的坐标不会自动更新
        self.rect2.x, self.rect2.y = 200, 100
        self.rect3.x,self.rect3.y = 400,600
        self.rect4.x,self.rect4.y = 700, 100
        self.rect5.x, self.rect5.y = 650, 600
        self.rect6.x, self.rect6.y = 100, 600
        self.rect7.x, self.rect7.y = 900, 600
        self.rect8.x,self.rect8.y = 470,375
        if who == 0:
            game.screen.blit(self.beijing, (0,0))          #把所有图片都渲染到窗口上
            game.screen.blit(self.new_image1,(self.x,self.y))
            game.screen.blit(self.new_image2,(200,100))
            game.screen.blit(self.new_image3,(400,600))
            game.screen.blit(self.new_image4, (700, 100))
            game.screen.blit(self.new_image5, (650, 600))
            game.screen.blit(self.new_image6, (100, 600))
            game.screen.blit(self.new_image7, (900, 600))
        if who == 2:game.screen.blit(self.new_image12,(0,0))
        if who == 4:game.screen.blit(self.new_image14,(534,0))
        if who == 6:game.screen.blit(self.new_image16,(0,373))
        if who == 3:game.screen.blit(self.new_image13,(260,373))
        if who == 5:game.screen.blit(self.new_image15,(534,373))
        if who == 7:game.screen.blit(self.new_image17,(794,373))
        if who == 8:game.screen.blit(self.new_bo,(470,375))
class JC:    #接触类
    def __init__(self):       #初始化接触后显示的文字
        self.ziti = pygame.font.SysFont('华文行楷', 30)
        self.hanyi_t = self.ziti.render('寒姨我回来了！贴贴！', True, 'white')
        self.hanyi_f = self.ziti.render('逆天，寒香寻这么权威也敢打？？', True, 'white')
        self.rongyuan_t = self.ziti.render('容鸢姐姐你太帅了！', True, 'white')
        self.rongyuan_f = self.ziti.render('？？？我容鸢姐姐飒成这样你也敢打？',True, 'white')
        self.dongque_t = self.ziti.render('盈盈你深藏不露啊', True, 'white')
        self.dongque_f = self.ziti.render('这通身的贵气啊，要不说谁能看出这是盈盈',True, 'white')
        self.heicaishen_t = self.ziti.render('老登你敢欺负盈盈', True, 'white')
        self.heicaishen_f = self.ziti.render('孩纸你真是饿了，姓史的也往上贴',True, 'white')
        self.guigongzi_t = self.ziti.render('鬼公子你真的有点吓人', True, 'white')
        self.guigongzi_f = self.ziti.render('听我一句劝，人鬼殊途，别贴了',True, 'white')
        self.zhenge_t = self.ziti.render('郑鄂你其实长得也挺好看的', True, 'white')
        self.zhenge_f = self.ziti.render('虽然长得好看，可惜性别不对', True, 'white')
    def show(self,who):       #判断应该显示哪个文字内容
        if who == 2:game.screen.blit(self.hanyi_t,(180,120))
        if who == 12: game.screen.blit(self.hanyi_f, (180, 120))
        if who == 3:game.screen.blit(self.rongyuan_t,(300,620))
        if who == 13: game.screen.blit(self.rongyuan_f, (300,620))
        if who == 4:game.screen.blit(self.dongque_t,(600,130))
        if who == 14: game.screen.blit(self.dongque_f, (500, 130))
        if who == 5:game.screen.blit(self.heicaishen_t,(550,630))
        if who == 15: game.screen.blit(self.heicaishen_f, (550, 630))
        if who == 6:game.screen.blit(self.guigongzi_t,(20,630))
        if who == 16: game.screen.blit(self.guigongzi_f, (20, 630))
        if who == 7:game.screen.blit(self.zhenge_t,(700,630))
        if who == 17: game.screen.blit(self.zhenge_f, (650, 630))

'''class JQ:    #剑气类
    def __init__(self,x,y,direction):     #初始化了一堆东西
        self.image1 = None
        self.image2 = None
        self.image3 = None
        self.image4 = None
        self.v = 10
        self.x,self.y = x,y
        self.direction = direction  # 添加方向属性
        self.rect1 = None
        self.rect2 = None
        self.rect3 = None
        self.rect4 = None
    def show(self):
        if self.direction == 'w':self.image1 = pygame.draw.arc(game.screen,'black',(self.x,self.y,100,50),0.3,3,3)
        if self.direction == 's':self.image2 = pygame.draw.arc(game.screen,'black',(self.x-20,self.y,100,50),3,6,3)
        if self.direction == 'a':self.image3 = pygame.draw.arc(game.screen,'black',(self.x,self.y,50,100),1.6,4.5,3)
        if self.direction == 'd':self.image4 = pygame.draw.arc(game.screen,'black', (self.x, self.y, 50, 100), 4.5, 1.6, 3)
        self.rect1 = pygame.Rect(self.x,self.y,100,50)
        self.rect2 = pygame.Rect(self.x-20,self.y,100,50)
        self.rect3 = pygame.Rect(self.x,self.y,50,100)
        self.rect4 = pygame.Rect(self.x,self.y,50,100)
    def move(self):
        if self.direction == 'w':self.y -= self.v
        if self.direction == 's':self.y += self.v
        if self.direction == 'a':self.x -= self.v
        if self.direction == 'd':self.x += self.v'''
'''class Music:
    def __init__(self):
        pass
        #pygame.mixer.music.load(r'ziyuan\hanyi.wav')
        #self.rongyuan = pygame.mixer.music.load(r'ziyuan\rongyuan.mp3')
        #self.dongque = pygame.mixer.Sound(r'ziyuan\dongque2.mp3')
        #self.heicaishen = pygame.mixer.music.load(r'ziyuan\heicaishen.mp3')
        #self.guigongzi = pygame.mixer.music.load(r'ziyuan\guigongzi.mp3')
        #self.zhenge = pygame.mixer.music.load(r'ziyuan\zhenge.mp3')
    def play(self,who):
        if who == 2:
            pygame.mixer.music.load(r'ziyuan\hanyi.wav')
            pygame.mixer.music.play(0)
        if who == 3:
            pygame.mixer.music.load(r'ziyuan\rongyuan.wav')
            pygame.mixer.music.play(0)
        if who == 4:
            pygame.mixer.music.load(r'ziyuan\dongque2.mp3')
            pygame.mixer.music.play(0)
        if who == 5:
            pygame.mixer.music.load(r'ziyuan\heicaishen.wav')
            pygame.mixer.music.play(0)
        if who == 6:
            pygame.mixer.music.load(r'ziyuan\guigongzi.wav')
            pygame.mixer.music.play(0)
        if who == 7:
            pygame.mixer.music.load(r'ziyuan\zhenge.wav')
            pygame.mixer.music.play(0)'''

class JQ:    #剑气类
    def __init__(self,x,y,direction):     #初始化了一堆东西
        self.image = pygame.image.load(r'ziyuan\jianqi.png')
        self.image1 = pygame.transform.rotozoom(self.image,0,0.3)
        self.image2 = pygame.transform.rotozoom(self.image,180,0.3)
        self.image3 = pygame.transform.rotozoom(self.image,270,0.3)
        self.image4 = pygame.transform.rotozoom(self.image,90,0.3)
        self.v = 10
        self.x,self.y = x,y
        self.direction = direction  # 添加方向属性
        self.rect1 = None
        self.rect2 = None
        self.rect3 = None
        self.rect4 = None
    def show(self):
        if self.direction == 'w':game.screen.blit(self.image1,(self.x-30,self.y))
        if self.direction == 's':game.screen.blit(self.image1,(self.x-30,self.y))
        if self.direction == 'a':game.screen.blit(self.image1,(self.x,self.y))
        if self.direction == 'd':game.screen.blit(self.image1,(self.x,self.y))
        self.rect1 = pygame.Rect(self.x-30,self.y,100,50)
        self.rect2 = pygame.Rect(self.x-30,self.y,100,50)
        self.rect3 = pygame.Rect(self.x,self.y,50,100)
        self.rect4 = pygame.Rect(self.x,self.y,50,100)
    def move(self):
        if self.direction == 'w':self.y -= self.v
        if self.direction == 's':self.y += self.v
        if self.direction == 'a':self.x -= self.v
        if self.direction == 'd':self.x += self.v
class Music:
    def __init__(self):
        self.music_files = {
            2: r'ziyuan\hanyi.wav',
            3: r'ziyuan\rongyuan.wav',
            4: r'ziyuan\dongque2.mp3',
            5: r'ziyuan\heicaishen.wav',
            6: r'ziyuan\guigongzi.wav',
            7: r'ziyuan\zhenge.wav',
            8: r'ziyuan\rongyuan3.mp3'
        }

    def play(self, who):
        if who in self.music_files:
            pygame.mixer.music.stop()  # 停止当前音乐
            pygame.mixer.music.load(self.music_files[who])  # 加载新音乐
            pygame.mixer.music.play()  # 播放
game = Game()
game.start_game()
game.main_game()