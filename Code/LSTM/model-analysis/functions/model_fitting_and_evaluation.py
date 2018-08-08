import time
import numpy as np
import scipy.stats as stats
from sklearn import linear_model
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline


def train_model(X_train, y_train, settings, params):
    # Train a regression model according to chosen method
    if settings.method == 'Ridge':
        model = train_model_ridge(X_train, y_train, settings, params)
    elif settings.method == 'Lasso':
        model = train_model_lasso(X_train, y_train, settings, params)
    elif settings.method == 'Elastic_net':
        model = train_model_elastic_net(X_train, y_train, settings, params)

    return model


def train_model_ridge(X_train, y_train, settings, params):

    # Grid search - calculate train/validation error for all regularization sizes

    tuned_parameters = [{'alpha': params.alphas}]
    model_ridge = GridSearchCV(linear_model.Ridge(), tuned_parameters, cv=params.CV_fold, refit=True, return_train_score=True)
    model_ridge.fit(X_train, y_train)
    model_ridge.alphas = params.alphas

    return model_ridge


def train_model_lasso(X_train, y_train, settings, params):
    # Compute path
    print("Computing regularization path using the lasso...")
    alphas, coefs_lasso, _ = linear_model.lasso_path(X_train, y_train, eps=params.eps, fit_intercept=True)

    # Grid search - calculate train/validation error for all regularization sizes
    lasso = linear_model.Lasso()
    tuned_parameters = [{'alpha': alphas}]
    model_lasso = GridSearchCV(lasso, tuned_parameters, cv=params.CV_fold,
                                               return_train_score=True, refit=True)
    model_lasso.fit(X_train, y_train)

    model_lasso.alphas = alphas
    model_lasso.coefs = np.transpose(coefs_lasso)
    return model_lasso


def train_model_elastic_net(X_train, y_train, settings, params):
    # Compute path
    print("Computing regularization path using the elastic net...")
    alphas, coefs_enet, _ = linear_model.enet_path(X_train, y_train,
                                                   eps=params.eps, l1_ratio=params.l1_ratio, fit_intercept=True)

    # Grid search - calculate train/validation error for all regularization sizes
    enet = linear_model.ElasticNet()
    tuned_parameters = [{'alpha': alphas}]
    model_enet = GridSearchCV(enet, tuned_parameters, cv=params.CV_fold,
                                              return_train_score=True, refit=True)
    model_enet.fit(X_train, y_train)

    model_enet.alphas = alphas
    model_enet.coefs = np.transpose(coefs_enet)

    return model_enet


def evaluate_model(model, X_test, y_test, settings, params):
    # ## Evaluate the regression models

    if settings.method == 'Ridge':
        scores, MSE_per_depth = eval_model_ridge(model, X_test, y_test, settings, params)
    elif settings.method == 'Lasso':
        scores = eval_model_lasso(model, X_test, y_test, settings, params)
        MSE_per_depth = []
    elif settings.method == 'Elastic_net':
        scores = eval_model_elastic_net(model, X_test, y_test, settings, params)
        MSE_per_depth = []

    return scores, MSE_per_depth


def eval_model_ridge(model, X_test, y_test, settings, params):
    scores = model.score(X_test, y_test)
    MSE_per_depth = []
    if settings.calc_MSE_per_each_depth:
        for depth in set(y_test):
            X_test_curr_depth = X_test[y_test == depth, :]
            y_test_curr_depth = y_test[y_test == depth]
            y_predicted_curr_depth = model.predict(X_test_curr_depth)
            scores_curr_depth = ((y_test_curr_depth - y_predicted_curr_depth)**2).sum()/y_test_curr_depth.shape[0]
            MSE_per_depth.append([depth, scores_curr_depth])
    return scores, MSE_per_depth


def eval_model_lasso(model, X_test, y_test, settings, params):
    scores = model.score(X_test, y_test)

    return scores


def eval_model_elastic_net(model_elastic_net, X_test, y_test, settings, param):
    scores_enet = model_elastic_net.score(X_test, y_test)
    # scores.append(model_ridge.score(X_test, y_test))

    return scores_enet


# t1 = time.time()
# model_lasso = linear_model.LassoCV(cv=5, eps=params.eps).fit(X_train, y_train)
# t_lasso_cv = time.time() - t1
# # Display results
# m_log_alphas = -np.log10(params.alphas)
