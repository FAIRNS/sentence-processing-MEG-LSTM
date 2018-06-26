def get_VIF_values(design_matrix, thresh = 3):
    '''

    :param design_matrix: num_samples X num_features numpy array
    :param thresh: scalar indicating the thresh for VIF
    :return:
    '''
    import numpy as np
    from statsmodels.stats.outliers_influence import variance_inflation_factor as vif
    from tqdm import tqdm

    print('Means and SD')
    ave_features = np.mean(design_matrix, axis = 0) # Make sure the features are centralized
    std_features = np.std(design_matrix, axis = 0) # Make sure the features are standardized

    #print('Pairwise Correlations')
    #corr = np.corrcoef(design_matrix.T)

    print('Variance inflation factors')
    VIF_values = [vif(design_matrix, i) for i in tqdm(range(design_matrix.shape[1]))]
    IX_filter = VIF_values > thresh

    return VIF_values, IX_filter, ave_features, std_features


def get_weight_outliers(weights, thresh = 3):
    '''
    
    :param weights: num_weights X 1 numpy array
    :param thresh: scalar indicating the number of standard deviations as a threshold for outlier detection
    :return:
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

    return k, n, ave, std