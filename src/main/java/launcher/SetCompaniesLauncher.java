package launcher;

import entity.Company;
import searvice.KabuService;
import utils.FileUtil;

import java.net.URISyntaxException;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.sql.SQLException;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * @author Tatsuya Oba
 */
public class SetCompaniesLauncher {
    private static final URL PATH = SetCompaniesLauncher.class.getResource("/kabu_list.csv");

    public static void main(String[] args) throws URISyntaxException, SQLException, ClassNotFoundException {
        final KabuService service = new KabuService();

        final List<Map<String, String>> list = FileUtil.csvToMap(PATH.toURI());
        final List<Company> companyList = list.stream()
                .map(companyCsv -> {
                    final Company company = new Company();
                    company.name = companyCsv.get("銘柄名");
                    company.market = companyCsv.get("市場");
                    company.code = companyCsv.get("コード");
                    return company;
                })
                .collect(Collectors.toList());
        service.saveCompanyList(companyList);
        service.close();
    }

    public static boolean isUTF8(byte[] src) {
        byte[] tmp = new String(src, StandardCharsets.UTF_8).getBytes(StandardCharsets.UTF_8);
        return Arrays.equals(tmp, src);
    }

}
