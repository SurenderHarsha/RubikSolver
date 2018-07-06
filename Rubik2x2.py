import numpy
import random

def get_structure(i):
    return [[i,i],[i,i]]

class Rubik(object):
    # 4 is TOP FACE ,  5 is BOTTOM , 0 is front, 1 is right, 2 is left, 3 is back

    def move_face_clockwise(self,face):
        mat=self.cube[face]
        # For 2x2

        final_mat=[]
        for i in range(2):
            a=[]
            for j in [1,0]:
                a.append(mat[j][i])
            final_mat.append(a)

        self.cube[face]=final_mat
        return

    def move_face_anticw(self,face):
        mat=self.cube[face]
        final_mat=[]
        '''
        row1=mat[0]
        row2=mat[1]
        new_mat=[]
        new_mat.append(row1[1])
        new_mat.append(row2[1])
        final_mat.append(new_mat)
        new_mat=[]
        new_mat.append(row1[0])
        new_mat.append(row2[0])
        final_mat.append(new_mat)
        '''

        for i in [1,0]:
            a = []
            for j in [0, 1]:
                a.append(mat[j][i])
            final_mat.append(a)
        self.cube[face]=final_mat
        return


    def m0(self):
        #TOP, HORIZONTAL, RIGHT
        store=self.cube[3][0]
        self.cube[3][0]=self.cube[1][0]
        self.cube[1][0]=self.cube[0][0]
        self.cube[0][0]=self.cube[2][0]
        self.cube[2][0]=store
        self.move_face_anticw(4)
        return

    def m1(self):
        # TOP, HORIZONTAL, LEFT
        store=self.cube[0][0]
        self.cube[0][0]=self.cube[1][0]
        self.cube[1][0]=self.cube[3][0]
        self.cube[3][0]=self.cube[2][0]
        self.cube[2][0]=store
        self.move_face_clockwise(4)
        return

    def m2(self):
        # BOT , HORIZONTAL, RIGHT

        store=self.cube[3][-1]
        self.cube[3][-1]=self.cube[1][-1]
        self.cube[1][-1]=self.cube[0][-1]
        self.cube[0][-1]=self.cube[2][-1]
        self.cube[2][-1]=store

        self.move_face_clockwise(5)
        return

    def m3(self):
        # BOT , HORIZONTAL, LEFT
        store = self.cube[0][-1]
        self.cube[0][-1]=self.cube[1][-1]
        self.cube[1][-1]=self.cube[3][-1]
        self.cube[3][-1]=self.cube[2][-1]
        self.cube[2][-1]=store




        self.move_face_anticw(5)
        return

    def m4(self):
        #LEFT , VERTICAL , UP
        # 0, 3 ,4 ,5
        f0=[self.cube[0][0][0],self.cube[0][1][0]]
        f4=[self.cube[4][0][0],self.cube[4][1][0]]
        f5=[self.cube[5][0][0],self.cube[5][1][0]]
        f3=[self.cube[3][0][1],self.cube[3][1][1]]

        self.cube[0][0][0]=f5[0]
        self.cube[0][1][0]=f5[1]
        self.cube[4][0][0]=f0[0]
        self.cube[4][1][0]=f0[1]
        self.cube[3][0][1]=f4[1]
        self.cube[3][1][1]=f4[0]
        self.cube[5][0][0]=f3[1]
        self.cube[5][1][0]=f3[0]

        self.move_face_anticw(2)
        return

    def m5(self):
        #LEFT, VERTICAL , DOWN
        f0 = [self.cube[0][0][0], self.cube[0][1][0]]
        f4 = [self.cube[4][0][0], self.cube[4][1][0]]
        f5 = [self.cube[5][0][0], self.cube[5][1][0]]
        f3 = [self.cube[3][0][1], self.cube[3][1][1]]

        self.cube[0][0][0] = f4[0]
        self.cube[0][1][0] = f4[1]
        self.cube[4][0][0] = f3[1]
        self.cube[4][1][0] = f3[0]
        self.cube[3][0][1] = f5[1]
        self.cube[3][1][1] = f5[0]
        self.cube[5][0][0] = f0[0]
        self.cube[5][1][0] = f0[1]

        self.move_face_clockwise(2)
        return

    def m6(self):
        #RIGHT, VERTICAL, UP
        # 0, 3 ,4 ,5
        f0 = [self.cube[0][0][1], self.cube[0][1][1]]
        f4 = [self.cube[4][0][1], self.cube[4][1][1]]
        f5 = [self.cube[5][0][1], self.cube[5][1][1]]
        f3 = [self.cube[3][0][0], self.cube[3][1][0]]

        self.cube[0][0][1] = f5[0]
        self.cube[0][1][1] = f5[1]
        self.cube[4][0][1] = f0[0]
        self.cube[4][1][1] = f0[1]
        self.cube[3][0][0] = f4[1]
        self.cube[3][1][0] = f4[0]
        self.cube[5][0][1] = f3[1]
        self.cube[5][1][1] = f3[0]

        self.move_face_clockwise(1)
        return
    def m7(self):
        #RIGHT , VERTICAL, DOWN

        # LEFT, VERTICAL , DOWN
        f0 = [self.cube[0][0][1], self.cube[0][1][1]]
        f4 = [self.cube[4][0][1], self.cube[4][1][1]]
        f5 = [self.cube[5][0][1], self.cube[5][1][1]]
        f3 = [self.cube[3][0][0], self.cube[3][1][0]]

        self.cube[0][0][1] = f4[0]
        self.cube[0][1][1] = f4[1]
        self.cube[4][0][1] = f3[1]
        self.cube[4][1][1] = f3[0]
        self.cube[3][0][0] = f5[1]
        self.cube[3][1][0] = f5[0]
        self.cube[5][0][1] = f0[0]
        self.cube[5][1][1] = f0[1]

        self.move_face_anticw(1)
        return

    def m8(self):
        #Front , - , Clockwise
        f4=[self.cube[4][1][0],self.cube[4][1][1]]
        self.cube[4][1][0]=self.cube[2][1][1]
        self.cube[4][1][1]=self.cube[2][0][1]
        self.cube[2][1][1]=self.cube[5][0][1]
        self.cube[2][0][1]=self.cube[5][0][0]
        self.cube[5][0][1]=self.cube[1][0][0]
        self.cube[5][0][0]=self.cube[1][1][0]
        self.cube[1][0][0]=f4[0]
        self.cube[1][1][0]=f4[1]
        self.move_face_clockwise(0)
        return

    def m9(self):
        # Front , -, AntiCW
        f4 = [self.cube[4][1][0], self.cube[4][1][1]]
        self.cube[4][1][0] = self.cube[1][0][0]
        self.cube[4][1][1] = self.cube[1][1][0]
        self.cube[1][0][0]=self.cube[5][0][1]
        self.cube[1][1][0]=self.cube[5][0][0]
        self.cube[5][0][1]=self.cube[2][1][1]
        self.cube[5][0][0]=self.cube[2][0][1]
        self.cube[2][1][1]=f4[0]
        self.cube[2][0][1]=f4[1]
        self.move_face_anticw(0)
        return

    def m10(self):
        # Back, - , Clockwise
        f4=[self.cube[4][0][0],self.cube[4][0][1]]

        self.cube[4][0][0]=self.cube[2][1][0]
        self.cube[4][0][1]=self.cube[2][0][0]
        self.cube[2][1][0]=self.cube[5][1][1]
        self.cube[2][0][0]=self.cube[5][1][0]
        self.cube[5][1][1]=self.cube[1][0][1]
        self.cube[5][1][0]=self.cube[1][1][1]
        self.cube[1][0][1]=f4[0]
        self.cube[1][1][1]=f4[1]

        self.move_face_anticw(3)

        return
    def m11(self):
        #Back , - , AntiCW
        f4 = [self.cube[4][0][0], self.cube[4][0][1]]
        self.cube[4][0][0]=self.cube[1][0][1]
        self.cube[4][0][1]=self.cube[1][1][1]
        self.cube[1][0][1]=self.cube[5][1][1]
        self.cube[1][1][1]=self.cube[5][1][0]
        self.cube[5][1][1]=self.cube[2][1][0]
        self.cube[5][1][0]=self.cube[2][0][0]
        self.cube[2][1][0]=f4[0]
        self.cube[2][0][0]=f4[1]

        self.move_face_clockwise(3)
        return





    def __init__(self):
        self.cube={0:[],1:[],2:[],3:[],4:[],5:[]}
        self.moves=[self.m0,self.m1,self.m2,self.m3,self.m4,self.m5,self.m6,self.m7,self.m8,self.m9,self.m10,self.m11]


    def reset(self):
        for i in range(6):
            a=get_structure(i)
            self.cube[i]=a
    def get_cube(self):
        #print self.mv
        return self.cube
    def move(self,mov_num):
        self.moves[mov_num]()

    def shuffle(self,num):
        self.mv=[]
        for i in range(num):

            k=random.randint(0,11)
            self.mv.append(k)
            self.move(k)
        return self.mv

    def random_move(self):
        k=random.randint(0,11)
        self.move(k)

    def get_reward(self):
        total=0
        for i in self.cube.keys():
            l=self.cube[i]
            #print l
            for j in l:
                for k in j:
                    if k==i:
                        #print k,i
                        total+=1

        total=float(total)/24
        total=total*100
        return total
    def get_binary_cube(self):
        r=[]
        for i in self.cube.keys():
            l=self.cube[i]
            #print l
            for j in l:
                for k in j:
                    c='{0:03b}'.format(k)
                    #print c
                    for s in c:
                        r.append(int(s))
        return r



#a.move(2)
#a.shuffle(10)
#a.m9()
#a.m7()
#a.m5()
#a.move_face_anticw(1)
#a.move_face_anticw(1)
#a.move_face_clockwise(1)
#a.m1()


# 0- White, 1-orange, 2- red, 3-yelow, 4-green, 5-blue