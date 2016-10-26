package launcher;

import entity.Company;
import searvice.KabuService;

import java.sql.SQLException;
import java.util.List;

/**
 * @author Tatsuya Oba
 */
public class TestLauncher {
    public static void main(String[] args) throws SQLException, ClassNotFoundException {
        final KabuService service = new KabuService();

//        final Company company = new Company();
//        company.name = "株式会社test";
//        company.code = "72783_T";
//        company.market = "東証";
//        service.saveCompanyList(company);

        final List<Company> companyList = service.getAllCompanyList();
        companyList.forEach(System.out::println);

        service.close();
    }
}
