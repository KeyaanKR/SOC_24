import json
import numpy as np
import matplotlib.pyplot as plt

def inv_transform(distribution: str, num_samples: int, **kwargs) -> list:
    """ populate the 'samples' list from the desired distribution """

    samples = []

    # TODO: first generate random numbers from the uniform distribution
    # round the random numbers to 4 decimal places
    rand_samples = np.round(np.random.uniform(0, 1, num_samples), 4)
    
    if distribution == "cauchy":
        peak_x = kwargs.get('peak_x')
        gamma = kwargs.get('gamma')
        for random in rand_samples:
            samples.append(peak_x + gamma * np.tan(np.pi * (random - 0.5)))

    elif distribution == "exponential":
        lambda_ = kwargs.get('lambda')
        for random in rand_samples:
            samples.append(-1/lambda_ * np.log(1 - random))
    # END TODO

    return samples

if __name__ == "__main__":
    np.random.seed(42)

    for distribution in ["cauchy", "exponential"]:
        file_name = "q1_" + distribution + ".json"
        args = json.load(open(file_name, "r"))
        samples = inv_transform(**args)
        
        with open("q1_output_" + distribution + ".json", "w") as file:
            json.dump(samples, file)

        # TODO: plot and save the histogram to "q1_" + distribution + ".png"
        plt.figure()
        plt.hist(samples, bins=100)
        plt.title(distribution + " distribution")
        plt.savefig("q1_" + distribution + ".png")
        plt.close()
        # END TODO
