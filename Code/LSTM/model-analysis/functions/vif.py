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
