import numpy as np


def calc_VIF(X):
    '''
    # This function calculates the Variance Inflation Factor (VIF) for a given design matrix
    :param X: a design matrix (num_samples X num_features)
    :return: VIF: a vector of size num_features
    '''
    import numpy as np
    from sklearn import datasets, linear_model

    num_samples, num_features = X.shape
    VIF = np.empty(num_features)
    for j in range(num_features):
        IX = np.asarray(range(num_features)) != j
        X_j = X[:, IX]
        y_j = X[:, j]

        regr = linear_model.LinearRegression(fit_intercept=True)
        regr.fit(X_j, y_j)
        R_2_j = regr.score(X_j, y_j)
        VIF[j] = 1. / (1. - R_2_j)

    return VIF


def get_VIF_values(design_matrix, thresh = 3):
    '''

    :param design_matrix: num_samples X num_features numpy array
    :param thresh: scalar indicating the thresh for VIF
    :return:
    '''
    import time
    from statsmodels.stats.outliers_influence import variance_inflation_factor as vif
    from statsmodels.tools.tools import add_constant
    from tqdm import tqdm

    print('Means and SD')
    ave_features = np.mean(design_matrix, axis = 0) # Make sure the features are centralized
    std_features = np.std(design_matrix, axis = 0) # Make sure the features are standardized

    #print('Pairwise Correlations')
    #corr = np.corrcoef(design_matrix.T)

    print('Variance inflation factors')
    design_matrix = add_constant(design_matrix)
    VIF_values = [vif(design_matrix, i) for i in range(design_matrix.shape[1])]
    IX_filter = np.asarray([i > thresh for i in VIF_values])

    return VIF_values, IX_filter, ave_features, std_features


def get_weight_outliers(weights, thresh = 3):
    '''

    :param weights: num_weights X 1 numpy array
    :param thresh: scalar indicating the number of standard deviations as a threshold for outlier detection
    :return:IX - list of boolean values whether the unit is outlier or not (without sorting)
    '''
    import math
    import numpy as np
    ave = np.mean(weights, axis=0)
    std = np.std(weights, axis=0)

    IX_pos = weights > ave + thresh * std
    IX_neg = weights < ave - thresh * std
    IX = [x or y for x, y in zip(IX_pos, IX_neg)]

    k = sum(IX)
    if k == 0:
        print('No outliers were identified - change thresh')
        n = 0
    else:
        # Find n such the n over k ~= 1000
        n = k
        n_over_k = 0
        while n_over_k < 1000:
            n += 1
            n_over_k = math.factorial(n)/(math.factorial(k)*math.factorial(n - k))

        # Check if previous n was closer to 10^3
        previous_n_over_k = math.factorial(n-1)/(math.factorial(k)*math.factorial(n-k-1))
        if np.abs(previous_n_over_k-1000)<np.abs(n_over_k-1000):
            n = n-1


    return k, n, ave, std, IX


def generate_text_file_with_sorted_weights(weights, output_path):
    '''

    :param weights: num_splits X num_units ndarray - regression weights
    :param output_path: folder+file_name string - where to save
    :return: None
    '''
    import os
    print('Writing sorted weights to file: %s'%output_path)
    best_weights_array = np.vstack((np.mean(weights, axis=0), np.std(weights, axis=0), range(weights.shape[1])))
    IX = np.argsort(best_weights_array[0, :])[::-1]
    best_weights_sorted = np.transpose(best_weights_array)[IX]
    np.savetxt(os.path.join(output_path), best_weights_sorted, fmt='%1.2f +- %1.2f, %i')