import numpy as np

def extract_features(mfcc_input, sampling_rate=None):
    # mfcc_input is a 1-D array of flattened MFCCs from Edge Impulse
    # Reshape into (num_frames, num_coeffs)
    
    num_coeffs = 13
    num_frames = len(mfcc_input) // num_coeffs
    mfcc_matrix = np.reshape(mfcc_input, (num_frames, num_coeffs))

    # Compute summary statistics
    mfcc_mean = np.mean(mfcc_matrix, axis=0)
    
    feature_names = [f"mfcc_mean_{i}" for i in range(num_coeffs)]
    features = dict(zip(feature_names, mfcc_mean.tolist()))
    return features
