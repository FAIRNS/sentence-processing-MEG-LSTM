def get_VIF_values(design_matrix, thresh = 3):
    import numpy as np
    from statsmodels.stats.outliers_influence import variance_inflation_factor as vif

    print('Means and SD')
    ave_features = np.mean(design_matrix, axis = 0) # Make sure the features are centralized
    std_features = np.std(design_matrix, axis = 0) # Make sure the features are standardized

    print('Pairwise Correlations')
    corr = np.corrcoef(design_matrix)

    print('Variance inflation factors')
    VIF_values = [vif(design_matrix, i) for i in range(m.shape[1])]
    IX_filter = VIF_values > thresh

    return VIF_values, IX_filter, ave_features, std_features


def get_weight_outliers(weights):
    import numpy as np
    ave = np.mean(weights, axis=0)
    std = np.std(weights, axis=0)

    IX_pos = weights > ave + 3 * std
    IX_neg = weights < ave - 3 * std
    IX = IX_pos or IX_neg

    k = IX.sum()
    

    return k, n, ave, std