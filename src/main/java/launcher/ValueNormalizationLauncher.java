package launcher;

import entity.Value;
import searvice.KabuService;

import java.sql.SQLException;
import java.util.List;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * @author Tatsuya Oba
 */
public class ValueNormalizationLauncher {
    public static void main(String[] args) throws SQLException, ClassNotFoundException {
        final KabuService service = new KabuService();
        final AtomicInteger counter = new AtomicInteger();
        service.getAllCompanyList().forEach(company -> {
            if (counter.incrementAndGet() % 100 == 0) {
                System.out.println(counter);
            }
            final List<Value> valueList = service.getValueListByCompany(company);
            for (int i = 1; i < valueList.size(); i++) {
                try {
                    valueList.get(i).changeRate = valueList.get(i).endValue / valueList.get(i - 1).endValue - 1;
                } catch (ArithmeticException e) {
                    System.out.println(valueList.get(i).id + ": end value = 0");
                }
            }
            service.updateChangeRate(valueList);
        });
        service.close();
    }
}
