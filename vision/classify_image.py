"""
Created on 04/30/2017
Python 2.7.13

@author: Javier Urquizu
"""
import os, sys

import tensorflow as tf



RETRAIN_LABELS = "../tf_classifier/retrained_labels.txt"
RETRAIN_GRAPH = "../tf_classifier/retrained_graph_50000.pb"

TEST_SET_PATH = "../tf_classifier/ImageDataset/Test/"
# OR
TEST_IMAGE_PATH = "../tf_classifier/ImageDataset/Demo/pepsi_bottle_1.jpg"



def getImageSet(query_path):
    """
    Gets a dictionary containing all the images in the given path.
    Includes the imageClass and imagePath.
    """
    if (query_path.strip()[-3:].lower() == "jpg"):
        is_image = True
    else:
        is_image = False
    
    image_set_info = {}    

    # Parse path to return a dictionary with 1 key
    if (is_image): 
        path_split = query_path.split("/")
        imgInfo = { 'class':path_split[-2].lower(), 'path':query_path }
        image_set_info[path_split[-1].split(".")[0]] = imgInfo
    
    # Populate the dictionary with image information in containing folder
    else:
        classes = os.listdir(query_path)        
        for testClass in classes:
            for img in os.listdir(query_path +testClass):
                imgInfo = { 'class' : testClass.lower(), 'path' : (query_path +testClass +"/" +img) }
                image_set_info[img.split(".")[0]] = imgInfo
    
    return image_set_info
        

def classifyImages(retrain_graph, retrain_labels, query_path):
    """
    """
    # Loads label file & strips off '/r'
    class_labels = [line.rstrip() for line in tf.gfile.GFile(retrain_labels)]
    
    # Unpersists graph from file
    with tf.gfile.FastGFile(retrain_graph, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    # Get image set information
    image_set_info = getImageSet(query_path)
        
    # Get prediction/classification info
    with tf.Session() as sess: 
        for key in sorted(image_set_info.keys()):
            img_path = image_set_info[key]['path']
            img = tf.gfile.FastGFile(img_path, 'rb').read()
            print("\nClassifying: %s" % img_path.split("/")[-1])
            
            # Feed the test image as input to the graph and get 1st prediction
            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')        
            predicts = sess.run(softmax_tensor, {'DecodeJpeg/contents:0':img} )
            
            # Sort labels of 1st prediction in order of confidence
            top_k = predicts[0].argsort()[-len(predicts[0]):][::-1]
            
            # Parse classification info
            classInfo = []
            for i in top_k:
                classInfo.append({ 'score' : predicts[0][i], 'label' : class_labels[i] })
                
            image_set_info[key]['classInfo'] = classInfo     
    
    sess.close()    
    return image_set_info
   

def calcClassifierAccuracy(image_set_info, printInfo=True):
    """
    """
    classifierStats = {}
    incorrectImages = []
    totalCorrect = 0
    totalScore = 0.0
    
    if printInfo:
        print("\nClassifier Stats:")
    for key in sorted(image_set_info.keys()):
        gnd_label = image_set_info[key]['class']
        pred_label = image_set_info[key]['classInfo'][0]['label']
        score = image_set_info[key]['classInfo'][0]['score']
        
        if gnd_label == pred_label:
            totalCorrect = totalCorrect +1
            totalScore = totalScore +score
        else:
            incorrectImages.append(key)
            
        if printInfo:
            print('\nImage:\t"%s"' % key )
            for info in image_set_info[key]['classInfo']:
                print( '%s\t(score = %.5f)' % (info['label'], info['score']) )
            
            
    accuracy = float(totalCorrect)/len(image_set_info.keys())
    avgScore = totalScore / len(image_set_info.keys())
    
    classifierStats['accuracy'] = accuracy
    classifierStats['avgScore'] = avgScore
    classifierStats['incorrectImages'] = incorrectImages
    
    return classifierStats


if __name__ == '__main__':
    # Check that all input paths/files are valid
    for img_path in [TEST_SET_PATH, RETRAIN_LABELS, RETRAIN_GRAPH]:
        if not os.path.exists(img_path):
            sys.exit("%s does not exist!" % img_path)

    
    image_set_info = classifyImages(RETRAIN_GRAPH, RETRAIN_LABELS, TEST_IMAGE_PATH)
    image_set_stats = calcClassifierAccuracy(image_set_info)
    print("\n")