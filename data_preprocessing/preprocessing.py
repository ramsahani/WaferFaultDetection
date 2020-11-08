import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer

class Preprocessor:
    """
        This class shall be used to clean and transform the data before training.

    """
    def __init__(self,file_object,logger_object):
        self.file_object = file_object
        self.lgger_object = logger_object

    def remove_columns(self,data,columns):
        """
        This method removes the given columns from a  pandas daaframe.
        :param columns,data
        :return: A pandas DataFrame after removing the specified columns.
        """
        self.logger_object.log(self.file_object,'Entered the remove_columns method of the Preprocessor class')
        self.data = data
        self.columns = columns
        try :
            self.useful_data = self.data.drop(labels=self.columns, axis=1) # drop the labels specified in the columns
            self.logger_object.log(self.file_object,'Column removal Successful. Exited the remove_columns method of the Preprocessor class')
            return self.useful_data

        except Exception as e:
            self.logger_object.log(self.file_object,"Exception occurred in remove_columns method of the processor class. Exception message : " +str(e))
            self.logger_object.log(self.file_object,"Column removal Unsuccessful. Exited the remove_columns method of the Preprocessor class")
            raise Exception()

    def separate_label_feature(self, data, label_column_name):
        """
        This method separate the features and a Label Columns.
        :param data:
        :param label_column_name:
        :return: two dataframes one containing the features and other containing the labels.
        """

        self.logger_object.log(self.file_object , 'Entered the separate_label_feature method of the Preprocessor class')
        try:
            self.X = data.drop(labels= label_column_name, axis= 1) #drop the column specified and separate the feature columns
            self.Y = data[label_column_name] # Filter the Label columns

            self.logger_object.log(self.file_object,'Label Separation Successfu. Exited the separate_label_feature method of the Preprocessor class' )

            return self.X,self.Y
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occurred in separate_label_feature method of the Preprocessor class.Exception message: ' + str(e))
            self.logger_object.log(self.file_object,'Label Separation Unsuccessful.Exited the separate_label_feature method of the Preprocessor class')
            raise Exception()

    def is_null_present(self,data):
        """
         This method checks whether there are null values present in the pandas DataFrame or not.
         :param data:
         :return: returns a bolean values . True if null present  else False.
        """

        self.logger_object.log(self.file_object,'Entered the is_null_present method of the Preprocessor class.')
        self.null_present = False
        try:
            self.null_counts= data.isna().sum() # check for the count of the null values per column
            for i in self.null_counts:
                if  i >0:

                    self.null_present = True
                    break
                if (self.null_present): # write the logs to see which columns have null values
                    dataframe_with_null = pd.DataFrame()
                    dataframe_with_null['columns'] = data.columns
                    dataframe_with_null['missing values count']= np.asarray(data.isna().sum())
                    dataframe_with_null.to_csv('preprocessing_data/null_values.csv')
                self.lgger_object.log(self.file_object,'Finding missing values is a success.Data written to the null values file. Exited the is_null_present_method of the Preprocessor class')
                return self.null_present
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occurred in is_null_present method of Preprocessor class . Exception message : ' +str(e))
            self.logger_object.log(self.file_object,'Finding missing values failed. Exited the is_null_present method of the Prepocessor clas')
            raise Exception()

    def impute_missing_values(self,data):
        """
        This method replaces all the missing values in the Dataframe using KNN Imputer.

        :param data:
        :return: A dataframe which all the missing values imputed.
        """
        self.logger_object.log(self.file_object,'Entered the impute_missing_values method of the Preprocessor class')
        self.data =data
        try:
            imputer= KNNImputer(n_neighbors=3,weights='uniform',missing_values=np.nan)
            self.new_array = imputer.fit_transform(self.data) # impute the missing values

            # convert the nd-array returned in the step above to a Datframe
            self.new_data = pd.DataFrame(data= self.new_array,columns= self.data.columns)
            self.logger_object.log(self.file_object,'Impute missing values Successful. Exited the impute_missing_values_method of the Preprocessor class ')
            return self.now_data

        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occurred in impute_missing_values method of the Preprocessor class')
            self.logger_object.log(self.file_object,'Imputing missing_values failed. Exited the impute_missing_values method of the Preprocessor class')
            raise Exception()

    def get_columns_with_zero_std_deviation(self,data):
        """
        This method finds out the columns which have a standard deviation of zero.
        :param data:
        :return: List of the columns with standard deviation of zero
        """

        self.logger_object.log(self.file_object,'Enterd the get_columns_with_zero_std_deviation method of the Preprocessor class')
        self.columns = data.columns
        self.data_n = data.describe()
        self.col_to_drop=[]
        try:
            for x in self.columns:
                if (self.data_n[x]['std'] == 0): # check if standard deviation is zero
                    self.col_to_drop.append(x) # prepare the list of columns with standard deviation zero
            self.logger_object.log(self.file_object,'Column search for Standard_Deviation Zero Successful. Exited the get_columns_with_zero_std_deviation_method of the Preprocessor class')
            return self.col_to_drop
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in get_columns_with_zero_std_deviation method of the Preprocessor class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object, 'Column search for Standard Deviation of Zero Failed. Exited the get_columns_with_zero_std_deviation method of the Preprocessor class')
            raise Exception()