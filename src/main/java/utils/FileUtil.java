package utils;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.URI;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * @author Tatsuya Oba
 */
public class FileUtil {
    public static List<Map<String, String>> csvToMap(final String uri) {
        return csvToMap(Paths.get(uri));
    }

    public static List<Map<String, String>> csvToMap(final URI uri) {
        return csvToMap(Paths.get(uri));
    }

    public static List<Map<String, String>> csvToMap(final Path path) {
        try (final BufferedReader bf = Files.newBufferedReader(path, Charset.forName("SHIFT-JIS"))) {
            final String[] head = bf.readLine().split(",\\s*");
            return bf.lines()
                    .map(line -> line.split(",\\s*"))
                    .map(values -> new LinkedHashMap<String, String>() {{
                        for (int i = 0; i < head.length; i++) {
                            put(head[i], values[i]);
                        }
                    }})
                    .collect(Collectors.toList());
        } catch (IOException e) {
            e.printStackTrace();
        }
        return Collections.emptyList();
    }
}
