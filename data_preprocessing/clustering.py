import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from kneed import KneeLocator
from file_operations import file_methods

class KMeanClustering:
    """ This class shall be used to divide the data into the different cluster before teh training."""

    def __init__(self, file_object ,logger_object):
        self.file_object = file_object
        self.logger_object = logger_object


    def elbow_plot(self , data):

        """
            Method Name : elbow_plot
            Description : This method saves the plot to decide the optimum number of the clusters to the file.
            Output: A picture saved to the directory
            On Failure : Raise Exception

        """
        self.logger_object.log(self.file_object,
                               "Entered in elbow_plot method of KMeanClusterin Class")
        wcss=[] # initializing an empytlist

        try:
            for i in range(1,11):
                kmeans = KMeans(n_clusters=i, init='kmeans++',ranodm_state=42) #initializing the KMeans Object
                kmeans.fit(data) # fitting the data into KMean Algorithm
                wcss.append(kmeans.inertia_)
            plt.plot(range(1,11),wcss)
            plt.title("The Elbow Method")
            plt.xlabel("Number of clusters")
            plt.ylabel("WCSS")
            plt.savefig("preprocessing_data/k_means_elbow.png") #saving the elbow locally

                #finding the value of omptimum clusters

            self.kn = KneeLocator(range(1,11),wcss, curve='convex', direction= "decreasing")
            self.logger_object.log(self.file_object,
                                       'The optimum number of the cluster is '+ str(self.kn) +" .Exited the elbow_plot method of KMeansClustering class")
            return self.kn.knee

        except Exception as e:
            self.logger_object.log(self.file_object,"Exception occured in elbow_method in KMeansClustering class . Exception message : " + str(e))
            self.logger_object.log(self.file_object,"Fiding Number of clusters failed . Exited the elbow_method in KMeansClustering Class")
            raise Exception

    def create_clusters(self, data, number_of_cluster):
        """
                            Method Name: create_clusters
                            Description: create a new dataframe consisting of the cluster information.
                            output: A dataframe with cluster clumn
                            On failure: Raise Exception

        """

        self.logger_object.lof(self.file_object,"Entered in create_cluster method of KMeansClustering class")
        self.data=data

        try:
            self.kmeans= KMeanClustering(n_clusters=number_of_cluster, init="k-means+++",random_state=42)
            self.y_kmeans=self.kmeans.predict(data) # divide data into clusters

            self.file_op=file_methods.File_Operation(self.file_object, self.logger_object)
            self.save_model = self.file_op.save_model(self.kmeans, "KMeans") # saving the model to directory

            self.data['Cluster'] = self.y_kmeans # create a new column in dataset for storing the cluster information
            self.logger_object.log(self.file_object,
                                   " successfully created " + str(self.kn.knee) +'clusters. Exited the create_cluster method of the KMeansClustering class')
            return self.data

        except Exception as e:
            self.logger_object.log(self.file_object,
                                   "Exception occured in create_clusters method of KMeansClustering class. Exception message: " + str(e))
            self.logger_object.log(self.file_object,
                                   "Fitting the data to clusters_finding method failed . Exited the create_cluster method of KMeansClustering class")





