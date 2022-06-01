from KeypointCluster import KeypointCluster

def DBSCAN_Cluster(image, eps, min_samples):

    detect=KeypointCluster(image)
    key_points, descriptors = detect.siftDetector()
    cluster_list = detect.DBSCANLocateForgery(eps, min_samples)

    return  cluster_list

def KMeans_Cluster(image, n_clusters):

    detect=KeypointCluster(image)
    key_points, descriptors = detect.siftDetector()
    cluster_list = detect.KMeansLocateForgery(n_clusters)

    return  cluster_list