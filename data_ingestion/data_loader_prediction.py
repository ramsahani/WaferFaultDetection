import pandas as pd

class Data_Getter_Pred:
    """ This class shall be use for obtaining the data from the source for  prediction ."""

    def __init__(self, file_object, logger_bject):
        self.prediction_file = "Prediction_FileFromDB/InputFile.csv"
        self.file_object= file_object
        self.logger_object = logger_bject

    def get_data(self):

        self.logger_object.log(self.file_object,
                               "Entered in get_data method of Data_Getter_Pred class")
        try:
            self.data= pd.read_csv(self.prediction_file)
            self.logger_object.log(self.file_object,
                                   "Data Load Successful. Exited the get_data method of Data_Getter_Pred class")
            return self.data
        except Exception as e:
            self.logger_object(self.file_object,
                               "Exception occurred in get_data method of Data_Getter_Pred class. Exception message : "+str(e))
            self.logger_object(self.file_object,
                               "Data Load Unsuccessful. Exited the get_data method of Data_Getter_Pred class")
            raise Exception()