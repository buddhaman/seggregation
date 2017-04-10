import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import GridPrice as price
import GridBasic as grd
from matplotlib import colors

plt.rcParams['animation.ffmpeg_path'] = u"/Users/timtrussner/Downloads/Lion_Mountain_Lion_Mavericks_Yosemite_El-Captain_20.02.2017/ffmpeg"
width, height = 8,8
#grid = price.GridPrice(width, height, typeNums=[10]*30, order=2, randomMoveProb=0.01)
grid = grd.GridBasic(width, height, typeNums=[20,20], order=1)
f=0

def generate_data():
    global f
    f=f+1
    gr = np.array(grid.getKindGrid()).reshape(width, height)
    if f>2:
        for i in range(100):
            grid.step()
    for i in range(100):
        grid.step()
    gr = np.array(grid.getKindGrid()).reshape(width, height)
    return gr

def data_gen():
    while True:
        yield generate_data()

def update(data):
    mat.set_data(data)
    return mat

def basicPlot():
    fig, ax = plt.subplots()
    #maak colormap
    cmap = colors.ListedColormap(['white', 'tomato', 'khaki' ])
    bounds=[0,1,2,3]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    mat = ax.matshow(generate_data(), cmap=cmap, norm=norm, interpolation='nearest',
                 origin='lower')
    plt.show()

def extensionPlot():
    fig, ax = plt.subplots()
    mat = ax.matshow(generate_data())

    plt.colorbar(mat)
    ani = animation.FuncAnimation(fig, update, data_gen, interval=100, 
                              save_count=20)

    ani.save('basic_animation.mp4')
    plt.show()
    
basicPlot()



