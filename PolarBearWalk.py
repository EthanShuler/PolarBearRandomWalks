import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import math
import numpy as np
import random
import statistics
import pylab


class Random_Walks():
    def random_walks(self):
        radius = 200
        ice_pos_x = 200
        ice_pos_y = -100
        N = 2000  # no of steps per trajectory
        realizations = 20  # number of trajectories
        v = 1.0  # velocity (step size)
        # the width of the random walk turning angle distribution (the lower it is, the more straight the trajectory will be)
        theta_s_i = round(math.pi/3, 4)
        # theta_s_i = 0.5
        # w is the weighting given to the directional bias (and hence (1-w) is the weighting given to correlated motion)
        w = 0.5
        ratio_theta_s_brw_crw = 1
        plot_walks = 1

        theta_s_crw = np.multiply(
            ratio_theta_s_brw_crw, theta_s_i)
        theta_s_brw = theta_s_i

        x, y, time = self.BRCW(N, realizations, v,
                         theta_s_crw, theta_s_brw, w, ice_pos_x, ice_pos_y, radius)

        min_xs = []
        for i in range(len(x)):
            min_xs.append(x[i][-1])
        print(statistics.mean(min_xs))

        if plot_walks == 1:
            fig = plt.figure()

            # initialize axis, important: set the aspect ratio to equal
            ax = fig.add_subplot(111, aspect='equal')
            ax.plot(x.T, y.T)
            ax.set(xlim=(0, 400), ylim=(-200, 200))

            ax.add_artist(Circle(xy=(ice_pos_x, ice_pos_y), radius=radius, color='black'))
            plt.show()
        print(time)


# The funciton generate 2D Biased Corrolated Random Walks

    def BRCW(self, N, realizations, v, theta_s_crw, theta_s_brw, w, melted_x, melted_y, radius):
        X = np.zeros([realizations, N])
        Y = np.zeros([realizations, N])
        time = np.zeros(realizations)
        theta = np.zeros([realizations, N])
        X[:, 0] = 0
        Y[:, 0] = 0
        theta[:, 0] = 0

        for realization_i in range(realizations):
            step_i = 1
            needs_redirect = False
            while step_i < N:
                # theta_crw = theta[realization_i][step_i-1] + \
                #     (theta_s_crw * 2.0 * (np.random.rand(1, 1)-0.5))
                # theta_brw = (theta_s_brw * 2.0 * (np.random.rand(1, 1)-0.5))
                if needs_redirect:
                    theta_crw = theta[realization_i][step_i-1] + \
                        (theta_s_crw * 2.0 * (np.random.rand(1, 1)-0.5))
                    theta_brw = (3 * 2.0 *
                                 (np.random.rand(1, 1)-0.5))
                    needs_redirect = False
                else:
                    theta_crw = theta[realization_i][step_i-1] + \
                        (theta_s_crw * 2.0 * (np.random.rand(1, 1)-0.5))
                    theta_brw = (theta_s_brw * 2.0 *
                                 (np.random.rand(1, 1)-0.5))

                X[realization_i, step_i] = X[realization_i][step_i-1] + \
                    (v * (w*math.cos(theta_brw))) + \
                    ((1-w) * math.cos(theta_crw))
                Y[realization_i, step_i] = Y[realization_i][step_i-1] + \
                    (v * (w*math.sin(theta_brw))) + \
                    ((1-w) * math.sin(theta_crw))

                continue_bool = False
                
                if ((Y[realization_i][step_i] - melted_y)**2 + (X[realization_i][step_i] - melted_x)**2) <= radius**2:
                    # print(X[realization_i][step_i], Y[realization_i][step_i],
                    #       'iceberg', val_y, melted_x[i])
                    continue_bool = True
                    # print('i =', step_i)
                    needs_redirect = True
                if continue_bool:
                    if (X[realization_i][step_i]) < 400:
                        time[realization_i] += 1
                    continue

                current_x_disp = X[realization_i][step_i] - \
                    X[realization_i][step_i-1]
                current_y_disp = Y[realization_i][step_i] - \
                    Y[realization_i][step_i-1]

                current_direction = math.atan2(current_y_disp, current_x_disp)

                theta[realization_i, step_i] = current_direction
                if (X[realization_i][step_i]) < 400:
                    time[realization_i] += 1
                step_i += 1
        return X, Y, time


rdm_plt = Random_Walks()
rdm_plt.random_walks()
