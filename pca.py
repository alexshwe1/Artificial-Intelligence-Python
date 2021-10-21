"""
In this project, I implement a facial analysis program using 
Principal Component Analysis (PCA), using the skills 
learned from the linear algebra + PCA lectures.
"""

from scipy.linalg import eigh
import numpy as np
import matplotlib.pyplot as plt

def load_and_center_dataset(filename):
    # load the dataset from a provided .npy file, re-center it around the origin and return it as a NumPy array of floats
    x = np.load(filename)
    mean = np.mean(x, axis = 0)
    return x - np.mean(x, axis = 0)

def get_covariance(dataset):
    # calculate and return the covariance matrix of the dataset as a NumPy matrix (d x d array)
    data_transpose = np.transpose(dataset)
    dot_prod = np.dot(data_transpose, dataset)
    return dot_prod / (dataset.shape[0] - 1)

def get_eig(S, m):
    # perform eigen decomposition on the covariance matrix S and return a diagonal matrix (NumPy array) with the largest m 
    # eigenvalues on the diagonal, and a matrix (NumPy array) with the corresponding eigenvectors as columns
    eigens = eigh(S, eigvals = (S.shape[0] - m, S.shape[0] - 1))
    return np.diag(eigens[0][::-1]), np.fliplr(eigens[1])

def get_eig_perc(S, perc):
    # similar to get_eig, but instead of returning the first m, return all eigenvalues and corresponding eigenvectors 
    # in similar format as get_eig that explain more than perc % of variance
    eigens = eigh(S)
    values = eigens[0]
    original_len = len(values)
    vectors = eigens[1]
    kept_values = values[values > (values.sum() * perc)]
    new_len = len(kept_values)
    new_vector = np.delete(vectors, np.s_[0:original_len - new_len], axis = 1)
    return np.diag(kept_values[::-1]), np.fliplr(new_vector)

def project_image(img, U):
    # project each image into an m-dimensional space and return the new representation as a one-dimensional NumPy array with d elements
    a = np.dot(np.transpose(U), img)
    return np.dot(U, a)

def display_image(orig, proj):
    # use matplotlib to display a visual representation of the original image and the projected image side-by-side
    figure, axes = plt.subplots(nrows = 1, ncols = 2)
    axes[0].set_title("Original")
    axes[1].set_title("Projection")
    p1 = axes[0].imshow(np.transpose(np.reshape(orig, (32, 32))), aspect = 'equal')
    p2 = axes[1].imshow(np.transpose(np.reshape(proj, (32, 32))), aspect = 'equal')
    figure.colorbar(p1, ax = axes[0])
    figure.colorbar(p2, ax = axes[1])
    plt.show()
    return None
