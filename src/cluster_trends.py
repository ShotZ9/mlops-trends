import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans, DBSCAN
import hdbscan
from sklearn.metrics import silhouette_score, davies_bouldin_score
import numpy as np

RANDOM_SEED = 42

np.random.seed(RANDOM_SEED) 
class TrendClusterizer:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

    def load_input_data(self):
        with open(self.input_path, 'r') as f:
            return json.load(f)

    def save_output_data(self, data):
        with open(self.output_path, 'w') as f:
            json.dump(data, f, indent=4)
    
    def harmonic_mean(self, silhouette_score, davies_bouldin_index):
        if davies_bouldin_index == 0:  # Prevent division by zero
            return 0
        return 2 * (silhouette_score * (1 / davies_bouldin_index)) / (silhouette_score + (1 / davies_bouldin_index))

    def cluster_trends(self, input_data):
        trends = input_data['trends']
        texts = [trend['trend'] for trend in trends]
        
        vectorizer = TfidfVectorizer(max_df=0.5, min_df=2, stop_words='english')
        X = vectorizer.fit_transform(texts)
        print(type(X))
        silhouette_scores = []
        min_cluster, max_cluster = 2, 10
        for k in range(min_cluster, max_cluster):  # Misalnya, coba dari 2 sampai 10 cluster
            kmeans = KMeans(n_clusters=k, random_state=RANDOM_SEED)
            kmeans.fit(X)
            labels = kmeans.labels_
            score = silhouette_score(X, labels)
            silhouette_scores.append(score)

        best_score = max(silhouette_scores)
        best_n_clusters = silhouette_scores.index(best_score) + min_cluster
        print("n cluster terbaik untuk KMeans: ", best_n_clusters)
        # Define models
        models = {
            'KMeans': KMeans(n_clusters=best_n_clusters, random_state=RANDOM_SEED),
            'DBSCAN': DBSCAN(eps=0.3, min_samples=3),
            'HDBSCAN': hdbscan.HDBSCAN(min_samples=3, min_cluster_size=3)
        }
        
        # Evaluate models
        results = {}
        for name, model in models.items():
            model.fit(X)
            labels = model.labels_
            
            # Convert sparse matrix to dense array if necessary
            X_dense = X.toarray()  # Convert to dense array
            
            if len(set(labels)) > 1:  # Ensure there are at least two clusters
                silhouette = silhouette_score(X_dense, labels)
                davies_bouldin = davies_bouldin_score(X_dense, labels)
                harmonic_mean = self.harmonic_mean(silhouette, davies_bouldin)
            else:
                silhouette = -1
                davies_bouldin = -1

            results[name] = {
                'silhouette_score': silhouette,
                'davies_bouldin_score': davies_bouldin,
                'harmonic_mean': harmonic_mean,
                'labels': labels
            }
        
        best_model_name = max(results, key=lambda k: results[k]['harmonic_mean'])
        best_model = models[best_model_name]
        best_labels = best_model.labels_
        
        output_clusters = {}
        for i, trend in enumerate(trends):
            cluster_id = best_labels[i]
            if cluster_id not in output_clusters:
                output_clusters[cluster_id] = []
            output_clusters[cluster_id].append({
                "trend": trend['trend'],
                "url": trend['url'],
                "data_count": trend['data_count']
            })
        
        cluster_list = []
        for cluster_id, trends in output_clusters.items():
            cluster_list.append({
                "title": f"Cluster {cluster_id}" if cluster_id != -1 else "Noise",
                "trends": trends
            })
        
        return cluster_list, results

    def run(self):
        input_data = self.load_input_data()
        clustered_data, evaluation_results = self.cluster_trends(input_data)
        self.save_output_data(clustered_data)
        print(f"Clustering selesai. Hasil tersimpan di {self.output_path}")
        print("Hasil evaluasi model:")
        for name, result in evaluation_results.items():
            print(f"{name}: Silhouette Score = {result['silhouette_score']:.3f}, Davies-Bouldin Index = {result['davies_bouldin_score']:.3f}, Harmonic Mean = {result['harmonic_mean']:.3f}")

# Contoh penggunaan
if __name__ == "__main__":
    input_path = 'data/trends.json'
    output_path = 'clusty.json'
    clusterizer = TrendClusterizer(input_path, output_path)
    clusterizer.run()