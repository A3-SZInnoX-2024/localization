import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN

# 生成模拟数据
np.random.seed(0)
# 创建两组数据，每组数据周围随机分布
cluster1 = np.random.normal(0.5, 0.1, (100, 2))
cluster2 = np.random.normal(1.5, 0.1, (100, 2))
data = np.vstack((cluster1, cluster2))

# 应用DBSCAN聚类
dbscan = DBSCAN(eps=2, min_samples=5)
clusters = dbscan.fit_predict(data)

# 可视化结果
plt.scatter(data[:, 0], data[:, 1], c=clusters, cmap="viridis", marker="o", s=50)
plt.title("DBSCAN Clustering")
plt.xlabel("X")
plt.ylabel("Y")
plt.colorbar(label="Cluster ID")
plt.show()
