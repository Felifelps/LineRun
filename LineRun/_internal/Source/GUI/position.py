from pyautogui import size, alert

'''
This class has methods that relate the window size (600, 900) with the real screen size, 
making the positions proportional to all screens.
'''

class Position:
    real_window_size = size()
    x_rel = (600/(real_window_size[0]/100))/100
    y_rel = (900/(real_window_size[1]/100))/100
    relative_game_screen_size = [real_window_size[0]*((600/(real_window_size[0]/100))/100), real_window_size[1]*((900/(real_window_size[1]/100))/100)]

    def rels(size, currentsize=[600, 900], newsize=relative_game_screen_size): #relative size
        rel = [newsize[0]/currentsize[0], newsize[1]/currentsize[1]]
        return [int(size[0] * rel[0]), int(size[1]*rel[1])]

    def relx(x, currentwidth=600, newwidth=relative_game_screen_size[0]):
        rel = newwidth/currentwidth
        return x * rel

    def rely(y, currentheight=900, newheight=relative_game_screen_size[1]):
        rel = newheight/currentheight
        return y * rel
    
    def relw(w, currentwidth=600, newwidth=relative_game_screen_size[0]):
        rel = newwidth/currentwidth
        return w * rel

    def relh(h, currentheight=900, newheight=relative_game_screen_size[1]):
        rel = newheight/currentheight
        return h * rel

    def msg(text):
        alert(text)

