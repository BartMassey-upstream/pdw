class Tile():
    def __init__(self, sourceSurface, left, top, right, bottom):
        width = right - left + 1
        height = bottom - top + 1
        
        self.image = sourceSurface.subsurface( (left,top,width,height))
        self.left = left
        self.top = top
    
    def paint(self,screen):
        screen.blit(self.image, [self.left,self.top])