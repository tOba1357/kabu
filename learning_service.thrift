service LearningService {
    void learn(1:list<list<list<double>>> inputData, 2:list<list<double>> targets, 3:i16 epochSize, 4:i16 batchSize)
    list<list<double>> precit(1:list<list<list<double>>> inputData)
}