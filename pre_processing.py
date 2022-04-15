DATASET_PATH = ''

cluster_model = None
cluster_model_path = ''

def get_cluster_model(dataset_path = DATASET_PATH):
    pass
    #if cluster_model is not None:
      #   return cluster_model

    #if <cluster model path> has cluster model:
        #cluster_model =
        #read that model and return


    #otherwise
    #read the dataset, clean the data, create cluster model, and dump in the cluster model path


    # docs = [nlp(text) for text in text_list]
    # for doc in docs:
    #     print(doc.vector)


    #cluster_model =
    #store the cluster model
    #return cluster_model

def create_cluster_model(dataset_path = DATASET_PATH):
    get_cluster_model(dataset_path)

def get_cluster_memberships(X_input):
    model = get_cluster_model()
    y_pred = model.predict(X_input)
    return y_pred

if '__name__' == '__main__':
    create_cluster_model(DATASET_PATH)

