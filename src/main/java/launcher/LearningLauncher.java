package launcher;

import entity.Company;
import entity.Value;
import javafx.util.Pair;
import org.apache.thrift.TException;
import org.apache.thrift.protocol.TBinaryProtocol;
import org.apache.thrift.protocol.TProtocol;
import org.apache.thrift.transport.TSocket;
import org.apache.thrift.transport.TTransportException;
import searvice.KabuService;

import java.sql.SQLException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;

/**
 * @author Tatsuya Oba
 */
public class LearningLauncher {
    public static void main(String[] args) throws SQLException, ClassNotFoundException, TException {
        final TSocket transport = new TSocket("localhost", 9090);
        transport.open();
        final TProtocol protocol = new TBinaryProtocol(transport);
        final LearningService.Client client = new LearningService.Client(protocol);

        final KabuService service = new KabuService();
        final List<Company> companyList = service.getAllCompanyList();
        companyList.forEach(company -> {
            try {
                final List<Value> valueList = service.getValueListByCompany(company);
                final LearningData data = createLearningData(valueList, 50);
                if (data == null) return;
                client.learn(data.inputData, data.targets, (short) 20, (short) 100);
            } catch (SQLException | TException e) {
                e.printStackTrace();
            }
        });
        transport.close();
    }

    private static LearningData createLearningData(
            final List<Value> valueList,
            final int batchSize
    ) {
        final int size;
        if (valueList.size() % batchSize == 0) {
            size = valueList.size() - batchSize + 1;
        } else {
            size = valueList.size() - valueList.size() % batchSize + 1;
        }
        if (size <= 1) {
            return null;
        }
        final LearningData data = new LearningData();
        final List<List<Double>> processedInputData = valueList.stream()
                .map(value -> value.endValue)
                .map(Collections::singletonList)
                .collect(Collectors.toList());
        data.inputData = split(processedInputData.subList(0, size - 1), batchSize);
        final List<List<Double>> processedTargets = data.inputData.subList(1, data.inputData.size()).stream()
                .map(inputDataList -> inputDataList.get(0))
                .collect(Collectors.toList());
        processedTargets.add(Collections.singletonList(valueList.get(size - 1).endValue));
        data.targets = processedTargets;
        return data;
    }

    private static <T> List<List<T>> split(final List<T> list, final int size) {
        final List<List<T>> rtn = new ArrayList<>();
        for (int i = 0; i < ((list.size() + size - 1) / size); i++) {
            rtn.add(list.subList(i * size, Math.min(list.size(), i * size + size)));
        }
        return rtn;
    }

    static class LearningData {
        public List<List<List<Double>>> inputData;
        public List<List<Double>> targets;
    }
}
