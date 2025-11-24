
nr_users = 2000
nr_movies = 1500


def train_baseline(training_data):
    """
    Uses the provided dataset to train the baseline predictor. 
    Should return three things:
    r_bar: the average rating over all users and movies
    bu: vector where the i:th entry represents the bias of the i:th user compared to r_bar
    bm: vector where the i:th entry represents the bias of the i:th movie compared to r_bar
    """
    
    

    return r_bar,bu,bm

def baseline_prediction(training_data,datasets_to_predict):
    """
    Uses the training_data to train the baseline predictor, 
    then evaluates its performance on all the datasets in the test_datas list 
    """
    r_bar,bu,bm = train_baseline(training_data)

    
    # Create a list with one element for each dataset in datasets_to_predict.
    # Each entry (r_hat) should be an array with the predicted ratings for all pairs of users and movies in that dataset
    r_hats = []
    for data in datasets_to_predict:
        r_hat = 
        r_hats.append(r_hat)

    return r_hats

def neighborhood_prediction(training_data,datasets_to_predict,u_min=1,L=nr_movies):
    """
    Uses the training_data to train the improved predictor, 
    then evaluates its performance on all the datasets in the test_datas list 
    """

    # ========================== Create the cosine similarity matrix D ==========================
    D =

    # Uncomment the following lines to check the correctness of the D matrix for u_min = 20 in the verification dataset
    # You should get an error that is less than 1e-5
    #
    # if filename == "verification" and u_min == 20:
    #     error_in_D = np.linalg.norm(np.load('verification_D_mat.npy') - D)
    #     print("Error in D matrix: {0:.5f}\n".format(error_in_D))

    # =================== Evaluate the performance of the improved predictor ====================
    r_hats = []
    for data in datasets_to_predict:
        r_hat = 
        r_hats.append(r_hat)

    return r_hats


def RMSE(r_hat,r):
    # Compute the RMSE between the true ratings r and the predicted ratings r_hat
    rmse = 
    return rmse

def draw_histogram(r_hat,r,name=""):
    # Create the described histogram
    return 0



filename = # "LiU-ID","task---2" or "verification"

training_data = load_data(filename+'.training')
test_data = load_data(filename+'.test')


# ====================================== TASK 2 ======================================
print("---- baseline predictor ----")

[r_hat_baseline_training,r_hat_baseline_test] = \
    baseline_prediction(training_data,[training_data,test_data])

rmse_baseline_training = RMSE(r_hat_baseline_training,training_data[:,2])
rmse_baseline_test = RMSE(r_hat_baseline_test,test_data[:,2])

print("Training RMSE: {0:.3f}".format(rmse_baseline_training))
print("Test RMSE: {0:.3f}".format(rmse_baseline_test))

draw_histogram(r_hat_baseline_test, test_data[:,2],"Baseline Test")


# ====================================== TASK 2 ======================================
u_min =
L = 
print("\n---- movie neighborhood predictor with u_min = {} and L = {} ----".format(u_min,L))

[r_hat_neighborhood_training,r_hat_neighborhood_test] = \
    neighborhood_prediction(training_data,[training_data,test_data],u_min,L)

rmse_neighborhood_training = RMSE(r_hat_neighborhood_training,training_data[:,2])
rmse_neighborhood_test = RMSE(r_hat_neighborhood_test,test_data[:,2])

print("Training RMSE: {0:.3f}".format(rmse_neighborhood_training))
print("Test RMSE: {0:.3f}".format(rmse_neighborhood_test))

print("\nTraining Improvement: {0:.3f}%".format(
    (rmse_baseline_training-rmse_neighborhood_training)/rmse_baseline_training*100))
print("Test Improvement: {0:.3f}%".format(
    (rmse_baseline_test-rmse_neighborhood_test)/rmse_baseline_test*100))


