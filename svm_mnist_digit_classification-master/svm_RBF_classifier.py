# Standard scientific Python imports
import time
import datetime as dt

# Import datasets, classifiers and performance metrics
import scipy
from sklearn import datasets, svm, metrics
# fetch original mnist dataset
from sklearn.datasets import fetch_mldata
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV

# Standard scientific Python imports
from matplotlib.colors import Normalize
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import csv


def main():
    # pick  random indexes from 0 to size of our dataset

    # ---------------- classification begins -----------------
    # scale data for [0,255] -> [0,1]
    # sample smaller size for testing
    # rand_idx = np.random.choice(images.shape[0],10000)
    # X_data =images[rand_idx]/255.0
    # Y      = targets[rand_idx]

    # full dataset classification
    # split data to train and test
    # from sklearn.cross_validation import train_test_split

    all_variables = scipy.io.loadmat('data_MNIST.mat')
    X_test = np.array(all_variables['Xtest'])
    X_train = np.array(all_variables['Xtrain'])
    y_test = np.array(all_variables['ytest'])
    y_train = np.array(all_variables['ytrain'])
    show_some_digits(X_test, y_test)

    ############### Classification with grid search ##############
    # If you don't want to wait, comment this section and uncommnet section below with
    # standalone SVM classifier

    # Warning! It takes really long time to compute this about 2 days

    # Create parameters grid for RBF kernel, we have to set C and gamma

    # generate matrix with all gammas
    # [ [10^-4, 2*10^-4, 5*10^-4],
    #   [10^-3, 2*10^-3, 5*10^-3],
    #   ......
    #   [10^3, 2*10^3, 5*10^3] ]
    # gamma_range = np.outer(np.logspace(-4, 3, 8),np.array([1,2, 5]))

    gamma_range = np.outer(np.logspace(-3, 0, 4), np.array([1, 5]))
    gamma_range = gamma_range.flatten()

    # generate matrix with all C
    C_range = np.outer(np.logspace(-1, 1, 3), np.array([1, 5]))
    # flatten matrix, change to 1D numpy array
    C_range = C_range.flatten()

    parameters = {'kernel': ['rbf'], 'C': C_range, 'gamma': gamma_range}

    svm_clsf = svm.SVC()
    grid_clsf = GridSearchCV(estimator=svm_clsf, param_grid=parameters, n_jobs=1, verbose=2)

    print('Время начала поиска параметров {}'.format(str(dt.datetime.now())))

    grid_clsf.fit(X_train, y_train)

    print('Время окончания поиска параметров {}'.format(str(dt.datetime.now())))
    sorted(grid_clsf.cv_results_.keys())

    classifier = grid_clsf.best_estimator_
    params = grid_clsf.best_params_

    scores = grid_clsf.cv_results_['mean_test_score'].reshape(len(C_range),
                                                              len(gamma_range))
    print(scores)
    plot_param_space_scores(scores, C_range, gamma_range)
    plot_param_space_scores_1(scores, C_range, gamma_range)

    for x in range(6):
        for y in range(8):
            print("c:", C_range[x], ", gamma:", gamma_range[y], ", score:", scores[x][y])

    ######################### end grid section #############

    # Now predict the value of the test
    expected = y_test
    print('Время начала классификации 10000 символов {}'.format(str(dt.datetime.now())))
    predicted = classifier.predict(X_test)
    print('Время окончанияа классификации 10000 символов {}'.format(str(dt.datetime.now())))

    show_some_digits(X_test, predicted, title_text="Predicted {}")

    print("Отчет для классификатора %s:\n%s\n"
          % (classifier, metrics.classification_report(expected, predicted)))

    cm = metrics.confusion_matrix(expected, predicted)
    print("Матрица совпадений:\n%s" % cm)

    plot_confusion_matrix(cm)

    print("Точность={}".format(metrics.accuracy_score(expected, predicted)))

    plt.show()


def show_some_digits(images, targets, sample_size=24, title_text='Digit {}'):
    '''
    Visualize random digits in a grid plot
    images - array of flatten gidigs [:,784]
    targets - final labels
    '''
    nsamples = sample_size
    rand_idx = np.random.choice(images.shape[0], nsamples)
    images_and_labels = list(zip(images[rand_idx], targets[rand_idx]))

    img = plt.figure(1, figsize=(15, 12), dpi=160)
    for index, (image, label) in enumerate(images_and_labels):
        plt.subplot(np.ceil(nsamples / 6.0), 6, index + 1)
        plt.axis('off')
        # each image is flat, we have to reshape to 2D array 28x28-784
        plt.imshow(image.reshape(28, 28), cmap=plt.cm.gray_r, interpolation='nearest')
        plt.title(title_text.format(label))


def plot_confusion_matrix(cm, title='Confusion matrix', cmap=plt.cm.Blues):
    """
    Plots confusion matrix,

    cm - confusion matrix
    """
    plt.figure(1, figsize=(15, 12), dpi=160)
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    plt.tight_layout()
    plt.ylabel('Исходные данные')
    plt.xlabel('Предсказанные данные')


class MidpointNormalize(Normalize):

    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y))


def plot_param_space_scores(scores, C_range, gamma_range):
    #
    # The score are encoded as colors with the hot colormap which varies from dark
    # red to bright yellow. As the most interesting scores are all located in the
    # 0.92 to 0.97 range we use a custom normalizer to set the mid-point to 0.92 so
    # as to make it easier to visualize the small variations of score values in the
    # interesting range while not brutally collapsing all the low score values to
    # the same color.

    # plt.figure(figsize=(8, 6))
    plt.figure(figsize=(2, 2))
    plt.subplots_adjust(left=.2, right=0.95, bottom=0.15, top=0.95)
    plt.imshow(scores, interpolation='nearest', cmap=plt.cm.jet)
    plt.xlabel('gamma')
    plt.ylabel('C')
    plt.colorbar()
    plt.xticks(np.arange(len(gamma_range)), gamma_range)
    plt.yticks(np.arange(len(C_range)), C_range)
    plt.title('Точность классификации')


def plot_param_space_scores_1(scores, C_range, gamma_range):
    data_names = gamma_range
    data_values = scores * 100

    dpi = 80
    fig = plt.figure(dpi=dpi, figsize=(1200 / dpi, 600 / dpi))
    mpl.rcParams.update({'font.size': 12})

    plt.title('Точность классификации в зависимости от параметров C и gamma')

    ax = plt.axes()
    ax.yaxis.grid(True, zorder=1)

    print(data_names)
    xs = range(len(data_names))
    print(xs)

    plt.bar([x - 0.38 for x in xs], data_values[0],
            width=0.15, color='darkgreen', label='C = %(C_range)1.1f' % {"C_range": C_range[0]},
            zorder=10)
    plt.bar([x - 0.23 for x in xs], data_values[1],
            width=0.15, color='green', label='C = %(C_range)1.1f' % {"C_range": C_range[1]},
            zorder=2)
    plt.bar([x - 0.08 for x in xs], data_values[2],
            width=0.15, color='limegreen', label='C = %(C_range)1.0f' % {"C_range": C_range[2]},
            zorder=2)

    plt.bar([x + 0.07 for x in xs], data_values[3],
            width=0.15, color='lime', label='C = %(C_range)1.0f' % {"C_range": C_range[3]},
            zorder=2)
    plt.bar([x + 0.22 for x in xs], data_values[4],
            width=0.15, color='greenyellow', label='C = %(C_range)1.0f' % {"C_range": C_range[4]},
            zorder=2)
    plt.bar([x + 0.37 for x in xs], data_values[5],
            width=0.15, color='yellow', label='C = %(C_range)1.0f' % {"C_range": C_range[5]},
            zorder=2)
    plt.xticks(xs, data_names)
    plt.xlabel('Значение параметра gamma')
    plt.ylabel('Точность, %')

    # fig.autofmt_xdate(rotation = 25)

    plt.legend(loc='upper right')
    fig.savefig('bars.png')


if __name__ == "__main__":  # If run as a script, create a test object
    main()
