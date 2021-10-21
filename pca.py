from scipy.linalg import eigh
import numpy as np
import matplotlib.pyplot as plt

def load_and_center_dataset(filename):
    # TODO: add your code here
    x = np.load(filename)
    mean = np.mean(x, axis = 0)
    return x - np.mean(x, axis = 0)

def get_covariance(dataset):
    # TODO: add your code here
    data_transpose = np.transpose(dataset)
    dot_prod = np.dot(data_transpose, dataset)
    return dot_prod / (dataset.shape[0] - 1)

def get_eig(S, m):
    # TODO: add your code here
    eigens = eigh(S, eigvals = (S.shape[0] - m, S.shape[0] - 1))
    return np.diag(eigens[0][::-1]), np.fliplr(eigens[1])

def get_eig_perc(S, perc):
    # TODO: add your code here
    eigens = eigh(S)
    values = eigens[0]
    original_len = len(values)
    vectors = eigens[1]
    kept_values = values[values > (values.sum() * perc)]
    new_len = len(kept_values)
    new_vector = np.delete(vectors, np.s_[0:original_len - new_len], axis = 1)
    return np.diag(kept_values[::-1]), np.fliplr(new_vector)

def project_image(img, U):
    # TODO: add your code here
    a = np.dot(np.transpose(U), img)
    return np.dot(U, a)

def display_image(orig, proj):
    # TODO: add your code here
    figure, axes = plt.subplots(nrows = 1, ncols = 2)
    axes[0].set_title("Original")
    axes[1].set_title("Projection")
    p1 = axes[0].imshow(np.transpose(np.reshape(orig, (32, 32))), aspect = 'equal')
    p2 = axes[1].imshow(np.transpose(np.reshape(proj, (32, 32))), aspect = 'equal')
    figure.colorbar(p1, ax = axes[0])
    figure.colorbar(p2, ax = axes[1])
    plt.show()
    return None
