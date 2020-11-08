from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score,accuracy_score


class Model_Finder:
    "This class is used to find the model with the best accuracy and auc score"

    def __init__(self,file_object, logger_object):
        self.file_object=file_object
        self.logger_object=logger_object
        self.clf= RandomForestClassifier()
        self.xgb=XGBClassifier(objective="binary:logisitc")


    def get_best_param_for_random_forest(self, train_x,train_y):
        self.logger_object.log(self.file_object,"Entered the get_best_param_for_random_forest Method of Model_Finder class")

        try:
            #initializing different combinatioins of parameters
            self.param_grid= {'n_estimators':[10,50,100,130],"criterion":['gini','entropy'],
                                "max_depth": range(2,4,1),"max_features": ['auto', 'log2']}

            #creating an object of the Grid Search Class
            self.grid= GridSearchCV(estimator=self.clf,param_grid=self.param_grid, cv=5, verbose=3)

            #finding best parameters
            self.grid.fit(train_x,train_y)

            #extracting the best parameters
            self.criterion= self.grid.best_params_['criterion']
            self.n_estimators= self.grid.best_params_['n_estimators']
            self.max_depth = self.grid.best_params_['max_depth']
            self.max_features = self.grid.best_params_['max_features']

            # creating a new model with best parameters

            self.clf= RandomForestClassifier(n_estimators=self.n_estimators, criterion=self.criterion,
                                                max_depth= self.depth, max_features= self.max_features)

            #treating the new model

            self.fit(train_x,train_y)

            self.logger_object.log(self.file_object,
                                            "Random Forest best params:" + str(self.grid.best_params_) + ".Exited the get_best_params_for_random_forest method of the Model Finder class")

            return self.clf

        except Exception as e :
            self.logger_object.log(self.file_object ,"Exception occured in get_best_params_for_random_forest_method of Model Finder Class. Exception message: "+str(e))

            self.logger_objdect.log(self.file_object, "Random Forest Parameter tuning failed . Exited the get_best_params_for_random_forest_method of the Model Finder class")

            raise Exception

        def get_best_params_for_xgboost(self, train_x, train_y):
            self.logger_object.log(self.file_object, "Entered the get_best_params_for_xgboost method of Model finder Class")

            #initializing with different parameters

            try:
                self.param_grid={
                    'learning_rate': [0.5, 0.1, 0.01, 0.001],
                    'max_depth': [3,5,10,10],
                    'n_estimators':[10,50,100,150]
                }

                #creating an object of the Grid Search class

                self.grid= GridSearchCV(estimator=self.xgb,param_grid=self.param_grid,versobose=3 , cv=5)

            # finding best parameters
                self.grid.fit(train_x, train_y)

            #extracting best parameters

                self.learning_rate= self.gird.best_params_['learning_rate']
                self.max_depth= self.gird.best_params_['max_depth']
                self.n_estimators= self.grid.best_params_['n_estimators']

            #creating a new model with best parameters

                self.xgboost= XGBClassifier(objective='binary:logistic',learning_rate= self.learning_rate,max_depth=self.max_depth, n_estimators= self.n_estimators)

            #treating the new model

                self.xgboost.fit(train_x, train_y)


                self.logger_object(self.file_object, 'XGBoost  best params :' + str(self.grid.best_params_) + ". Exited the get_best_params_for_xgboost method of Model Finder Class")

                return self.xgb

            except Exception as e:
                self.logger_object.log(self.file_object,
                                       "Exception occured in get_best_params_for_xgb method  of Model Finder Class. Exception message" + str(e))

                self.logger_object.log(self.file_object,
                                       "XGBoost tuning failed . Exited the get_best_params_for_xgb method of Model finder class")
                raise Exception

            def get_best_model(self, train_x,train_y ,test_x, test_y):
                """Method to find the model which has best AUC score"""

                self.logger_object.log(self.file_object,"Entered the get_best_model of Model Finder Class")

                #create the best model for xgboost

                try:
                    self.xgboost=self.get_best_params_for_xgboost(train_x , train_y)

                    self.prediction_xgboost= self.xgboost.predict(test_x) # Prediction using Xgboost Model

                    if len(test_y.unique())==1 : # if there is only one label in y, then roc_auc_score returns error. We will use accuracy i that case.
                        self.xgboost_score= accuracy_score(test_y , self.prediction_xgboost)
                        self.logger_object.log(self.file_object,"Accuracy for XGboost : " + str(self.xgboost_score)) #Log Accuracy
                    else:
                        self.xgboost_score= roc_auc_score(test_y , self.prediction_xgboost) # AUC for XGboost
                        self.logger_object.log(self.file_object, "AUC score for XGBoost : " + str(self.xgboost_score)) # Log AUC


                    # create the best model for Random Forest

                    self.random_forest = self.get_best_params_for_random_forest(train_x, train_y)

                    self.prediction_random_forest = self.random_forest.predict(test_x)

                    if len(test_y.unique()) == 1:
                        self.random_forest_score= accuracy_score(test_y , self.prediction_random_forest)
                        self.logger_object.log(self.file_object,"Accuracy for Random forest : " + str(self.random_forest_score))

                    else:
                        self.random_forest_score= roc_auc_score( test_y , self.prediction_random_forest) # AUC for Random forest
                        self.logger_object.log(self.file_object, "AUC score for Random Forest : " + str(self.random_forest_score))


                    #comparing two models

                    if self.random_forest_score < self.xgboost_score:
                        return  "XGBoost",self.xgboost
                    else:
                        return "Random Forest", self.random_forest


                except Exception as e:
                    self.logger_object.log(self.file_object,
                                           "Exception occured in get_best_model method of Model Finder Class. Exception message : " + str(e))

                    self.logger_object.log(self.file_object,
                                           "Model Selection Failed . Exited the get_best_model  method of Model Finder Class.")

                    raise Exception













