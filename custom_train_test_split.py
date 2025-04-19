import numpy as np

def custom_train_test_split(X, y, test_size=0.2, shuffle=True, random_state=None):
    # Convert to numpy if not already
    X = np.array(X)
    y = np.array(y)
    
    # Check same length
    assert len(X) == len(y), "X and y must be the same length"
    
    n_samples = len(X)
    
    # Handle test size
    if isinstance(test_size, float):
        test_count = int(n_samples * test_size)
    elif isinstance(test_size, int):
        test_count = test_size
    else:
        raise ValueError("test_size must be float or int")

    indices = np.arange(n_samples)

    # Shuffling
    if shuffle:
        if random_state is not None:
            np.random.seed(random_state)
        np.random.shuffle(indices)

    # Split indices
    test_indices = indices[:test_count]
    train_indices = indices[test_count:]

    # Final split
    X_train = X[train_indices]
    X_test = X[test_indices]
    y_train = y[train_indices]
    y_test = y[test_indices]

    return X_train, X_test, y_train, y_test
