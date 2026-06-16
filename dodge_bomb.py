import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0, -5),
    pg.K_DOWN:(0, 5),
    pg.K_LEFT:(-5, 0),
    pg.K_RIGHT:(5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRect or ばくだんRect
    戻り値：判定結果タプル（横方向判定結果，縦方向判定結果）
    画面内ならTrue,画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left <0 or WIDTH <rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate

def gameover(screen: pg.Surface) -> None:
    """
    引数：画面Surface
    戻り値：なし
    ゲームオーバーになった場合、ゲームオーバー画面を表示
    """
    go_img = pg.Surface((WIDTH, HEIGHT))
    go_rct = go_img.get_rect()
    go_img.set_alpha(200)
    fonto = pg.font.Font(None, 60)
    go_txt = fonto.render("Game Over", True, (255, 255, 255))
    txt_rct = go_txt.get_rect(center=(WIDTH // 2, HEIGHT // 2 ))
    cry_kk_img = pg.image.load("fig/8.png")
    cry_kk_rctR = cry_kk_img.get_rect(center=(WIDTH // 2 + 150, HEIGHT // 2 ))
    cry_kk_rctL = cry_kk_img.get_rect(center=(WIDTH // 2 - 150, HEIGHT // 2 ))
    go_img.blit(cry_kk_img, cry_kk_rctR)
    go_img.blit(cry_kk_img, cry_kk_rctL)
    go_img.blit(go_txt, txt_rct)
    screen.blit(go_img, go_rct)
    pg.display.update()
    time.sleep(5)
    return

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    引数：なし
    戻り値：pg.Surfaceが入ったリストが入ったタプル、整数のリスト
    時間とともに爆弾が拡大,加速する関数
    """
    bb_imgs = []
    bb_accs =[a for a in range(1, 11)]
    for r in list(range(1, 11)):
        bb_img = pg.Surface((20*r, 20*r))  
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)  
        bb_imgs.append(bb_img)
    return bb_imgs, bb_accs  

def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    """
    引数：なし
    戻り値：押下キーに対する移動量の合計値タプルをキー,rotozoomしたSurfaceを値とした辞書
    飛ぶ方向に従ってこうかとん画像を切り替える関数
    """
    kk_dict = {
        (0, 0):pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 1),
        (0, -5):pg.transform.rotozoom(pg.transform.flip(pg.image.load("fig/3.png"), True, False), 90, 1),
        (0, +5):pg.transform.rotozoom(pg.image.load("fig/3.png"), 90, 1),
        (-5, 0):pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 1),
        (+5, 0):pg.transform.flip(pg.image.load("fig/3.png"), True, False),
        (-5, -5):pg.transform.rotozoom(pg.image.load("fig/3.png"), 315, 1),
        (+5, -5):pg.transform.rotozoom(pg.image.load("fig/3.png"), 225, 1),
        (-5, +5):pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 1),
        (+5, +5):pg.transform.rotozoom(pg.image.load("fig/3.png"), 135, 1)
        }  
    return kk_dict

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5,+5
    clock = pg.time.Clock()
    
    tmr = 0
    bb_imgs, bb_accs =init_bb_imgs()
    kk_dict = get_kk_imgs()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            print("ゲームオーバー")
            return
        screen.blit(bg_img, [0, 0]) 

        avx = vx * bb_accs[min(tmr//500, 9)]
        avy = vy * bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)] 
        bb_img.set_colorkey((0, 0, 0))

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        
        bb_rct.move_ip(avx,avy)
        bb_rct.width=bb_imgs[min(tmr//500, 9)].get_rect().width 
        bb_rct.height=bb_imgs[min(tmr//500, 9)].get_rect().height 
        kk_img = kk_dict.get(tuple(sum_mv), kk_dict[(0, 0)])

        yoko, tate =check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
