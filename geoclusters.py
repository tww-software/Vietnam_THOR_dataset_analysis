"""
attempt K-means clustering on our GEO LAT LON mission data

Vietnam THOR dataset

Thomas W Whittam
"""


import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

import kml


def plot_elbow_curve(df):
    """
    plot an elbow curve to find the optimal number of clusters
    """
    K_clusters = range(1, 10)
    kmeans = [KMeans(n_clusters=i) for i in K_clusters]
    Y_axis = df[["TGTLATDD_DDD_WGS84"]]
    X_axis = df[["TGTLONDDD_DDD_WGS84"]]
    score = [kmeans[i].fit(Y_axis).score(Y_axis) for i in range(len(kmeans))]
    plt.plot(K_clusters, score)
    plt.xlabel('Number of Clusters')
    plt.ylabel('Score')
    plt.title('Elbow Curve')
    plt.savefig('elbow-curve.png')
    plt.clf()


def kmeans(df):
    """
    cluster the data points

    plot clusters on a chart
    plot clusters centers to KML
    """
    X = df.loc[
        :, ['THOR_DATA_VIET_ID', "TGTLATDD_DDD_WGS84", "TGTLONDDD_DDD_WGS84"]]
    kmeans = KMeans(n_clusters=4, init='k-means++')
    kmeans.fit(X[X.columns[1:3]])
    X['cluster_label'] = kmeans.fit_predict(X[X.columns[1:3]])
    centers = kmeans.cluster_centers_
    labels = kmeans.predict(X[X.columns[1:3]])
    plt.figure(figsize=(25, 25))
    plt.scatter(
        x=X['TGTLONDDD_DDD_WGS84'], y=X['TGTLATDD_DDD_WGS84'], c=labels)
    plt.scatter(centers[:, 1], centers[:, 0], c='black', s=200, alpha=0.5)
    plt.title('K-means Clustered')
    plt.savefig('Kmeans.png')
    plt.clf()
    print(centers)
    print(type(centers))
    print('plotting cluster centers to KML map')
    kmlmap = kml.KMLOutputParser('cluster-centers.kml')
    kmlmap.create_kml_header()
    clusterno = 1
    for cluster in centers:
        cluster = list(cluster)
        kmlmap.add_kml_placemark(
                str(clusterno), '',
                str(cluster[1]),
                str(cluster[0]),
                altitude='0')
        clusterno += 1
    kmlmap.close_kml_file()
    kmlmap.write_kml_doc_file()


def main():
    """
    main program code

    load dataset
    remove missions with no LAT LON co-ords
    filter to missions in the Indochina region
    #plot elbow curve
    cluster the data!
    """
    filename = 'thor_data_vietnam.csv'
    df = pd.read_csv(filename)
    df["TGTLONDDD_DDD_WGS84"].fillna('NO CO-ORDS', inplace=True)
    df["TGTLATDD_DDD_WGS84"].fillna('NO CO-ORDS', inplace=True)
    df = df[
        (df["TGTLONDDD_DDD_WGS84"] != 'NO CO-ORDS') &
        (df["TGTLATDD_DDD_WGS84"] != 'NO CO-ORDS')]
    df = df[
        (df['TGTLONDDD_DDD_WGS84'] >= 99) &
        (df['TGTLONDDD_DDD_WGS84'] <= 110) &
        (df['TGTLATDD_DDD_WGS84'] >= 8) &
        (df['TGTLATDD_DDD_WGS84'] <= 23)]
    #plot_elbow_curve(df)
    kmeans(df)


if __name__ == '__main__':
    main()
