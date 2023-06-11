def save_parameters(train_function):
    """
    Decorator for models training functions, that saves created coefficient to database
    """
    def inner_train_function(*args, **kwargs):
        print("Training decorator is called")
        print("Length of df: "+str(args[0].datasource_length))
        return train_function(*args, **kwargs)
    return inner_train_function

