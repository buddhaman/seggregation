import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import GridPrice as price
import GridBasic as grd

plt.rcParams['animation.ffmpeg_path'] = u"/Users/timtrussner/Downloads/Lion_Mountain_Lion_Mavericks_Yosemite_El-Captain_20.02.2017/ffmpeg"
width, height = 20,20
grid = grd.GridBasic(width, height, typeNums=[170,170], randomHouse=True,
                     happyThreshold=.7)
f=0
def generate_data():
    global f
    f=f+1
    gr = np.array(grid.getKindGrid()).reshape(width, height)
    if f>2:
        grid.step()
    return gr

def data_gen():
    while True:
        yield generate_data()
        
def update(data):
    mat.set_data(data)
    return mat

fig, ax = plt.subplots()
mat = ax.matshow(generate_data())
plt.colorbar(mat)
ani = animation.FuncAnimation(fig, update, data_gen, interval=100, 
                              save_count=300)

ani.save('basic_animation.mp4')
#plt.show()
