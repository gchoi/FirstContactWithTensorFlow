# -*- coding: utf-8 -*-
"""
k-Means running on TF version 1.3

Created on Mon Oct 16 16:38:58 2017

@author: gchoi
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import tensorflow as tf

num_vectors = 1000
num_clusters = 3
num_steps = 100

vector_values = []
for i in range(num_vectors):
  if np.random.random() > 0.5:
    vector_values.append([np.random.normal(0.5, 0.6), np.random.normal(0.3, 0.9)])
  else:
    vector_values.append([np.random.normal(2.5, 0.4), np.random.normal(0.8, 0.5)])

df = pd.DataFrame({"x": [v[0] for v in vector_values], "y": [v[1] for v in vector_values]})
sns.lmplot("x", "y", data=df, fit_reg=False, size=7)
plt.show()

vectors = tf.constant(vector_values)
centroids = tf.Variable( tf.slice( tf.random_shuffle( vectors ), [0,0], [num_clusters, -1] ) )

expanded_vectors = tf.expand_dims(vectors, 0)
expanded_centroids = tf.expand_dims(centroids, 1)

print( expanded_vectors.get_shape() )
print( expanded_centroids.get_shape() )

distances = tf.reduce_sum( tf.square( tf.subtract( expanded_vectors, expanded_centroids ) ), 2 )
assignments = tf.argmin(distances, 0)

### TEST
c = 0
tmp1 = tf.equal(assignments, c)
tmp2 = tf.where(tmp1)
tmp3 = tf.reshape(tmp2,[1,-1])
tmp4 = tf.gather(vectors, tmp3)
tmp5 = tf.reduce_mean(tmp4, reduction_indices=[1])
means = tf.concat([tmp5 for c in range(num_clusters)], 0)
###

means = tf.concat([
  tf.reduce_mean(
      tf.gather(vectors, 
                tf.reshape(
                  tf.where(
                    tf.equal(assignments, c)
                  ),[1,-1])
               ), reduction_indices=[1])
  for c in range(num_clusters)], 0)

update_centroids = tf.assign(centroids, means)
init_op = tf.initialize_all_variables()

with tf.Session() as sess:
  sess.run(init_op)
  for step in range(num_steps):
    _, centroid_values, assignment_values = sess.run([update_centroids,
                                                      centroids,
                                                      assignments])
  print( "centroids" )
  print( centroid_values )