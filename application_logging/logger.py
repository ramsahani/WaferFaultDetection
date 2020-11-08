from datetime import datetime

class App_Logger:
    def __init__(self):
        pass

    def log(self,file_object, log_message):
        self.now=datetime.now()
        self.data=datetime.date()
        self.current_time=self.now.strftime("%H:%M:%S")
        file_object.write(
            str(self.data) + "/" + str(self.curret_time)+ "\t\t" +log_message +"\n"
        )
