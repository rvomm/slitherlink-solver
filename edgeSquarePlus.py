
import edge 

class EdgeSquarePlus:
    """

    """

    def __init__(self, u, d, l, r, ul, ur, ru, rd, dr, dl, ld, lu):
        self.u = u
        self.ul = ul
        self.ur = ur 

        self.d = d
        self.dr = dr
        self.dl = dl
        
        self.l = l
        self.ld = ld
        self.lu = lu 

        self.r = r
        self.ru = ru
        self.rd = rd

    def rotate(self):
        self.rotate_outer()
        self.rotate_inner()

    def rotate_inner(self):
        tmp = self.u 
        self.u = self.l
        self.l = self.d
        self.d = self.r
        self.r = tmp

    def rotate_outer(self):
        tmp_ul = self.ul
        tmp_ur = self.ur 

        # left to upper
        self.ur = self.lu
        self.ul = self.ld

        # down to left
        self.lu = self.dl
        self.ld = self.dr

        # right to down
        self.dl = self.rd
        self.dr = self.ru

        # upper to right
        self.rd = tmp_ur
        self.ru = tmp_ul

    def draw(self):
        print(". . . . ")
        print("  " + self.ul.draw_v() + " " + self.ur.draw_v() + " " + "  ")
        print("." + self.lu.draw_h() + "." + self.u.draw_h() + "." + self.ru.draw_h() + ".")
        print("  " + self.l.draw_v() + " " + self.r.draw_v() + "  ")
        print("." + self.ld.draw_h() + "." + self.d.draw_h() + "." + self.rd.draw_h() + ".")
        print("  " + self.dl.draw_v() + " " + self.dr.draw_v() + " " + "  ")
        print(". . . . ")


if __name__ == "__main__":
    u = edge.Edge()
    u.make()
    ul = edge.Edge()
    ur = edge.Edge() 
    d = edge.Edge()
    dr = edge.Edge()
    dl = edge.Edge()
        
    l = edge.Edge()
    ld = edge.Edge()
    lu = edge.Edge() 
    r = edge.Edge()
    ru = edge.Edge()
    rd = edge.Edge()

    obj = EdgeSquarePlus(u, d, l, r, ul, ur, ru, rd, dr, dl, ld, lu)

    obj.draw()