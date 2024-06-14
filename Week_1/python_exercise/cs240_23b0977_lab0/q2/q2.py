import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def PCA(init_array: pd.DataFrame):

    sorted_eigenvalues = None
    final_data = None
    dimensions = 2
    #print(init_array)

    # TODO: transform init_array to final_data using pca_data

    # Step 1: Standardize the data
    mean = np.mean(init_array, axis = 0)
    std_dev = np.std(init_array, axis = 0)
    standardized_data = (init_array - mean) / std_dev

    # Step 2: Calculate the covariance matrix
    covariance_matrix = np.cov(standardized_data, rowvar = False)

    # Step 3: Calculate the eigenvalues and eigenvectors of the covariance matrix
    eigenvalues, eigenvectors = np.linalg.eig(covariance_matrix)

    # Step 4: Sort the eigenvalues in decreasing order
    idx = eigenvalues.argsort()[::-1]
    sorted_eigenvalues = np.round(eigenvalues[idx],4)
    eigenvectors = eigenvectors[:,idx]

    # Step 5: Choose the top K=2 eigenvectors
    top_eigenvectors = eigenvectors[:, :dimensions]

    # Step 6: Transform the original data using the top K eigenvectors
    final_data = np.dot(standardized_data, top_eigenvectors)

    # END TODO

    return sorted_eigenvalues, final_data


if __name__ == '__main__':
    init_array = pd.read_csv("pca_data.csv", header = None)
    sorted_eigenvalues, final_data = PCA(init_array)
    np.savetxt("transform.csv", final_data, delimiter = ',')
    for eig in sorted_eigenvalues:
        print(eig)

    # TODO: plot and save a scatter plot of final_data to out.png
    plt.figure()
    plt.scatter(final_data[:,0], final_data[:,1])
    # set the aspect of the plot to be equal
    plt.gca().set_aspect('equal', adjustable='box')
    # set limits for x and y axes
    plt.xlim(-15, 15)
    plt.ylim(-15, 15)
    # save the scatter plot
    plt.savefig("out.png")
    plt.close()
    # END TODO
