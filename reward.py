import csv

class AverageReward():
    def __init__(self, initial_measurement, num_measurements = 3, threshold = 0.01):
        #must be THRESHOLD % higher than average of last rewards to be counted as improvement-- vice versa for a worse result (negative reward)
        #this should help against small measurement errors that don't actually affect performance
        self.THRESHOLD = threshold
        self.last_measurements = [initial_measurement] * num_measurements

#-1 to 1 reward function based on rolling window of past x results
class BinaryAverageReward(AverageReward):
    def __init__(self, initial_measurement, num_measurements = 3, threshold = 0.01):
        super().__init__(initial_measurement, num_measurements = num_measurements, threshold = threshold)

    def get_reward(self, new_measurement):
        avg = sum(self.last_measurements) / len(self.last_measurements)
        self.last_measurements.pop(0)
        self.last_measurements.append(new_measurement)
        if new_measurement > self.THRESHOLD*avg + avg:
            return 1
        if new_measurement < -self.THRESHOLD*avg + avg:
            return -1
        return 0

#reward function based on rolling window of past x results, but uses the difference between measurements as the reward
class ContinuousAverageReward(AverageReward):
    def __init__(self, initial_measurement, num_measurements = 3, threshold=0.01):
        super().__init__(initial_measurement, num_measurements = num_measurements, threshold = threshold)

    def get_reward(self, new_measurement):
        avg = sum(self.last_measurements) / len(self.last_measurements)
        self.last_measurements.pop(0)
        self.last_measurements.append(new_measurement)
        if new_measurement > self.THRESHOLD*avg + avg:
            return new_measurement - avg
        if new_measurement < -self.THRESHOLD*avg + avg:
            return new_measurement - avg
        return 0



#USAGE:
if __name__ == "__main__":
    #binary
    b = BinaryAverageReward(150) #150 is a fake initial measurement, you would want to run the benchmark to get this number
    for i in [150, 140, 190, 200, 156]: #these are fake throughput measurements, it should be obtained through the benchmark connector
        print(b.get_reward(i))

    print("====")

    #...and continuous
    c = ContinuousAverageReward(150) #150 is a fake initial measurement, you would want to run the benchmark to get this number
    for i in [150, 140, 190, 200, 156]: #these are fake throughput measurements, it should be obtained through the benchmark connector
        print(c.get_reward(i))
