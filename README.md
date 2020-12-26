# WaferFaultDetection
 The inputs of various sensors for different wafers have been provided. In electronics, a wafer (also called a slice or substrate)
 is a thin slice of semiconductor used for the fabrication of integrated circuits. The goal is to build a machine learning model which
 predicts whether a wafer needs to be replaced or not(i.e., whether it is working or not) based on the inputs from various sensors.
 
 <br>There are two classes: +1 and -1. 
*	+1 means that the wafer is in a working condition and it doesn’t need to be replaced.
*	-1 means that the wafer is faulty and it needs to be replaced. 

## Instructions to run

 *Prerequisite*
 >IDE : Pycharm 

After cloning the repository<br>
install the requirements.txt
~~~python
 pip install requirements.txt
~~~

open http://localhost:5000/train to start training the model

After successful training 

open http://localhost:5000/prediction
<br>In the prediction page either you can check default predictions or  enter the path of the prediction files for custom prediction
