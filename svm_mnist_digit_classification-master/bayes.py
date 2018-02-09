import matplotlib

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
from tensorflow.contrib.distributions.python.ops import bijectors as bijectors
from tensorflow.contrib.distributions.python.ops.bijectors import *
import pandas as pd
import edward as ed
from edward.models import *


def main():
    # Use the TensorFlow method to download and/or load the data.
    mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)


if __name__ == "__main__":  # If run as a script, create a test object
    main()
