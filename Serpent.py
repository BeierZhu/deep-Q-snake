import cv2
import sys
from game import serpent as game
from BrainDQN_Nature import BrainDQN
import numpy as np

# preprocess raw image to 80*80 gray image
def preprocess(observation):
	observation = cv2.cvtColor(cv2.resize(observation, (80, 80)), cv2.COLOR_BGR2GRAY)
	ret, observation = cv2.threshold(observation,1,255,cv2.THRESH_BINARY)
	return np.reshape(observation,(80,80,1))
def playGame():
	# Step 1: init BrainDQN
	actions = 5
	brain = BrainDQN(actions)
	# Step 2: init Game
	serpent = game.GameState()
	# Step 3: play game
	# Step 3.1: obtain init state
	average_reward = np.zeros(100)
	average_Q = np.zeros(100)
	average_score = np.zeros(100)
	episode_per_epoch = np.zeros(100)
	score_max_per_epoch = np.zeros(100)
	
	action0 = np.array([1,0,0,0,0])  # do nothing
	observation0, reward0, terminal,score0 = serpent.frame_step(action0)
	observation0 = cv2.cvtColor(cv2.resize(observation0, (80, 80)), cv2.COLOR_BGR2GRAY)
	ret, observation0 = cv2.threshold(observation0,1,255,cv2.THRESH_BINARY)
	brain.setInitState(observation0)

	# Step 3.2: run the game
	i = 1
	epoch_episode, epoch_reward, epoch_Q, epoch_score, score_max \
		= 1., 0., 0., 0., 0.

	while True:
		action, Q_value = brain.getAction()
		nextObservation,reward,terminal, score = serpent.frame_step(action)
		nextObservation = preprocess(nextObservation)
		brain.setPerception(nextObservation,action,reward,terminal)

		# Step 3.2.1 record Q and reward 
		epoch_Q += Q_value
		epoch_reward += reward

		if terminal == True:
			epoch_episode += 1
			epoch_score += score

		if score > score_max:
			score_max = score

		if i%50000 == 0:
			index = min(i/50000 - 1,99)

			average_reward[index] = epoch_reward/epoch_episode
			average_Q[index] = epoch_Q/50000
			average_score[index] = epoch_score/epoch_episode
			episode_per_epoch[index] = epoch_episode
			score_max_per_epoch[index] = score_max

			epoch_episode, epoch_reward, epoch_Q, epoch_score, score_max\
				= 1., 0., 0., 0., 0.

			print 'average reward and Q, average score, max score: ' + str(index)
			print average_reward[index], average_Q[index], average_score[index], score_max_per_epoch[index]


			np.savez("result.npz", average_reward=average_reward, average_Q=average_Q, \
					 episode_per_epoch=episode_per_epoch, average_score=average_score, \
					 score_max_per_epoch=score_max_per_epoch)

		i += 1



def main():
	playGame()

if __name__ == '__main__':
	main()