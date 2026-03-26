def run_model(alpha, beta, gamma):
    
    accuracy = 0.8 + alpha * 0.1
    loss = 0.4 - beta * 0.1

    curve = [0.5, 0.6, 0.7, accuracy]

    return {
        "Accuracy": accuracy,
        "Loss": loss,
        "Training Curve": curve
    }