package searvice;

import entity.Company;
import entity.Value;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

/**
 * @author Tatsuya Oba
 */
public class KabuService {
    private static final String URL = "jdbc:mysql://localhost:3306/kabudb";
    private static final String DRIVER = "com.mysql.jdbc.Driver";
    private static final String USER_NAME = "root";
    private static final String PASSWORD = "root";

    private final Connection connection;

    public KabuService() throws SQLException, ClassNotFoundException {
        Class.forName(DRIVER);
        this.connection = DriverManager.getConnection(URL, USER_NAME, PASSWORD);
    }

    private static final String GET_COMPANY_QUERY = "SELECT * FROM tblcompanies ORDER BY id";
    public List<Company> getAllCompanyList() throws SQLException {
        final Statement statement = connection.createStatement();
        final ResultSet rs = statement.executeQuery(GET_COMPANY_QUERY);
        final List<Company> companyList = new ArrayList<>();
        while (rs.next()) {
            companyList.add(Company.createFromResultSet(rs));
        }
        statement.close();
        return companyList;
    }

    private static final String GET_COMPANY_QUERY_BY_ID_QUERY = "SELECT * FROM tblcompanies WHERE id >= ? ORDER BY id";
    public List<Company> getCompanyListLteId(final int minId) throws SQLException {
        final PreparedStatement statement = connection.prepareStatement(GET_COMPANY_QUERY_BY_ID_QUERY);
        statement.setInt(1, minId);
        final ResultSet rs = statement.executeQuery();
        final List<Company> companyList = new ArrayList<>();
        while (rs.next()) {
            companyList.add(Company.createFromResultSet(rs));
        }
        statement.close();
        return companyList;
    }

    private static final String SAVE_COMPANY_QUERY = "INSERT INTO tblcompanies (name, code, market) VALUES(?, ?, ?)";
    public void saveCompany(final Company company) throws SQLException {
        final PreparedStatement statement = connection.prepareStatement(SAVE_COMPANY_QUERY);
        statement.setString(1, company.name);
        statement.setString(2, company.code);
        statement.setString(3, company.market);
        statement.executeUpdate();
    }

    public void saveCompanyList(final List<Company> companyList) throws SQLException {
        final PreparedStatement statement = connection.prepareStatement(SAVE_COMPANY_QUERY);
        for (final Company company : companyList) {
            statement.setString(1, company.name);
            statement.setString(2, company.code);
            statement.setString(3, company.market);
            statement.addBatch();
        }
        statement.executeBatch();
    }

    private static final String SAVE_VALUE_QUERY = "INSERT INTO tblvalues (company_id, date, start_value, high_value, low_value, end_value, volume, trading_value) VALUES(?, ?, ?, ?, ?, ?, ?, ?)";
    public void saveValue(final Value value) throws SQLException {
        final PreparedStatement statement = connection.prepareStatement(SAVE_VALUE_QUERY);
        statement.setInt(1, value.companyId);
        statement.setDate(2, value.date);
        statement.setDouble(3, value.startValue);
        statement.setDouble(4, value.highValue);
        statement.setDouble(5, value.lowValue);
        statement.setDouble(6, value.endValue);
        statement.setDouble(7, value.volume);
        statement.setDouble(8, value.tradingValue);

        statement.executeUpdate();
    }

    public void saveValueList(final List<Value> valueList) throws SQLException {
        final PreparedStatement statement = connection.prepareStatement(SAVE_VALUE_QUERY);
        for (final Value value : valueList) {
            statement.setInt(1, value.companyId);
            statement.setDate(2, value.date);
            statement.setDouble(3, value.startValue);
            statement.setDouble(4, value.highValue);
            statement.setDouble(5, value.lowValue);
            statement.setDouble(6, value.endValue);
            statement.setDouble(7, value.volume);
            statement.setDouble(8, value.tradingValue);

            statement.addBatch();
        }
        statement.executeBatch();
    }

    private static final String GET_VALUE_QUERY = "SELECT * FROM tblvalues WHERE company_id = ? AND date = ?";
    public boolean contain(final Value value) throws SQLException {
        final PreparedStatement statement = connection.prepareStatement(GET_VALUE_QUERY);
        statement.setInt(1, value.companyId);
        statement.setDate(2, value.date);
        final ResultSet resultSet = statement.executeQuery();
        final boolean contain = resultSet.next();
        resultSet.close();
        statement.close();
        return contain;
    }

    public static final String GET_VALUE_BY_COMPANY_QUERY = "SELECT * FROM tblvalues WHERE company_id = ? ORDER BY date";
    public List<Value> getValueListByCompany(final Company company) throws SQLException {
        final PreparedStatement statement = connection.prepareStatement(GET_VALUE_BY_COMPANY_QUERY);
        statement.setInt(1, company.id);

        final ResultSet resultSet = statement.executeQuery();
        final List<Value> valueList = new ArrayList<>();
        while (resultSet.next()) {
            valueList.add(Value.createFromResultSet(resultSet));
        }
        resultSet.close();
        statement.close();
        return valueList;
    }

    private static final String GET_VALUE_FOR_LEARNING_QUERY = "SELECT * FROM tblvalues WHERE company_id = ? ORDER BY date LIMIT ?, ?";
    public List<Value> getValueListsForLearning(
            final Company company,
            final int from,
            final int size
    ) throws SQLException {
        final PreparedStatement statement = connection.prepareStatement(GET_VALUE_FOR_LEARNING_QUERY);
        statement.setInt(1, company.id);
        statement.setInt(2, from);
        statement.setInt(3, size);
        final ResultSet resultSet = statement.executeQuery();

        final List<Value> valueList = new ArrayList<>();
        while (resultSet.next()) {
            valueList.add(Value.createFromResultSet(resultSet));
        }
        return valueList;
    }

    private static final String SAVE_LOG_QUERY = "INSERT INTO tbllearning_log (company_id) VALUES (?)";
    public void saveLog(final Company company) throws SQLException {
        final PreparedStatement statement = connection.prepareStatement(SAVE_LOG_QUERY);
        statement.setInt(1, company.id);
        statement.executeUpdate();
    }

    public void close() throws SQLException {
        connection.close();
    }
}
