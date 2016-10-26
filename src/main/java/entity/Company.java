package entity;

import java.sql.ResultSet;
import java.sql.SQLException;

/**
 * @author Tatsuya Oba
 */
public class Company {
    public Integer id;

    public String name;

    public String code;

    public String market;

    public static Company createFromResultSet(final ResultSet rs) throws SQLException {
        final Company company = new Company();
        company.id = rs.getInt("id");
        company.name = rs.getString("name");
        company.code = rs.getString("code");
        company.market = rs.getString("market");
        return company;
    }

    @Override
    public String toString() {
        return "id:" + id + ",name:" + name + ",code:" + code + ",market:" + market;
    }
}
