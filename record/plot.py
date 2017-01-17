import numpy as np
import pylab as pl

# x = range(1,46)
# y = np.load('average_reward1.npy')
# y1 = y[0:20]
# y = np.load('average_reward2.npy')
# y2 = y[0:10]
# y = np.load('average_reward3.npy')
# y3 = y[0:15]
# y = np.concatenate((y1,y2,y3))
# print y
# pl.plot(x,y)
# pl.title('Average Reward on Retro Snake')
# pl.xlabel('Training Epochs')
# pl.ylabel('Average Reward per Episode')
# pl.show()

x = range(1,46)

y = np.load('result.npz')
q = y['average_reward']
q1 = q[0:4]

y = np.load('result1.npz')
q = y['average_reward']
q2 = q[0:16]

y = np.load('result2.npz')
q = y['average_reward']
q3 = q[0:25]

y = np.concatenate((q1,q2,q3))
print y
pl.plot(x,y*2)
pl.title('Average Reward on Retro Snake')
pl.xlabel('Training Epochs')
pl.ylabel('Average Reward per Episode')
pl.show()