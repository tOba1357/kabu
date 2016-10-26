package utils;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLConnection;

/**
 * @author Tatsuya Oba
 */
public class HttpConnectionUtils {
    public static boolean saveFile(final File file, final URL url) {
        try {
            final URLConnection connection = url.openConnection();
            final InputStream in = connection.getInputStream();
            final FileOutputStream fos = new FileOutputStream(file);
            byte[] buf = new byte[512];
            while (true) {
                int len = in.read(buf);
                if (len == -1) {
                    break;
                }
                fos.write(buf, 0, len);
            }
            in.close();
            fos.flush();
            fos.close();
            return true;
        } catch (IOException e) {
            e.printStackTrace();
        }
        return false;
    }
}
