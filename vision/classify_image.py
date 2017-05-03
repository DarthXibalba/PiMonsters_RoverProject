"""
Created on 04/30/2017
Python 2.7.13

@author: Javier Urquizu
"""
import os, sys

import tensorflow as tf



TEST_SET_PATH = "../tf_classifier/ImageDataset/Test/"
RETRAIN_LABELS = "../tf_classifier/retrained_labels.txt"
RETRAIN_GRAPH = "../tf_classifier/retrained_graph_50000.pb"



def getImageSet(image_set_path):
    """
    Gets a dictionary containing all the images in the given path.
    Includes the imageClass and imagePath.
    """
    image_set = {}
    classes = os.listdir(image_set_path)
    
    for testClass in classes:
        for img in os.listdir(image_set_path +testClass):
            imgInfo = { 'class' : testClass.lower(), 'path' : (image_set_path +testClass +"/" +img) }
            image_set[img.split(".")[0]] = imgInfo

    return image_set


def classifyImage(retrain_graph, retrain_labels, query_path, pathType="image_set", printInfo=True):
    """
    """
    # Loads label file & strips off '/r'
    class_labels = [line.rstrip() for line in tf.gfile.GFile(retrain_labels)]
    
    # Unpersists graph from file
    with tf.gfile.FastGFile(retrain_graph, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')
        
    # Get prediction/classification info
    with tf.Session() as sess:
        # Read in the test image
        testImg = tf.gfile.FastGFile(query_path, 'rb').read()
        
        # Feed the test image as input to the graph and get 1st prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')        
        predicts = sess.run(softmax_tensor, {'DecodeJpeg/contents:0':testImg} )
        
        # Sort labels of 1st prediction in order of confidence
        top_k = predicts[0].argsort()[-len(predicts[0]):][::-1]
    sess.close()
    
    # Parse classification info
    classifyInfo = []
    for i in top_k:
        classifyInfo.append({ 'score' : predicts[0][i], 'label' : class_labels[i] })
    
    # Display information
    if printInfo:
        print('\nUsing graph model: "%s"' % retrain_graph)
        print('\nImage:\t"%s"' % query_path.split("/")[-1] )
        for info in classifyInfo:
            print( '%s\t(score = %.5f)' % (info['label'], info['score']) )
            
    return classifyInfo

'''
def classifyImageSet(retrain_graph, retrain_labels, set_path, printInfo=True):
'''     

def calcImageSetAccuracy(printInfo=True):
    pass



if __name__ == '__main__':
    # Check that all input paths/files are valid
    for img_path in [TEST_SET_PATH, RETRAIN_LABELS, RETRAIN_GRAPH]:
        if not os.path.exists(img_path):
            sys.exit("%s does not exist!" % img_path)
    
    
    test_class = "Sprite"
    test_img = "sprite_logo_3.jpg"
    test_img_path = TEST_SET_PATH +test_class +"/" +test_img
    
    image_classification =  classifyImage(RETRAIN_GRAPH, RETRAIN_LABELS, test_img_path)
    
    image_set = getImageSet(TEST_SET_PATH)