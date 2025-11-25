import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN

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

    def cluster_trends(self, input_data):
        trends = input_data['trends']
        texts = [trend['trend'] for trend in trends]
        
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(texts)
        
        dbscan = DBSCAN(eps=0.5, min_samples=2)
        clusters = dbscan.fit_predict(X)
        
        output_clusters = {}
        for i, trend in enumerate(trends):
            cluster_id = clusters[i]
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
        
        return cluster_list

    def run(self):
        input_data = self.load_input_data()
        clustered_data = self.cluster_trends(input_data)
        self.save_output_data(clustered_data)
        print(f"Clustering selesai. Hasil tersimpan di {self.output_path}")

# Contoh penggunaan
if __name__ == "__main__":
    input_path = 'input_data.json'
    output_path = 'output_clusters.json'
    clusterizer = TrendClusterizer(input_path, output_path)
    clusterizer.run()