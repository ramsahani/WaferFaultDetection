import _sqlite3
from datetime import datetime
from os import listdir
import os
import re
import json
import shutil
import pandas as pd
from application_logging.logger import App_Logger


class Prediction_Data_validation:


    """
            This class shall be used for handling all the validation done on the Raw Prediction Data!!.

    """
    def __init__(self,path):
        self.Batch_Directory = path
        self.schema_path= 'schema_prediction.json'
        self.logger= App_Logger()

    def valuesFromSchema(self):
        """
                                        Method Name: valuesFromSchema
                                        Description: This method extracts all the relevant information from the pre-defined "Schema" file.
                                        Output: LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, Number of Columns
                                        On Failure: Raise ValueError,KeyError,Exception

                                       """
        try:
            with open(self.schema_path,'r') as f:
                dic = json.load(f)
                f.close()
            pattern = dic['SampleFileName']
            LengthOfDateStampInFile = dic['LenghtOfDateStampInFile']
            LengthOfTimeStampInFile  = dic['LengthOfTimeStampInFile']
            column_names = dic['ColName']
            NumberofColumns = dic['NumberofColumns']

            file= open("Training_Logs/valuesfromSchemaValidationLog.txt",'a+')

            message = "LengthOfDateStampInFile:: %s" %LengthOfDateStampInFile + "\t" + 'LengthOfTimeStampInFile:: %s' % LengthOfTimeStampInFile + "\t" + "NumberofCoulmns:: %s" % NumberofColumns + '\n'

            self.logger.log(file,message)

            file.close()

        except ValueError:
            file=open("Prediciton_Logs/valuesfromSchemaValidationLoge.txt",'a+')
            self.logger.log(file,'Value Error: Value not found inside schema_trainings.json')
            file.close()
            raise Exception()

        except KeyError:
            file = open("Prediction_Logs/valuesfromSchemaValidationLog.txt",'a+')
            self.logger.log(file, "KeyError: Key value error incorrect key passed")

            file.close()
            raise KeyError
        except Exception as e:
            file=open("Prediction_Logs/valuesfromSchemvValidationLog.txt",'a+')
            self.logger.log(file,str(e))
            file.close()
            raise e
        return LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, NumberofColumns

    def manualRegexCreation(self):
        """
                Method Name : manualRegexCreation
                Description : This method contains a manual defined regex based on the "FileName" given in "Schema" file.
                                This Regex is used to validate the filename of the prediction data.
                Output : Regex pattern
                On Failure : None

        """


        regex = "['wafer']+['\_'']+[\d_]+[\d]+\.csv"

        return regex

    def createDirectoryForGoodBadRawData(self):
        """
        Method Name: creatDirectoryForGoodBadRawData
        Description : This method creates directories to store the Good Data and Bad Data
                        after validating the prediction data.

        :return: None
        """

        try:
            path = os.path.join("Prediction_Raw_Files_Validated/","Good_Raw/")
            if not os.path.isdir(path):
                os.makedires(path)
            path = os.path.join("Prediction_Raw_Files_Validated/","Bad_Raw/")
            if not os.path.idir(path):
                os.makedires(path)

        except OSError as ex:
            file = open("Prediction_Logs/GeneralLog.txt",'a+')
            self.logger.log(file,"Error while creating Directory %s:" % ex)
            file.close()
            raise OSError


    def deleteExistingGoodDataTrainingFolder(self):

        """
        This method deletes the directory made to store the Good data after loading the data in th table.
        Once the good files are loaded in the DB, deleting the directory ensures space optimization.

        :return: None
        """

        try :
            path = "Prediction_Raw_Files_Validated/"

            if os.path.isdir(path + "Good_Raw/"):
                shutil.rmtree(path + "Good_Raw/")
                file = open("Prediction_Logs/GeneralLog.txt",'a+')
                self.logger.log(file,"GoodRaw directory deleted successfully!!!")
                file.close()
        except OSError as s:
            file= open("Prediction_Logs/GeneralLog.txt",'a+')
            self.logger.log(file,"Error while  Deleting Directory : %s" %s)
            file.clos()
            raise OSError

    def deleteExistingBadataTrainingFolder(self):
        """
            This method deletes the directory made to store the bad Data.
        :return:None
        """

        try:
            path = "Prediction_Raw_Files_Validated/"
            if os.path.isdir(path + 'Bad_Raw/'):
                shutil.rmtree(path + 'Bad_Raw/')
                file = open('Prediction_Logs/GeneralLog.txt','a+')
                self.logger.log(file,'Bad directory deleted before starting validation !!!')
                file.close()

        except OSError as s:
            file = open("Prediction_Logs/GeneralLog.txt",'a+')
            self.logger.log(file,"Error while Deleting Directory : %s"%s)
            file.close()
            raise OSError

    def moveBadFilesToArchiveBad(self):
        """
        This method deletes the directory made to store the Bad Data
        after moving the data in archive folder. We archive the bad
        files to send them back to the client for invalid data issue.
        :return: None
        """
        now = datetime.now()
        data = now.data()
        time = now.strftime("%H%M%S")
        try:
            path = "PredictionArchivedBadData"
            if not os.path.isdir(path):
                os.makedirs(path)
            source = 'Prediction_Raw_Files_Validated/Bad_Raw/'
            dest = "PredictionArchivedBadData/BadData_" + str(data) + '_' + str(time)

            if not os.path.isdir(dest):
                os.makedirs(dest)
            files = os.listdir(source)
            for f in files:
                if f not in os.listdir(dest):
                    shutil.move(source + f,dest)
            file = open("Prediction_Logs/GeneralLog.txt",'a+')
            self.logger.log(file,"Bad files moved to archive")
            path='Prediction_Raw_Files_Validated/'
            if os.path.isdir(path + "Bad_Raw/"):
                shutil.rmtree(path+'Bad_Raw/')
            self.logger.log(file,'Bad Raw data folder deleted successfully!!!')
            file.close()

        except OSError as e:
            file = open("Prediction_Logs/GeneralLog.txt",'a+')
            self.logger.log(file,"Error while moving bad files to archive :: %s" % e)
            file.cloes()
            raise OSError


    def validationFileNameRaw(self,regex,LengthOfDateStampInFile,LengthOfTimeStampInFile):
        """
        This function validates th name of the prediction csv as per given name in the schema!
        Regex patter is used to do validation.If name format do not match the file is moved
        to Bad Raw Data folder else in Good raw data.
        :param regex:
        :param LengthOfDateStampInFile:
        :param LengthOfTimeStampInFile:
        :return:
        """
    # delete the directories for good and bad in case last run was unsuccessful and folders were not deleted.
        self.deleteExistingBadDataTrainingFolder()
        self.deleteExistingGoodDataTrainingFolder()
        self.createDirectoryForGoodBadRawData()
        onlyfiles= [f for f in listdir(self.Batch_Directory)]
        try:
            f= open("Prediction_Logs/nameValidationLog.txt",'a+')
            for filename in onlyfiles:
                if (re.match(regex, filename)):
                    splitAtDot = re.split('.csv',filename)
                    splitAtDot = (re.split('_',splitAtDot[0]))
                    if len(splitAtDot[1]) == LengthOfDateStampInFile:
                        if len(splitAtDot[2]) == LengthOfTimeStampInFile:
                            shutil.copy("Prediction_Batch_files/" + filename,"Prediction_Raw_Files_Validated/Good_Raw")
                            self.logger.log(f,"Valid File name!! File moved to GoodRaw Folder :: %s" % filename)

                        else:
                            shutil.copy("Prediction_Batch_files/"+ filename,"Prediction_Raw_Files_Validated/Bad_Raw")
                            self.logger.log(f,"Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)
                    else:
                        shutil.copy("Prediction_BatchFiles/" + filename, "Prediction_Raw_Files_Validated/Bad_Raw")
                        self.logger.log(f, "Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)

                else:
                    shutil.copy("Prediction_Batch_files/"+ filename, "Prediction_Raw_Files_Validated/Bad_Raw")
                    self.logger.log(f,"Invalid Column length for the file!! File moved to Bad Raw Folder :: %s"  % filename)

            f.close()
        except Exception as e:
            f= open("Prediction_Logs/namValidationLog.txt",'a+')
            self.logger.log(f,"Error occurred while validating FileName %s" % e)
            f.close()
            raise e

    def validateColumnLength(self,NumberofColumns):


        """
            This function validates the number of columns in csv files.
            It  should be same as given the schema file.
            If not same file is not suitable for processing and thus is moved to Bad_Raw Data folder.
            If the column number matches ,file is kept in Good Raw Data for processing.
            The csv file is missing the first column name , this function changes the missing name to "Wafer".
            :param self:
            :param NumberofColumns:
            :return: None
            """
        try:
            f = open("Prediction_Logs/columnValidation.txt",'a+')
            self.logger.log(f,"Coulumn Length Validation Started !!!")
            for file in listdir('Prediction_Raw_Files_Validated/Good_Raw/'):
                csv = pd.read_csv("Prediction_Raw_Files_Validated/Good_Raw/" + file)
                if csv.shape[1] == NumberofColumns:
                    csv.rename(columns={"Unnamed: 0":"Wafer"},inplace=True)
                    csv.to_csv("Prediction_Raw_Files_Validated/Good_Raw/" + file,index=None,header=True)
                else:
                    shutil.move("Prediction_Raw_Files/Validated/Good_Raw/"+file  ,"Prediction_Raw_Files_Validated/Bad_Raw")
                    self.logger.log(f,"Invalid Column Length for the file !! moved to Bad Raw Data folder :: %s" %  file)

            self.logger(f,"Column Length Validation Completed !!")

        except OSError:
            f=open("Prediction_Logs/columnValidationLog.txt",'a+')
            self.logger.log(f,'Error Occurred while validating column :: %s' % OSError)
            f.close()
            raise OSError
        except Exception as e:
            f= open("Prediction_Logs/columnValidationLog.txt",'a+')
            self.logger.log(f,"Error Occurred :: %s " % e)
            f.close()
            raise e
        f.close()

    def deletePredictionFile(self):

        if os.path.exists("Prodiction_Output_File/Predictions.csv"):
            os.remove('Prediction_Output_File/Prediction.csv')

    def validateMissingValuesInWholeColumn(self):
        """
        This function validates if any column in the csv file has all values missing.
        If all the values are missing , the file is not suitable for processing.
        Such files are moved to  bad raw data.
        :return: None
        """

        try:
            f = open("Prediction_Logs/missingValuesInColumn.txt",'a+')
            self.logger.log(f,"Missing Values Validation Started !!")

            for file in listdir("Prediction_Raw_Files_Validated/Good_Raw/"):
                csv = pd.read_csv("Prediction_Raw_Files_Validated/Good_Raw/" + file)
                count = 0
                for columns in csv:
                    if (len(csv[columns])- csv[columns].count()) == len(csv[columns]):
                        count += 1
                        shutil.move("Prediction_Raw_Files_Validated/Good_Raw/" + file ,"Prediction_Raw_Files_Validated/Bad_Raw")

                        self.logger.log(f,"Invalid Column Length for the file!! moved to Bad Raw Folder:: %s " % file)
                        break
                    if count ==0:
                        csv.rename(columns = {'Unnamed:0':'Wafer'},inplace = True)
                        csv.to_csv("Prediction_Raw_Files_Validated/Good_Raw/"+ file, index= None)

        except OSError:
            f= open("Prediction_Logs/missingValuesInColumn.txt",'a+')
            self.logger.log(f,'Error Occurred while moving the file :: % s ' % OSError)
            f.close()
            raise OSError
        except Exception as e:
            f = open("Prediction_Logs/missingValuesInColumn.txt",'a+')
            self.logger.log(f,"Error Occurred :: %s" % e)
            f.close()
            raise e
        f.close()



