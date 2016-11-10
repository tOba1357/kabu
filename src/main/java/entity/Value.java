package entity;

import java.sql.Date;
import java.sql.ResultSet;
import java.sql.SQLException;

/**
 * @author Tatsuya Oba
 */
public class Value {
    public Integer id;

    public Integer companyId;

    public Date date;

    public Double startValue;

    public Double endValue;

    public Double highValue;

    public Double lowValue;

    public Double volume;

    public Double tradingValue;

    public Double changeRate;


    public static Value createFromResultSet(final ResultSet resultSet) throws SQLException {
        final Value value = new Value();
        value.id = resultSet.getInt("id");
        value.companyId = resultSet.getInt("company_id");
        value.startValue = resultSet.getDouble("start_value");
        value.endValue = resultSet.getDouble("end_value");
        value.highValue = resultSet.getDouble("high_value");
        value.lowValue = resultSet.getDouble("low_value");
        value.volume = resultSet.getDouble("volume");
        value.tradingValue = resultSet.getDouble("trading_value");
        value.changeRate = resultSet.getDouble("change_rate");
        return value;
    }

    @Override
    public String toString() {
        return "id:" + id +
                ",companyId:" + companyId +
                ",date:" + date +
                ",startValue:" + startValue +
                ",endValue:" + endValue +
                ",highValue:" + highValue +
                ",lowValue:" + lowValue +
                ",volume:" + volume +
                ",tradingValue:" + tradingValue +
                ",changeRate:" + changeRate;
    }
}
