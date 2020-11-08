import pickle
import os
import shutil

class File_Operation:
    """
        This class be used to save the model after training
        and load the saved model for prediction.

    """
    def __init__(self, file_object, logger_object):
        self.file_object = file_object
        self.logger_object = logger_object
        self.model_directory="models/"

    def save_model(self, model , filename):

        self.logger_object.log(self.file_object,
                                   "Entered in save_model method of File_Operation cass")
        try:
            path=os.path.join(self.model_directory,filename) #create each separate directory for each clusters
            if os.path.isdir(path):# remove previous existing models for each clusters
                shutil.rmtree(self.model_directory)
                os.makedirs(path)
            else:
                os.makedirs(path)
            with open(path + "/" + filename + " .sav") as f:
                pickle.dump(model,f) # save the model to file

            self.logger_object.log(self.file_object, "Model File "+ filename+ " saved. Exited the save_model method of File_Operration Class")

            return 'success'
        except Exception as e:
            self.logger_object.log(self.file_object,
                                       "Exceptino occurres in save_model method of the File_Operation clas . Exception message :" + str(e))
            self.logger_object.log(self.file_object,
                                      'Model File ' + filename + ' could not be saved . Exited the save_model method of File_Operation class')
            raise Exception()

    def load_model(self,filename ):

        self.logger_object.log(self.file_object,"Entered in teh load_model method of File_Operation class")

        try:
            with open(self.model_directory + filename + '/' + filename + '.sav',
                      'rb') as f:
                self.logger_object.log(self.file_object , 'Model File' + filename + ' loaded. Exited the load_model method of File_Operation class')
                return pickle.load(f)
        except Exception as e:
            self.logger_object.log(self.file_object, 'Excception occured in load_model method of File_Operation class. Exception message : ' +str(e))
            self.logger_object.log(self.file_object, 'Model File '+ filename + ' could not loaded. Exited the load_model method of File_Operation class')

            raise Exception()

    def find_correct_model_file(self, cluster_number):

        self.logger_object.log(self.file_object , 'Entered the find_correct_model_file method of File_Operation class')

        try:
            self.cluster_numberr = cluster_number
            self.folder_name = self.model_directory
            self.list_of_model_files = []
            for self.file in self.file.list_of_files:
                try:
                    if (self.file.index(str(self.cluster_number)) != -1):
                        self.model_name = self.file
                except :
                    continue
            self.model_name = self.model_name.split('.')[0]
            self.logger_object.log(self.file_object,
                                   "Exception occured in find_correct_model of the  File_Operation. ")

            return self.model_name
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'EXception occured in find_correct_model_file method of File_Operation class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object,
                                   "Exited the find_correct_model_file method of File_Operation class.")
            raise Exception()




