"""
Created on 04/30/2017
Python 2.7.13

@author: Javier Urquizu
"""
import os, sys

import tensorflow as tf



TEST_PATH = "../tf_classifier/ImageDataset/Test/"
TEST_CLASS = "Pepsi"
TEST_IMG = "pepsi_can_2.jpg"

RETRAIN_LABELS = "../tf_classifier/retrained_labels_5000.txt"
RETRAIN_GRAPH = "../tf_classifier/retrained_graph_5000.pb"



if __name__ == '__main__':
    if not os.path.exists(TEST_PATH):
        sys.exit("Test image path does not exist!")
    
    # Find all test images
    test_classes = os.listdir(TEST_PATH)
    test_images = {}
    for testClass in test_classes:
        test_images[testClass] = os.listdir(TEST_PATH +testClass)
    
    # Loads label file & strips off '/r'
    label_lines = [line.rstrip() for line in tf.gfile.GFile(RETRAIN_LABELS)]
    
    # Unpersists graph from file
    with tf.gfile.FastGFile(RETRAIN_GRAPH, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')
        
    with tf.Session() as sess:
        # Read in the test image
        test_img_path = TEST_PATH +TEST_CLASS +"/" +TEST_IMG
        testImg = tf.gfile.FastGFile(test_img_path, 'rb').read()
        
        # Feed the test image as input to the graph and get 1st prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')        
        predicts = sess.run(softmax_tensor, {'DecodeJpeg/contents:0':testImg} )
        
        # Sort labels of 1st prediction in order of confidence
        top_k = predicts[0].argsort()[-len(predicts[0]):][::-1]
        
        # Display information
        print('\nUsing labels: %s' % (RETRAIN_LABELS))
        print('Classifying: %s\n' % (TEST_IMG))
        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predicts[0][node_id]
            print('%s (score = %.5f)' % (human_string, score))
        